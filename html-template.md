# HTML & WeChat Typography Specification (自媒体学术纸媒与混合公式排版规范)

本文件作为 [SKILL.md](./SKILL.md) `§5.2` 的执行参考，仅在**博客生成模式**下按需加载。最终输出为包含完整内联样式的 `[文献名].html`，保存至工作目录。

---

## 1. 核心设计准则

- **极简权威学术纸媒风:** 纯白底色（`#ffffff`）、碳黑文字（`#111827`）、无彩色大色块卡片、全篇**绝对严禁出现任何 Emoji 图标**。
- **100% 全内联样式 (Zero External CSS):** 所有样式必须完整写入元素的 `style` 属性中，确保浏览器全选（Ctrl+A / Cmd+A）复制粘贴至微信公众号富文本编辑器（mp.weixin.qq.com）、知乎专栏或飞书文档时无损渲染。
- **微信编辑器强清洗防御体系:**
  - 严禁用 `<div>` 包裹外边框卡片（微信强制解包导致 `border-left` 消失），必须采用微信白名单原生支持的 `<section>` 标签并附带 `box-sizing: border-box;`。
  - 微信编辑器默认对 `<table>` 内所有单元格强加网格线，必须对每个 `<th>`/`<td>` 显式添加全向否定边框属性（`border: none;`）。

---

## 2. 页面全局与结构化排版规范

### 2.1 全局容器与标题
```html
<body style="background-color: #ffffff; margin: 0; padding: 20px; font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, 'PingFang SC', 'Hiragino Sans GB', 'Microsoft YaHei', sans-serif; font-size: 15px; color: #374151; line-height: 1.8; letter-spacing: 0.3px;">
    <div style="max-width: 650px; margin: 0 auto; padding: 20px 10px;">
        <!-- 一级标题 (选用微信高传播力主标题) -->
        <h1 style="font-size: 1.6em; color: #111827; line-height: 1.4; font-weight: bold; margin-bottom: 24px; text-align: left; letter-spacing: 0.5px;">
            ...
        </h1>
    </div>
</body>
```

### 2.2 论文元数据卡片 (微信 `<section>` 兼容容器)
```html
<section style="border-left: 3px solid #111827; padding-left: 14px; margin-top: 16px; margin-bottom: 28px; font-size: 14px; color: #4b5563; box-sizing: border-box;">
    <p style="margin: 6px 0; text-indent: 0; line-height: 1.75;"><strong style="color: #111827;">文章名字：</strong>...</p>
    <p style="margin: 6px 0; text-indent: 0; line-height: 1.75;"><strong style="color: #111827;">作者与机构：</strong>...</p>
    <p style="margin: 6px 0; text-indent: 0; line-height: 1.75;"><strong style="color: #111827;">期刊与会议：</strong>...</p>
    <p style="margin: 6px 0; text-indent: 0; line-height: 1.75;"><strong style="color: #111827;">论文类型：</strong>...</p>
    <p style="margin: 6px 0; text-indent: 0; line-height: 1.75; text-align: justify;"><strong style="color: #111827;">一句话定位：</strong>...</p>
</section>
```

### 2.3 章节标题、正文与数据解读引用栏
- **二级标题 (`<h2>`，带底部分割线):**
  ```html
  <h2 style="font-size: 1.35em; color: #111827; font-weight: bold; border-bottom: 1px solid #111827; padding-bottom: 6px; margin-top: 36px; margin-bottom: 18px; letter-spacing: 0.5px;">
      一、 完整摘要
  </h2>
  ```
- **三级标题 (`<h3>`):**
  ```html
  <h3 style="font-size: 1.1em; color: #111827; font-weight: bold; margin-top: 24px; margin-bottom: 12px;">
      前置概念
  </h3>
  ```
- **学术正文段落 (`<p>`，两端对齐 + 首行缩进 2 字符):**
  ```html
  <p style="text-align: justify; text-indent: 2em; margin: 0 0 16px 0;">
      正文内容...
  </p>
  ```
- **表格数据解读与局限性评估 (`<blockquote>`，粗黑左竖线，无底色):**
  ```html
  <blockquote style="margin: 0 0 24px 0; border-left: 3px solid #111827; padding-left: 16px; color: #4b5563; text-align: justify; font-size: 13px; line-height: 1.6; box-sizing: border-box;">
      <strong style="color: #111827;">数据解读与局限性评估：</strong>客观剖析表格中显露的技术约束、资源开销或性能瓶颈...
  </blockquote>
  ```

