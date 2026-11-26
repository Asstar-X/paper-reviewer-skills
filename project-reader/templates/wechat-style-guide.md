# 微信公众号 Apple 极简风排版与内联样式指南

> 本指南用于规范 `project-reader` 生成可直接一键全选复制至微信公众平台（mp.weixin.qq.com）的 **Apple 极简风（纯黑白灰 + 克制留白 + 细线分割）** HTML 文件。

---

## 1. 核心视觉美学与设计原则

- **风格定位：** Apple Newsroom / Apple Developer 文档级的克制极简美学——**只用纯白、Apple 浅灰（`#f5f5f7`）、深墨黑（`#1d1d1f`）与中性灰（`#6e6e73`）**，通过字号、字重、留白与 1px 细线建立高级层次感。
- **反“AI 味”禁令（严格执行）：**
  - **严禁五颜六色：** 禁止使用蓝色左竖线、黄色/琥珀色警示底框、彩色表格列填充、彩色小圆点、彩色标签胶囊。
  - **严禁多余装饰：** 禁止在正文标题或卡片前堆砌 Emoji（如 💡、🖼️、🔗、🎧、▪），禁止 macOS 红黄绿三圆点代码块顶栏，禁止在 `<h1>` 下方加彩色短横线。
- **100% 全内联样式 (Zero External CSS)：** 所有样式必须完整写入 HTML 元素的 `style` 属性中，确保浏览器全选（`Ctrl+A`）复制进微信编辑器格式零损耗。
- **移动端呼吸感：**
  - 单段中文不超过 1~3 行（约 60~100 字），段落间距 `18px`，章节前留白 `38px`。
  - 正文采用 `#1d1d1f`（Apple 深墨黑），行高 `1.85`，字间距 `0.2px`，字号 `16px`。
  - 行内代码 `<code>` 统一采用低饱和度 Apple 浅灰底：`background-color: #f5f5f7; color: #1d1d1f; padding: 2px 6px; border-radius: 4px; font-family: 'SF Mono', Consolas, Monaco, monospace; font-size: 13.5px;`。

---

## 2. 微信编辑器防清洗核心组件库

所有卡片容器**一律采用微信白名单原生支持的 `<section>` 标签**，并声明 `box-sizing: border-box;`。

### 2.1 顶部发文自选工具箱（克制灰底细框）
```html
<section style="border: 1px solid #e5e5ea; background-color: #f5f5f7; border-radius: 12px; padding: 16px 20px; margin-bottom: 32px; font-size: 13.5px; color: #424245; line-height: 1.75; box-sizing: border-box;">
  <p style="margin: 0 0 8px 0; font-weight: 600; color: #1d1d1f; font-size: 13.5px;">发文备选标题与封面参考</p>
  <p style="margin: 4px 0;"><strong style="color: #1d1d1f;">亲历故事向：</strong>...</p>
  <p style="margin: 4px 0;"><strong style="color: #1d1d1f;">痛点好奇向：</strong>...</p>
  <p style="margin: 4px 0;"><strong style="color: #1d1d1f;">干货实战向：</strong>...</p>
  <p style="margin: 10px 0 0 0; color: #6e6e73; font-size: 12.5px; border-top: 1px solid #e5e5ea; padding-top: 8px;">
    封面构想 (2.35:1)：...
  </p>
</section>
```

### 2.2 文章大标题（纯排版张力，无多余线条）
```html
<h1 style="font-size: 24px; color: #1d1d1f; line-height: 1.38; font-weight: 700; margin: 0 0 28px 0; text-align: left; letter-spacing: -0.3px;">...</h1>
```

### 2.3 一句话说人话（Apple `#f5f5f7` 极简卡片）
```html
<section style="margin: 28px 0; padding: 20px 22px; background-color: #f5f5f7; border-radius: 12px; box-sizing: border-box;">
  <p style="margin: 0 0 10px 0; font-size: 15px; font-weight: 600; color: #1d1d1f;">一句话说人话：它到底干了啥？</p>
  <p style="margin: 0 0 14px 0; font-size: 15px; line-height: 1.8; color: #1d1d1f;">...</p>
  <section style="border-top: 1px solid #e5e5ea; padding-top: 12px; font-size: 14.5px; line-height: 1.8; color: #424245; box-sizing: border-box;">
    <p style="margin: 0 0 6px 0;"><strong style="color: #1d1d1f;">1. 干货点一：</strong>...</p>
    <p style="margin: 0 0 6px 0;"><strong style="color: #1d1d1f;">2. 干货点二：</strong>...</p>
    <p style="margin: 0;"><strong style="color: #1d1d1f;">3. 干货点三：</strong>...</p>
  </section>
</section>
```

### 2.4 补充背景小卡片（极简左细灰线引用，无彩色胶囊）
```html
<section style="margin: 22px 0; padding: 14px 18px; border-left: 2px solid #d2d2d7; font-size: 14.5px; color: #6e6e73; line-height: 1.8; box-sizing: border-box;">
  <p style="margin: 0 0 4px 0; font-weight: 600; color: #1d1d1f;">补充背景 · 术语说明</p>
  <p style="margin: 0;">...</p>
</section>
```

### 2.5 代码框（Apple Developer 浅灰单色极简风格，无三色圆点）
```html
<section style="margin: 22px 0; background-color: #f5f5f7; border: 1px solid #e5e5ea; border-radius: 10px; padding: 16px 18px; overflow-x: auto; color: #1d1d1f; font-family: 'SF Mono', Consolas, Monaco, monospace; font-size: 13.5px; line-height: 1.75; box-sizing: border-box;">
  <span style="color: #6e6e73;"># 注释说明</span><br>
  <span style="color: #1d1d1f; font-weight: 600;">真实核实过的运行指令</span>
</section>
```

