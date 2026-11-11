# HTML & WeChat Typography Specification (自媒体学术纸媒排版规范)

本文件作为 [SKILL.md](./SKILL.md) `§5.2` 的执行参考，仅在**博客生成模式**下按需加载。输出文件名为 `[文献名].html`，保存至用户当前工作目录。

## 1. 设计准则
- **极简权威学术纸媒风:** 拒绝任何彩色背景卡片、圆角阴影装饰及“AI 生成感”样式；全篇标题、正文、元信息、列表和表格内部**严禁出现任何 Emoji 图标**。
- **全内联 CSS:** 所有样式必须写入元素的 `style` 属性，确保浏览器全选复制粘贴至微信公众号编辑器（mp.weixin.qq.com）或知乎时 100% 保留渲染。

## 2. 页面与段落样式模板

- **页面全局容器:**
  ```html
  <body style="background-color: #ffffff; margin: 0; padding: 20px; font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Helvetica, Arial, sans-serif; font-size: 15px; color: #374151; line-height: 1.8; letter-spacing: 0.3px;">
      <div style="max-width: 650px; margin: 0 auto; padding: 20px 10px;">
          <!-- 文章内容 -->
      </div>
  </body>
  ```
- **一级标题 (`<h1>`，直接复用锐评标题):**
  ```html
  <h1 style="font-size: 1.6em; color: #111827; line-height: 1.4; font-weight: bold; margin-bottom: 24px; text-align: left; letter-spacing: 0.5px;">...</h1>
  ```
- **论文基本信息卡片 (左侧粗黑实线，无背景、无圆角):**
  ```html
  <div style="border-left: 3px solid #111827; padding-left: 16px; margin-bottom: 30px; font-size: 14px; color: #4b5563;">
      <p style="margin: 4px 0; text-indent: 0;"><strong>文章名字：</strong>...</p>
  </div>
  ```
- **二级标题 (`<h2>`，底部分割线):**
  ```html
  <h2 style="font-size: 1.35em; color: #111827; font-weight: bold; border-bottom: 1px solid #111827; padding-bottom: 6px; margin-top: 36px; margin-bottom: 18px; letter-spacing: 0.5px;">...</h2>
  ```
- **三级标题 (`<h3>`):**
  ```html
  <h3 style="font-size: 1.1em; color: #111827; font-weight: bold; margin-top: 24px; margin-bottom: 12px;">...</h3>
  ```
- **学术正文段落 (`<p>`，两端对齐 + 首行缩进 2 字符):**
  ```html
  <p style="text-align: justify; text-indent: 2em; margin: 0 0 16px 0;">...</p>
  ```
- **引用栏 / 表格数据解读与局限性评估 (`<blockquote>`，左侧粗黑竖线，无背景):**
  ```html
  <blockquote style="margin: 0 0 24px 0; border-left: 3px solid #111827; padding-left: 16px; color: #4b5563; text-align: justify; font-size: 13px; line-height: 1.6;">
      <strong>数据解读与局限性评估：</strong>...
  </blockquote>
  ```

## 3. 图片排版与 Base64 嵌入规范
- **图片容器与图注:**
  ```html
  <div style="text-align: center; margin: 24px 0;">
      <img src="data:image/png;base64,..." alt="Figure X" style="max-width: 100%; height: auto; display: block; margin: 0 auto 10px;">
      <p style="text-align: center; text-indent: 0; font-size: 13px; color: #6b7280; margin: 0; padding: 0 10px; line-height: 1.4;">图 X：...</p>
  </div>
  ```
- **Token 安全注入策略:** 为了保证微信公众号整页全选复制时图片可连同正文一并无损上传，最终 HTML 中的 `<img>` `src` 必须为 Base64 Data URI。**严禁由模型手写超长 Base64 字符串**——应先在 HTML 中填入占位符（如 `./figure/figure_1.png`），随后运行简短的 Python 脚本（UTF-8 编码）将本地 PNG 转码并替换写入最终 `[文献名].html`。

## 4. 学术三线表与微信防框线规范
微信公众号编辑器默认会对表格所有单元格强制渲染灰色网格线。必须通过**外层滚动容器 + 显式否定边框属性**彻底规避：