### 2.4 极客评分与实战研判排版 (Section 6 模板)
微信推文的价值巅峰与读者互动引擎。包含雷达评分、落地暗礁与终局选型三大模块：
```html
<h2 style="font-size: 1.35em; color: #111827; font-weight: bold; border-bottom: 1px solid #111827; padding-bottom: 6px; margin-top: 36px; margin-bottom: 18px; letter-spacing: 0.5px;">
    六、 极客评分与实战研判
</h2>

<!-- 6.1 三维极客雷达 -->
<h3 style="font-size: 1.1em; color: #111827; font-weight: bold; margin-top: 24px; margin-bottom: 12px;">6.1 三维极客雷达</h3>
<div style="margin-bottom: 14px;">
    <p style="margin: 4px 0; text-indent: 0;"><strong style="color: #111827;">创新性评分 (9.0 / 10)：</strong></p>
    <p style="margin: 4px 0; text-indent: 2em; text-align: justify; color: #4b5563;">彻底颠覆了音频 SSL 领域长久以来的掩码重建架构...</p>
</div>
<div style="margin-bottom: 14px;">
    <p style="margin: 4px 0; text-indent: 0;"><strong style="color: #111827;">实用性评分 (8.5 / 10)：</strong></p>
    <p style="margin: 4px 0; text-indent: 2em; text-align: justify; color: #4b5563;">预训练通过 75% 的超高掩码率实现了极高加速...</p>
</div>
<div style="margin-bottom: 14px;">
    <p style="margin: 4px 0; text-indent: 0;"><strong style="color: #111827;">行业价值评分 (9.0 / 10)：</strong></p>
    <p style="margin: 4px 0; text-indent: 2em; text-align: justify; color: #4b5563;">开创了统一语言、视觉、语音和通用非言语音频预训练格式的先河...</p>
</div>

<!-- 6.2 落地暗礁与避坑指南 (Section 兼容框) -->
<h3 style="font-size: 1.1em; color: #111827; font-weight: bold; margin-top: 24px; margin-bottom: 12px;">6.2 落地暗礁与避坑指南</h3>
<section style="border: 1px solid #e5e7eb; border-left: 3px solid #111827; padding: 14px; margin-bottom: 20px; font-size: 14px; color: #4b5563; box-sizing: border-box; background-color: #fafafa;">
    <p style="margin: 6px 0; text-indent: 0; line-height: 1.7;"><strong style="color: #111827;">算力与显存账本：</strong>预训练需要多次交替循环（多阶段 400K 步），需 8~16 张高性能 GPU，中小团队几乎无法从零复现，建议直接调用开源预训练权重微调。</p>
    <p style="margin: 6px 0; text-indent: 0; line-height: 1.7;"><strong style="color: #111827;">工业部署与延迟边界：</strong>ViT-Base 90M 单模型推理仅需几十毫秒，但 10 模型集成在强实时、低算力边缘端不可行，线上业务推荐单模型部署。</p>
    <p style="margin: 6px 0; text-indent: 0; line-height: 1.7;"><strong style="color: #111827;">论文未言之隐：</strong>纯无监督自蒸馏存在明显性能瓶颈，最终突破高度依赖有监督教师模型（BEATs_iter3+），并非“纯粹无监督”的奇迹。</p>
</section>

<!-- 6.3 号主终局研判 -->
<h3 style="font-size: 1.1em; color: #111827; font-weight: bold; margin-top: 24px; margin-bottom: 12px;">6.3 号主终局研判</h3>
<blockquote style="margin: 0 0 24px 0; border-left: 3px solid #111827; padding-left: 16px; color: #111827; text-align: justify; font-size: 14px; line-height: 1.7; box-sizing: border-box; font-weight: 500;">
    <strong>技术定性与选型建议：</strong>BEATs 是通用音频迈向多模态离散大一统的里程碑方案，而非过渡期补丁。做多模态理解、音频分类、长音频大模型底座的团队建议<strong>立即跟进其 Tokenizer 机制</strong>；但如果是极端超低延迟边缘唤醒（<10ms）场景，应继续沿用轻量化 CNN，坚决不要盲目上 ViT。
</blockquote>

---

## 3. 混合数学公式渲染引擎 (Hybrid Dual-Engine Architecture)

微信富文本编辑器原生不支持 MathJax/KaTeX 脚本执行。为了兼顾“可编辑性/零图复制”与“复杂公式高精排版”，采用**两级分级渲染策略**：

### 3.1 Tier 1 (轻量常规公式：原生 HTML 语义排版)
适用于行内变量、简单分式、加总、极限、Argmin 及常规方程式。排版要素：
- **公式块容器 (`<p>` + 右浮动编号):**
  ```html
  <p style="text-align: center; margin: 16px 0; font-family: 'Times New Roman', Times, serif; font-size: 1.15em; color: #111827; line-height: 1.8; padding: 4px 0; border: none;">
      <span style="float: right; color: #6b7280; font-size: 0.85em; font-family: sans-serif; font-weight: normal; margin-top: 2px;">(1)</span>
      公式主体
  </p>
  ```
- **上下垂直分式 (纯 CSS 分数线):**
  ```html
  <span style="display: inline-block; vertical-align: middle; text-align: center; margin: 0 2px;">
      <span style="display: block; border-bottom: 1px solid #111827; padding: 0 4px; font-size: 0.85em; line-height: 1.2;">分子</span>
      <span style="display: block; padding: 0 4px; font-size: 0.85em; line-height: 1.2;">分母</span>
  </span>
  ```
- **求和 / 乘积 / 算子垂直堆叠:**
  ```html
  <span style="display: inline-block; vertical-align: middle; text-align: center; margin: 0 4px;">
      <span style="display: block; font-size: 0.7em; line-height: 1.0; margin-bottom: -1px;">上限</span>
      <span style="display: block; font-size: 1.3em; line-height: 1.0; font-family: 'Times New Roman', Times, serif;">&sum;</span>
      <span style="display: block; font-size: 0.7em; line-height: 1.0; margin-top: -1px;"><i>t</i>=1</span>
  </span>
  ```
- **根号 (带上划横线):**
  ```html
  &radic;<span style="border-top: 1px solid #111827; padding-top: 1px; margin-left: -2px;">( <i>x</i> + <i>y</i> )</span>
  ```

### 3.2 Tier 2 (高维复杂公式：无外部依赖的离线 Mathtext 渲染)
当遇到**多维矩阵 (`bmatrix`)、多行条件分支方程组 (`cases`)、复杂张量网络或复杂多重括号**时，纯 HTML `<span>` 会出现排版错位。
- **解法:** 利用 Python 标准科学计算栈内置的 `matplotlib.mathtext`（**无需在操作系统安装数百兆的 TeXLive 发行版**），将其离线渲染为 300 DPI、背景透明的 Base64 PNG 并行内居中嵌入。

```python
import base64
import io
import matplotlib
import matplotlib.pyplot as plt