### 2.6 真实链接兜底卡片（克制单色框）
```html
<section style="margin: 22px 0; background-color: #f5f5f7; border-radius: 10px; padding: 16px 20px; font-size: 14.5px; line-height: 1.8; box-sizing: border-box;">
  <p style="margin: 0 0 10px 0; color: #424245;"><strong style="color: #1d1d1f;">官方体验与授权说明：</strong>...</p>
  <section style="padding-top: 10px; border-top: 1px solid #e5e5ea; font-size: 13.5px; color: #6e6e73; box-sizing: border-box;">
    <p style="margin: 0 0 4px 0;"><strong style="color: #1d1d1f;">模型主页：</strong><span style="font-family: 'SF Mono', Consolas, Monaco, monospace; font-size: 13px; color: #0066cc; word-break: break-all;">...</span></p>
  </section>
</section>
```

### 2.7 正文二级标题 (`<h2>`) 与「泼点冷水」规范

正文所有二级标题保持统一的纯黑极简字体排版（`margin: 38px 0 16px 0; padding-bottom: 8px; border-bottom: 1px solid #e5e5ea;`），**不加彩色竖标**。局限性章节**固定只显示 `泼点冷水`**，分条局限用干干净净的细线段落或浅灰文字层级展示，**严禁使用黄色警告框**：

```html
<!-- 常规章节标题 & 泼点冷水固定标题 -->
<h2 style="font-size: 19px; color: #1d1d1f; font-weight: 700; margin: 38px 0 16px 0; padding-bottom: 8px; border-bottom: 1px solid #e5e5ea; line-height: 1.35; letter-spacing: -0.2px;">泼点冷水</h2>

<p style="margin: 0 0 18px 0;"><strong style="color: #1d1d1f;">第一，核心局限。</strong>具体说明...</p>
```

### 2.8 极简数据对比表（纯黑白灰 + 细线，无彩色背景）
```html
<section style="margin: 22px 0; overflow-x: auto; box-sizing: border-box;">
  <table style="width: 100%; border-collapse: collapse; font-size: 13.5px; color: #424245; text-align: left; min-width: 440px;">
    <thead>
      <tr style="border-bottom: 1.5px solid #1d1d1f;">
        <th style="padding: 10px 10px; font-weight: 600; color: #1d1d1f; border: none;">数据集</th>
        <th style="padding: 10px 10px; font-weight: 500; color: #6e6e73; text-align: center; border: none;">旧版</th>
        <th style="padding: 10px 10px; font-weight: 700; color: #1d1d1f; text-align: center; border: none;">新版</th>
      </tr>
    </thead>
    <tbody>
      <tr style="border-bottom: 1px solid #e5e5ea;">
        <td style="padding: 10px 10px; font-weight: 500; color: #1d1d1f; border: none;">Dataset</td>
        <td style="padding: 10px 10px; text-align: center; color: #6e6e73; border: none;">24.5</td>
        <td style="padding: 10px 10px; text-align: center; font-weight: 700; color: #1d1d1f; border: none;">20.3</td>
      </tr>
    </tbody>
  </table>
</section>
```

### 2.9 结尾收束规范（禁加小标题）

结尾点评段落直接顺接正文自然收束，**不要添加 `<h2>最后聊两句</h2>` 等小标题**，结尾段使用 `margin: 30px 0 28px 0;` 与前文拉开呼吸间距即可。

### 2.10 音视频展示卡片（网站含真实音频/视频时使用，支持直接复制进公众号）

由于微信公众号编辑器会强制清洗外部 `<audio>`、`<video>` 与 `<iframe>` 标签，**严禁直接输出 `<audio>`/`<video>` 标签**；改为使用 Apple `#f5f5f7` 卡片 + **Base64 内联单色声波预览图/视频封面 `<img>`** + 试听链接与本地 `./media/` 文件对照提示（由 `scripts/extract_media.py` 自动抓取生成）。浏览器全选复制进微信后台后排版与图片 100% 保留；若需在公众号内直接点击播放，发布前用微信编辑器「音频/视频」按钮上传对应本地文件即可：

```html
<section style="margin: 22px 0; padding: 18px 20px; background-color: #f5f5f7; border-radius: 12px; box-sizing: border-box;">
  <p style="margin: 0 0 6px 0; font-size: 15px; font-weight: 600; color: #1d1d1f;">实测音频对比（输入 vs 输出）</p>
  <p style="margin: 0 0 10px 0; font-size: 14px; color: #6e6e73; line-height: 1.7;">示例说明（如：16kHz 单声道输入，时长 4.2s）</p>
  <img src="./media/01_sample_waveform.png" alt="音频声波预览" style="width: 100%; height: auto; display: block; border-radius: 6px; margin: 10px 0;">
  <p style="margin: 8px 0 0 0; font-size: 13px; color: #6e6e73; line-height: 1.65;">
    已保存至本地 <code style="background-color: #e5e5ea; color: #1d1d1f; padding: 2px 6px; border-radius: 4px; font-family: 'SF Mono', Consolas, Monaco, monospace; font-size: 12.5px;">./media/01_sample.wav</code>（如需在公众号内嵌播放，可在微信编辑器点击「音频」上传该文件）
  </p>
</section>
```

---

## 3. 证据优先（Evidence-First）排版铁律

1. **若网页有明确 CLI：** 提炼最核心的 1~2 步写入极简浅灰代码框。
2. **若网页无命令行（纯在线 Demo 或复杂源码）：** 坚决不伪造虚假命令，直接采用上述“真实链接兜底卡片”，将官方项目主页、在线 Demo 真实呈现给读者。
