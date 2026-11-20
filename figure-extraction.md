# Figure Extraction Specification (自适应多栏布局与智能安全区插图提取规范)

本文件作为 [SKILL.md](./SKILL.md) `§5.1` 的执行参考，仅在**博客生成模式**或用户要求提取高精图表时按需加载。

---

## 1. 核心设计原则

1. **自适应分栏感知 (Adaptive Layout Detection):**
   严禁硬编码 `W / 2` 左右分栏分割线。必须通过分析页面正文文本块的水平分布，自动判定页面是**单栏 (Single-Column)**、**双栏 (Double-Column)** 还是**通栏跨栏大图 (Full-Width Figure)**，动态计算真实的栏间隙（Gutter Gap）与栏边界。
2. **图内元素与图例安全区保护 (Safe-Zone Preservation):**
   严禁仅凭“字符长度 > 40”粗暴遮罩！系统架构图、流程图和原理图内部往往包含大量长模块名、参数注释与图例文本（如 `Acoustic Tokenizer (Frozen Codebook)`）。
   - **保护策略:** 凡完全落入图表矢量元素集聚区（Drawing Bounding Hull）或图像图元内的文字，一律判定为图内核心标注，加入安全白名单绝对保留；
   - 仅对**起始于图表外围、水平跨度接近完整栏宽且与图表拓展边距相交的正文段落块**执行内存白底遮罩。
3. **高解析度与视网膜渲染:** 渲染倍率固定为 `3.0x`（`fitz.Matrix(3.0, 3.0)`），保证 300+ DPI 超清画质，微信公众号与移动端视网膜屏无毛刺、无抗锯齿模糊。
4. **内存遮罩 (Zero Disk Mutation):** 所有白底矩形绘制（`page.draw_rect(..., fill=(1,1,1), overlay=True)`）均只在内存中的 `fitz.Page` 对象执行，不保存回原 PDF 文件，保障原文献无损。
5. **输出路径双写:** 裁剪后的 `.png` 插图必须同时保存至本地工作目录（如 `./figure/figure_X.png`）和系统的 Artifacts 目录（若当前环境存在）。

---

## 2. 生产级自适应提取脚本模板 (Windows UTF-8 Safe)

