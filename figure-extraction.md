# Figure Extraction Specification (高精插图提取与遮罩规范)

本文件作为 [SKILL.md](./SKILL.md) `§5.1` 的执行参考，仅在**博客生成模式**或用户要求带图解析时按需加载。

## 1. 核心规范
1. **高解析度导出:** 使用 `pymupdf`（`fitz`），渲染倍率不得低于 `3.0x`（`fitz.Matrix(3.0, 3.0)`），确保视网膜屏幕及微信公众号清晰无锯齿。
2. **动态定位计算:** 严禁硬编码裁剪坐标。必须通过 `page.search_for("Figure X:")` / `page.search_for("Fig. X")` 定位题注锚点，结合 `page.get_drawings()`、`page.get_images()` 与图表内部短标签 `page.get_text("blocks")`，动态计算完整包裹目标图表的 `fitz.Rect`。
3. **内存白底遮罩 (White-out Masking):** 在调用 `page.get_pixmap()` 前，直接在内存中的 `page` 对象上绘制纯白填充矩形（不保存修改回原 PDF），阻断无关字符渗透：
   - **双栏文字防溢出:** 当图表位于左栏（`bbox.x1 <= W * 0.52`）时，向右栏 `[W / 2 + 5, 0, W, H]` 绘白；位于右栏（`bbox.x0 >= W * 0.48`）时，向左栏 `[0, 0, W / 2 - 5, H]` 绘白；跨双栏通栏大图则跳过左右栏遮罩。
   - **上下正文漏入遮罩:** 遍历 `page.get_text("blocks")`，筛选出字符数较多（如 `len(text.strip()) > 40`）且并非目标图题注（不包含 `Figure X` / `Fig. X`）的正文文本块；若其坐标与拓展后的裁剪框相交，对相交区域绘制白底矩形遮罩。
4. **输出路径双写:** 导出后的 `.png` 图片需同时保存至用户当前工作目录（如 `./figure/figure_x.png`）和系统 Artifacts 目录（若当前环境提供）。

## 2. 脚本参考模板 (Windows UTF-8 Safe)

```python
import os
import sys
import fitz

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")


def mask_and_crop_figure(
    pdf_path: str,
    page_num: int,
    crop_rect: fitz.Rect,
    output_paths: list[str],
    column_mode: str = "full",  # "left", "right", or "full"
    caption_keywords: tuple[str, ...] = (),
    zoom: float = 3.0,
) -> None:
    """在内存中遮罩无关正文并高分辨率裁剪指定页面的插图。"""
    doc = fitz.open(pdf_path)
    page = doc[page_num]
    W, H = page.rect.width, page.rect.height

    # 1. 双栏文献防跨栏文字渗入遮罩
    if column_mode == "left":
        page.draw_rect(fitz.Rect(W / 2 + 5, 0, W, H), color=(1, 1, 1), fill=(1, 1, 1), overlay=True)
    elif column_mode == "right":
        page.draw_rect(fitz.Rect(0, 0, W / 2 - 5, H), color=(1, 1, 1), fill=(1, 1, 1), overlay=True)

    # 2. 上下无关长正文文本块遮罩
    for block in page.get_text("blocks"):
        x0, y0, x1, y1, text, *_ = block
        clean_text = text.strip()
        block_rect = fitz.Rect(x0, y0, x1, y1)
        if not block_rect.intersects(crop_rect):
            continue
        if len(clean_text) > 40 and not any(kw in clean_text for kw in caption_keywords):
            inter = block_rect & crop_rect
            page.draw_rect(inter, color=(1, 1, 1), fill=(1, 1, 1), overlay=True)

    # 3. 高清渲染并保存
    pix = page.get_pixmap(matrix=fitz.Matrix(zoom, zoom), clip=crop_rect)
    for out_path in output_paths:
        os.makedirs(os.path.dirname(os.path.abspath(out_path)), exist_ok=True)
        pix.save(out_path)
    doc.close()
```

> **提示:** 在调用 `mask_and_crop_figure` 前，先用脚本检索 `page.search_for("Figure X")`、`page.get_drawings()` 和 `page.get_images()` 的实际边界坐标动态算出 `crop_rect`（注意给上下左右留出约 `4~8pt` 的安全边距，避免切掉坐标轴刻度或图例边框）。

## 3. 视觉校验闭环 (强制步骤)
每张插图生成后，必须立即执行以下闭环校验：
1. **调用视觉工具检查:** 主动使用 `view_file`（或当前运行环境的图像读取工具）直接查看导出的 `.png` 文件。
2. **核查清单:**
   - 图表边缘、箭头、坐标轴标签、公式角标是否完整无截断？
   - 是否存在跨栏文字、正文段落或题注碎片漏入？
   - 若包含子图 `(a)` `(b)` `(c)`，所有子图与子标签是否均被完整纳入？
3. **迭代修正:** 只要视觉反馈存在任何瑕疵，必须微调 `crop_rect` 边距或调整正文遮罩过滤条件后重新渲染，直到图片 100% 干净精准为止。
