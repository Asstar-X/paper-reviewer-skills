# 微信公众号自媒体极简排版与内联样式指南

> 本指南用于规范 `project-reader` 生成可直接一键全选复制至微信公众平台（mp.weixin.qq.com）的高颜值、简约纸媒风 HTML 文件。

---

## 1. 核心视觉美学与设计原则

- **风格定位：** 现代化极简科技风（参考“数字生命卡兹克”、少数派、海外 Substack 优质专栏质感），克制、干净、呼吸感强。
- **100% 全内联样式 (Zero External CSS)：** 所有样式必须完整写入 HTML 元素的 `style` 属性中，确保在浏览器中全选（`Ctrl+A`）并粘贴到微信富文本编辑器时样式零损耗。
- **排版呼吸感（手机端黄金法则）：**
  - **单段中文不超过 1~3 行**（约 60~100 字），坚决杜绝大段密集文字给读者带来的窒息压迫感。
  - 行高（`line-height`）统一采用 `1.85`，字间距 `0.3px`，字号 `16px`。
  - 正文字色采用碳黑（`#2d3748`），比纯黑 `#000000` 更柔和耐看。
  - 背景色采用纯白（`#ffffff`），搭配极淡灰色浅色边框卡片。

---

## 2. 微信编辑器防清洗核心组件库

微信富文本编辑器对 `<div>` 标签具有自动解包和剥离样式的特性，因此所有卡片容器**一律采用微信白名单原生支持的 `<section>` 标签**，并声明 `box-sizing: border-box;`。

### 2.1 顶部发文自选工具箱 (虚线卡片)
```html
<section style="border: 1px dashed #cbd5e1; background-color: #f8fafc; border-radius: 8px; padding: 16px; margin-bottom: 28px; font-size: 13.5px; color: #475569; line-height: 1.7; box-sizing: border-box;">
  <p style="margin: 0 0 8px 0; font-weight: bold; color: #0f172a; font-size: 14px;">💡 微信发文备选标题库：</p>
  <p style="margin: 3px 0;"><strong>【亲历故事向】：</strong>...</p>
  <p style="margin: 3px 0;"><strong>【痛点好奇向】：</strong>...</p>
  <p style="margin: 3px 0;"><strong>【干货实战向】：</strong>...</p>
  <p style="margin: 8px 0 0 0; color: #64748b; font-size: 12px; border-top: 1px dashed #e2e8f0; padding-top: 6px;">
    🖼️ <strong>封面设计构想 (2.35:1)：</strong>...
  </p>
</section>
```

### 2.2 一句话说人话（左侧蓝边卡片）
```html
<section style="margin: 24px 0; padding: 18px 20px; background-color: #f8fafc; border-left: 4px solid #2563eb; border-radius: 6px; box-sizing: border-box;">
  <p style="margin: 0 0 8px 0; font-size: 16px; font-weight: bold; color: #0f172a;">一句话说人话：它到底干了啥？</p>
  <p style="margin: 0; font-size: 15px; line-height: 1.8; color: #334155;">...</p>
</section>
```

### 2.3 补充背景小卡片
```html
<section style="margin: 18px 0; padding: 14px 16px; background-color: #f1f5f9; border-radius: 6px; font-size: 14px; color: #475569; line-height: 1.75; box-sizing: border-box;">
  <p style="margin: 0;"><strong style="color: #0f172a;">【补充背景·...】</strong><br>...</p>
</section>
```

### 2.4 真实终端命令代码框
```html
<section style="margin: 18px 0; background-color: #1e293b; border-radius: 8px; padding: 16px 18px; overflow-x: auto; color: #f8fafc; font-family: Consolas, Monaco, monospace; font-size: 14px; line-height: 1.75; box-sizing: border-box;">
  <span style="color: #94a3b8;"># 注释说明</span><br>
  <span style="color: #38bdf8;">真实核实过的运行指令</span>
</section>
```

### 2.5 真实链接兜底卡片（无简易指令时使用，绝不胡编）
```html
<section style="margin: 18px 0; background-color: #f8fafc; border: 1px solid #e2e8f0; border-radius: 8px; padding: 16px 18px; font-size: 14.5px; line-height: 1.8; box-sizing: border-box;">
  <p style="margin: 0 0 8px 0;"><strong>官方体验途径说明：</strong>...</p>
  <div style="margin-top: 10px; padding-top: 8px; border-top: 1px dashed #cbd5e1; font-size: 13.5px; color: #475569;">
    🔗 <strong>官方主页：</strong><code>...</code>
  </div>
</section>
```

---

## 3. 证据优先（Evidence-First）排版铁律

1. **若网页有明确 CLI：** 提炼最核心的 1~2 步写入极简终端框。
2. **若网页无命令行（纯在线 Demo 或复杂源码）：** 坚决不伪造虚假命令，直接采用上述“真实链接兜底卡片”，将官方项目主页、在线 Demo 真实呈现给读者。