```python
import os
import sys
from typing import List, Optional, Tuple
import fitz  # PyMuPDF

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")


def detect_page_columns(page: fitz.Page) -> Tuple[str, float, float]:
    """通过文本块聚类分析页面分栏布局。

    返回:
        (layout_type, col1_right, col2_left)
        layout_type: "double" | "single"
        col1_right: 左栏右边界 (若为 single 则为页面右边界)
        col2_left: 右栏左边界 (若为 single 则为页面左边界)
    """
    W, H = page.rect.width, page.rect.height
    blocks = page.get_text("blocks")

    # 提取主体正文文本块 (剔除页眉页脚与短标注)
    body_blocks = [
        b
        for b in blocks
        if 40 < b[1] < H - 40 and 40 < b[3] < H - 30 and len(b[4].strip()) > 50
    ]

    if not body_blocks:
        return "single", W, 0.0

    # 收集正文块的起始与结束 X 坐标
    x0_list = sorted([b[0] for b in body_blocks])
    x1_list = sorted([b[2] for b in body_blocks])

    mid_W = W * 0.5
    left_x1 = [x for x in x1_list if x < mid_W + 20]
    right_x0 = [x for x in x0_list if x > mid_W - 20]

    # 如果左右两边都有明显聚集的正文，则判定为双栏
    if len(left_x1) >= 3 and len(right_x0) >= 3:
        col1_r = max(left_x1)
        col2_l = min(right_x0)
        # 预留 2pt 安全间隙
        return "double", min(col1_r + 2, W * 0.5), max(col2_l - 2, W * 0.5)

    return "single", W, 0.0


def calculate_figure_bbox(
    page: fitz.Page,
    caption_prefix: str,  # 例如 "Figure 1:" 或 "Fig. 1"
    padding: float = 6.0,
) -> Tuple[Optional[fitz.Rect], Optional[fitz.Rect]]:
    """根据题注锚点与关联图元动态计算图表的裁剪框与绘图安全核心区。

    返回:
        (crop_rect, drawing_hull)
    """
    caption_matches = page.search_for(caption_prefix)
    if not caption_matches:
        return None, None

    cap_rect = caption_matches[0]
    W, H = page.rect.width, page.rect.height

    # 获取页面上所有矢量绘图和图像图元
    drawings = page.get_drawings()
    images = page.get_images()

    # 寻找在题注上方 (或紧邻下方) 的关联绘图元素
    # 统计题注上方合理距离内的绘图闭包
    relevant_rects = []
    for d in drawings:
        r = d["rect"]
        # 仅吸纳面积合理且在题注上方的图元 (学术论文通常图在上方，题注在下方)
        if (
            r.y1 <= cap_rect.y1 + 5
            and r.y1 > cap_rect.y0 - 450
            and r.width > 20
            and r.height > 20
        ):
            # 排除全页背景或通栏顶线
            if r.width < W * 0.98 or r.height < H * 0.9:
                relevant_rects.append(r)

    # 检查嵌入式位图
    for img in page.get_image_info():
        r = fitz.Rect(img["bbox"])
        if (
            r.y1 <= cap_rect.y1 + 10
            and r.y1 > cap_rect.y0 - 450
            and r.width > 30
            and r.height > 30
        ):
            relevant_rects.append(r)

    if relevant_rects:
        # 合并所有关联图元构成核心绘图区 (Drawing Hull)
        hull = relevant_rects[0]
        for r in relevant_rects[1:]:
            hull = hull | r
    else:
        # 备选：无矢量图元时以题注宽度和预估比例向上延伸
        hull = fitz.Rect(
            cap_rect.x0, max(40.0, cap_rect.y0 - 200), cap_rect.x1, cap_rect.y0
        )

    # 包含图表核心区与题注，外扩安全边距
    crop_rect = (
        fitz.Rect(
            min(hull.x0, cap_rect.x0) - padding,
            hull.y0 - padding,
            max(hull.x1, cap_rect.x1) + padding,
            cap_rect.y1 + padding,
        )
        & page.rect
    )

    return crop_rect, hull


def smart_mask_and_crop_figure(
    pdf_path: str,
    page_num: int,
    caption_prefix: str,
    output_paths: List[str],
    zoom: float = 3.0,
    manual_crop_rect: Optional[fitz.Rect] = None,
) -> bool:
    """自适应探测排版、智能安全区保护并在内存中遮罩裁剪高精插图。"""
    doc = fitz.open(pdf_path)
    page = doc[page_num]
    W, H = page.rect.width, page.rect.height

    if manual_crop_rect:
        crop_rect = manual_crop_rect
        drawing_hull = manual_crop_rect
    else:
        crop_rect, drawing_hull = calculate_figure_bbox(page, caption_prefix)
        if not crop_rect:
            doc.close()
            return False

    layout, col1_r, col2_l = detect_page_columns(page)

    # 1. 跨栏正文防渗透遮罩 (仅在双栏排版生效)
    if layout == "double":
        fig_mid_x = (crop_rect.x0 + crop_rect.x1) * 0.5
        is_span_both = (
            crop_rect.width > W * 0.65 or crop_rect.x0 < col1_r < crop_rect.x1
        )

        if not is_span_both:
            if fig_mid_x < W * 0.5:
                # 图在左栏：向右栏正文区绘白，预留安全间隙
                page.draw_rect(
                    fitz.Rect(col2_l, 0, W, H),
                    color=(1, 1, 1),
                    fill=(1, 1, 1),
                    overlay=True,
                )
            else:
                # 图在右栏：向左栏正文区绘白
                page.draw_rect(
                    fitz.Rect(0, 0, col1_r, H),
                    color=(1, 1, 1),
                    fill=(1, 1, 1),
                    overlay=True,
                )

    # 2. 上下正文相交白底遮罩 (图内图例文本安全白名单)
    for block in page.get_text("blocks"):
        bx0, by0, bx1, by1, text, *_ = block
        b_rect = fitz.Rect(bx0, by0, bx1, by1)
        clean_text = text.strip()

        # 无相交或属于题注本身，跳过
        if not b_rect.intersects(crop_rect) or caption_prefix in clean_text:
            continue

        # 安全白名单：若文本块完全位于绘图核心区 (Drawing Hull) 内部，判定为图内标签/图例，绝对不抹除！
        if drawing_hull and (
            drawing_hull.contains(b_rect) or b_rect.y1 < drawing_hull.y1 + 5
        ):
            # 只有当文本水平宽度超过栏宽 80% 且段落行数多时，才判定为侵入正文
            if b_rect.width < (col1_r - 20) * 0.7:
                continue

        # 针对从外部侵入的冗余正文段落执行相交抹白
        if len(clean_text) > 40:
            inter = b_rect & crop_rect
            page.draw_rect(inter, color=(1, 1, 1), fill=(1, 1, 1), overlay=True)

    # 3. 高清渲染与文件落盘
    pix = page.get_pixmap(matrix=fitz.Matrix(zoom, zoom), clip=crop_rect)
    for out_path in output_paths:
        os.makedirs(os.path.dirname(os.path.abspath(out_path)), exist_ok=True)
        pix.save(out_path)

    doc.close()
    return True
```

---

## 3. 多模态视觉自检闭环清单

每张插图导出后，智能体必须调用视觉工具（如 `view_file` 或多模态工具）主动自检：

1. **图表完整性:**
   - 坐标轴（Axes）、刻度标签（Ticks）、单位是否完好无损？
   - 顶端标题与底部题注（Caption）文字是否未被截断？
2. **图内元素存活检测:**
   - 流程图或架构图中的方块文字、数据流箭头、颜色图例（Legend）是否完好保留，没有被意外白块覆盖？
3. **正文杂质检测:**
   - 边缘是否存在相邻栏目的零碎文字字符或上一段落的末尾文字碎片？
4. **迭代修正机制:**
   - 若出现边缘文字渗透：适当缩小裁剪框 2~4pt 或根据检测到的侵入段落坐标微调遮罩；
   - 若图例被截断：主动将裁剪外围向对应方向外扩 6~10pt 后重新运行渲染。