- **表题:** `<p style="font-size: 13px; font-weight: bold; color: #111827; margin: 16px 0 8px 0; text-indent: 0;">表 X：...</p>`
- **移动端横向滚动包装:** `<div style="overflow-x: auto; -webkit-overflow-scrolling: touch; margin: 0 0 12px 0;">`
- **三线表 `<table ...>`:**
  ```html
  <table style="width: 100%; border-collapse: collapse; font-size: 12px; color: #374151; font-family: sans-serif; text-align: left; border-top: 2px solid #111827; border-bottom: 2px solid #111827; min-width: 600px;">
      <thead>
          <tr>
              <th style="padding: 10px 8px; font-weight: bold; color: #111827; border: none; border-left: none; border-right: none; border-top: none; border-bottom: 1px solid #111827;">Col</th>
          </tr>
      </thead>
      <tbody>
          <tr style="border-bottom: 1px solid #f3f4f6;">
              <td style="padding: 6px 8px; border: none; border-left: none; border-right: none; border-top: none; border-bottom: none;">Val</td>
          </tr>
      </tbody>
  </table>
  ```
- **定量表格全覆盖要求:** 论文中的 `Table 1 ~ Table X` 须全部输出，每张表格紧接 `<blockquote>` 数据解读与局限性评估。

## 5. 数学公式无损原生排版规范
严禁在生成的 HTML 中暴露 `$`、`$$` 或 `\frac`、`\sum`、`\sigma` 等原始 LaTeX 源码；**严禁使用 `<table>` 包装公式或公式编号**。所有公式一律转化为原生 HTML 结构：

1. **无框线块级公式容器 (`<p>` + 右浮动编号):**
   编号置于 `<p>` 开头并右浮动，实现公式视觉居中且编号右对齐：
   ```html
   <p style="text-align: center; margin: 16px 0; font-family: 'Times New Roman', Times, serif; font-size: 1.15em; color: #111827; line-height: 1.8; padding: 4px 0; border: none;"><span style="float: right; color: #6b7280; font-size: 0.85em; font-family: sans-serif; font-weight: normal; margin-top: 2px;">(1)</span>...公式主体...</p>
   ```

2. **垂直分式 (分数线):**
   ```html
   <span style="display: inline-block; vertical-align: middle; text-align: center; margin: 0 2px;"><span style="display: block; border-bottom: 1px solid #111827; padding: 0 4px; font-size: 0.85em; line-height: 1.2;">分子</span><span style="display: block; padding: 0 4px; font-size: 0.85em; line-height: 1.2;">分母</span></span>
   ```

3. **求和 / 乘积 / 极限 / arg min 垂直堆叠:**
   ```html
   <span style="display: inline-block; vertical-align: middle; text-align: center; margin: 0 4px;"><span style="display: block; font-size: 0.7em; line-height: 1.0; margin-bottom: -1px;">上限</span><span style="display: block; font-size: 1.3em; line-height: 1.0; font-family: 'Times New Roman', Times, serif;">&sum;</span><span style="display: block; font-size: 0.7em; line-height: 1.0; margin-top: -1px;">下限</span></span>
   ```
   > 对于 `arg min` / `max` 等仅含下限的算子，可用两层 `<span style="display: inline-block; vertical-align: middle; text-align: center; margin: 0 4px;"><span style="font-size: 0.8em; display: block; line-height: 1.1;">arg min</span><span style="font-size: 0.7em; display: block; line-height: 1.1;"><i>i</i></span></span>`。

4. **根号 (带上划线):**
   ```html
   &radic;<span style="border-top: 1px solid #111827; padding-top: 1px; margin-left: -2px;">( 被开方数 )</span>
   ```

5. **常用符号与变量排版:**
   - 期望算符：双线大写 E（`&#120124;`）
   - 行内变量：斜体 `<i>x</i>`
   - 希腊字母与算符：统一转为 HTML 实体或 Unicode（`&alpha;`、`&beta;`、`&sigma;`、`&isin;`、`&ne;`、`&minus;` 等）
   - 上下标：`<sup>` 与 `<sub>`