matplotlib.use("Agg")


def render_latex_to_base64_png(latex_math: str, dpi: int = 300) -> str:
    """将复杂 LaTeX 方程渲染为透明背景的高清 Base64 PNG。

    latex_math 示例: r"$\begin{bmatrix} a & b \\ c & d \end{bmatrix}$"
    """
    fig = plt.figure(figsize=(0.01, 0.01))
    fig.patch.set_alpha(0.0)
    # 使用 matplotlib 内置 mathtext 解析器
    text = fig.text(
        0, 0, latex_math, fontsize=14, color="#111827", usetex=False, va="bottom"
    )

    buf = io.BytesIO()
    # 紧凑裁剪边界并以高分辨率导出
    fig.savefig(buf, format="png", dpi=dpi, transparent=True, bbox_inches="tight", pad_inches=0.05)
    plt.close(fig)

    encoded = base64.b64encode(buf.getvalue()).decode("ascii")
    return f"data:image/png;base64,{encoded}"
```

- **HTML 嵌入结构:**
  ```html
  <p style="text-align: center; margin: 18px 0; border: none;">
      <span style="float: right; color: #6b7280; font-size: 0.85em; font-family: sans-serif; font-weight: normal; margin-top: 6px;">(2)</span>
      <img src="data:image/png;base64,..." alt="Formula (2)" style="max-height: 65px; vertical-align: middle; display: inline-block;">
  </p>
  ```

---

## 4. 学术三线表与微信网格线免疫体系

微信富文本编辑器对所有表格的默认策略是强制显示四周灰框。必须通过**外层横向滚动条 + 单元格全向否定样式**实现纯正的三线表（Booktabs）：

```html
<!-- 表题 -->
<p style="font-size: 13px; font-weight: bold; color: #111827; margin: 18px 0 8px 0; text-indent: 0;">表 1：模型性能定量对比</p>

<!-- 移动端横向自适应滚动容器 -->
<div style="overflow-x: auto; -webkit-overflow-scrolling: touch; margin: 0 0 14px 0;">
    <table style="width: 100%; border-collapse: collapse; font-size: 12px; color: #374151; font-family: -apple-system, sans-serif; text-align: left; border-top: 2px solid #111827; border-bottom: 2px solid #111827; min-width: 580px; border-left: none; border-right: none;">
        <thead>
            <tr style="border-bottom: 1px solid #111827;">
                <th style="padding: 9px 8px; font-weight: bold; color: #111827; border: none; border-left: none; border-right: none; border-top: none; border-bottom: 1px solid #111827;">模型</th>
                <th style="padding: 9px 8px; font-weight: bold; color: #111827; text-align: center; border: none; border-left: none; border-right: none; border-top: none; border-bottom: 1px solid #111827;">参数量</th>
                <th style="padding: 9px 8px; font-weight: bold; color: #111827; text-align: center; border: none; border-left: none; border-right: none; border-top: none; border-bottom: 1px solid #111827;">准确率 (%)</th>
            </tr>
        </thead>
        <tbody>
            <tr style="border-bottom: 1px solid #f3f4f6;">
                <td style="padding: 7px 8px; border: none; border-left: none; border-right: none; border-top: none; border-bottom: none;">Baseline</td>
                <td style="padding: 7px 8px; text-align: center; border: none; border-left: none; border-right: none; border-top: none; border-bottom: none;">86M</td>
                <td style="padding: 7px 8px; text-align: center; border: none; border-left: none; border-right: none; border-top: none; border-bottom: none;">48.2</td>
            </tr>
            <tr style="border-bottom: 1px solid #f3f4f6;">
                <td style="padding: 7px 8px; border: none; border-left: none; border-right: none; border-top: none; border-bottom: none;">Ours</td>
                <td style="padding: 7px 8px; text-align: center; border: none; border-left: none; border-right: none; border-top: none; border-bottom: none;">90M</td>
                <td style="padding: 7px 8px; text-align: center; border: none; border-left: none; border-right: none; border-top: none; border-bottom: none;"><strong>50.6</strong></td>
            </tr>
        </tbody>
    </table>
</div>

<!-- 紧随表格的客观解读与局限性评估 -->
<blockquote style="margin: 0 0 24px 0; border-left: 3px solid #111827; padding-left: 16px; color: #4b5563; text-align: justify; font-size: 13px; line-height: 1.6; box-sizing: border-box;">
    <strong style="color: #111827;">数据解读与局限性评估：</strong>Ours 在 AS-2M 上超越前代 baseline 2.4 个点，但在轻量化极端边缘场景下推理延迟稍高。
</blockquote>
```

---

## 5. Token 保护与 Base64 自动注入脚本

严禁大模型在聊天输出或直接编写中输出庞大的 Base64 字符！
**规范执行流向:**
1. 大模型在生成 `[文献名].html` 初稿时，插图 `<img>` 的 `src` 统一填写本地相对路径（如 `./figure/figure_1.png`）。
2. 调用下列轻量 Python 脚本，自动扫描 HTML 中的所有本地图片路径，完成 Base64 编码并替换回写入最终 HTML 文件。

```python
import base64
import os
import re
import sys

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")


def inject_base64_images_into_html(
    html_path: str, base_dir: str = "."
) -> None:
    """将 HTML 中引用的本地插图路径替换为内联 Base64 Data URI。"""
    with open(html_path, "r", encoding="utf-8") as f:
        content = f.read()

    def replace_img_src(match: re.Match) -> str:
        src = match.group(1)
        if src.startswith("data:") or src.startswith("http"):
            return match.group(0)

        img_path = os.path.normpath(os.path.join(base_dir, src))
        if not os.path.exists(img_path):
            print(f"[Warning] Image not found: {img_path}")
            return match.group(0)

        ext = os.path.splitext(img_path)[1].lower().replace(".", "")
        mime = "image/png" if ext == "png" else "image/jpeg"
        with open(img_path, "rb") as img_f:
            b64_data = base64.b64encode(img_f.read()).decode("ascii")

        return f'src="data:{mime};base64,{b64_data}"'

    new_content = re.sub(r'src=["\']([^"\']+\.(?:png|jpg|jpeg|webp))["\']', replace_img_src, content)

    with open(html_path, "w", encoding="utf-8") as f:
        f.write(new_content)
    print(f"[Success] Base64 images injected into {html_path}")


if __name__ == "__main__":
    if len(sys.argv) > 1:
        inject_base64_images_into_html(sys.argv[1])
```
