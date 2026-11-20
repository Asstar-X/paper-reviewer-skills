# Paper Reviewer Skills 📄🔍

<p align="center">
  <a href="README.md">English</a> • <b>中文</b> • <a href="SHOWCASE.md">Showcase (样例展示)</a>
</p>

<p align="center">
  <img src="https://img.shields.io/badge/Version-2.0.0-blue.svg" alt="Version">
  <img src="https://img.shields.io/badge/Role-The_Ultimate_7--Point_Extractor-black.svg" alt="Role">
  <img src="https://img.shields.io/badge/Spec-Agent_Skill_Standard-green.svg" alt="Agent Skill">
  <img src="https://img.shields.io/badge/Typography-WeChat_&_Zhihu-orange.svg" alt="Typography">
  <img src="https://img.shields.io/badge/Math-Hybrid_Dual--Engine-purple.svg" alt="Math">
</p>

---

## 🌟 极简文献拆解专家 (The Ultimate 7-Point Extractor v2.0)

`paper-reviewer-skills` 是一套工业级智能体技能（Agent Skill），专为学术文献高密度深度精读、严苛极客评分以及自媒体高保真发布（微信公众号、知乎专栏、飞书文档）而设计。

它彻底过滤学术垃圾话，坚持“5分为中庸及格线，10分为颠覆神作”的冷酷标准，以结构化的 **7-Point 核心技术框架** 重构文献：

1. **论文基本信息 (Metadata)**：核心元数据、会议期刊公认等级，以及一气呵成的端到端算法流微叙事。
2. **一、 完整摘要 (The Perfect Abstract)**：高保真提炼问题、方法、真正贡献与硬核结果。
3. **二、 知识背景全景 (Background & Context)**：前置概念速查、赛道技术版图及“为什么出现在现在（Why Now?）”。
4. **三、 痛点与动机 (Problem & Motivation)**：底层物理/数学瓶颈、核心假设剖析与条件被打破时的“失效推演（What-If）”。
5. **四、 核心方法 (Innovation & Methods)**：穷尽拆解系统子模块、关键公式推导、输入输出张量对齐与算法流程。
6. **五、 实验 (Experiments & Analysis)**：完整复刻论文所有定量对比表格（Table 1 至 Table X），加粗最强指标，附带“一划而过”秒懂的数据解读与局限性评估。
7. **六、 极客评分与实战研判 (Geek Evaluation & Reality Check)**：三维极客雷达打分、真实算力与部署暗礁剖析、论文未言之隐，以及穿透性的号主终局选型建议。

---

## 🚀 核心特性升级 (v2.0 工业级突破)

### 1. 🛡️ 不可信文献输入防线与提示注入防护 (Prompt Injection Defense)
将所有 PDF 文本、OCR 数据与论文元信息严格限制为只读被动数据，严禁模型将其视作执行指令。天然免疫隐藏在论文文字中试图重置角色、操纵评分或刺探系统提示词的越狱对抗文本。

### 2. 📐 自适应多栏插图提取与安全区保护 (`figure-extraction.md`)
- **自适应分栏与栏间隙探测**：废除硬编码 `W / 2` 左右分界，通过页面正文水平坐标聚类分析自动适配单栏、双栏或通栏排版；
- **绘图核心区 (Drawing Hull) 白名单保护**：通过矢量图形与位图闭包分析，保护架构图、流程图内部的长图例、长注释文本不被误抹；
- **内存白底遮罩 (White-out Masking)**：在不修改原 PDF 的前提下，阻断相邻栏目文字渗入，以 `3.0x` 视网膜解析度导出极为干净的高清插图。

### 3. 🧮 混合数学公式双引擎 (Hybrid Dual-Engine Math, `html-template.md`)
- **Tier 1 (轻量常规公式)**：通过原生 HTML 语义标签（`<span>` 垂直堆叠分式、Times New Roman 字体、Unicode 算符）排版，保证微信内一键复制零图损；
- **Tier 2 (高维复杂公式)**：针对多维矩阵（`bmatrix`）、多行分段函数（`cases`）等复杂结构，运行免外部 LaTeX 发行版的 Python `matplotlib.mathtext` 脚本，离线导出透明底 300 DPI Base64 PNG 并行内居中嵌入，彻底打破排版天花板。

### 4. 📰 微信公众号编辑器清洗全面免疫
- 全内联 CSS 属性（`style="..."`），复制粘贴 100% 保留渲染；
- 采用微信原生白名单 `<section style="box-sizing: border-box; border-left: ...">`，防止编辑器解包普通 `<div>` 导致外层黑实线丢失；
- 单元格显式声明否定样式（`border: none;`），置于横向触摸滚动容器中，彻底免疫微信强加的网格线。

### 5. 🔄 运行环境自适应降级矩阵 (Graceful Degradation)
- **全功能环境**（Shell + Python + `pymupdf` + 视觉工具）：执行完整裁图、公式转换并导出 Base64 HTML；
- **轻量环境**（Shell + Python，无 PyMuPDF）：跳过物理裁图，自动补充 ASCII/结构化图注，正常导出公式与学术 HTML；
- **受限沙箱环境**（纯只读/无脚本权限）：优雅降级为高质量 GFM Markdown，零报错平稳交付。

---

## 📂 项目文件架构

```text
paper-reviewer-skills/
├── SKILL.md                 # 核心 Agent Skill 规范（包含标准 YAML Frontmatter）
├── figure-extraction.md     # 自适应多栏检测与图内图例保护插图提取规范
├── html-template.md         # 微信自媒体纸媒排版规范与混合公式引擎
├── README.md                # 英文使用指南
├── README_ZH.md             # 中文使用指南
├── SHOWCASE.md              # 完整样例精读报告（BEATs - ICML 2023）
├── Beats.html               # 最终微信自媒体高保真 HTML 成果文件
├── figure/                  # 提取的高清图表 (figure_1.png ~ figure_4.png)
└── BEATS - ... .pdf         # 样例学术文献 PDF
```

---

## 💡 快速上手

将本项目目录添加至智能体技能目录（如 `~/.gemini/antigravity/skills/` 或 `.claude/skills/`）：

- **触发标准拆解**：*“精读这篇论文并做标准拆解”* -> 输出完整 7-Point 结构化报告。
- **触发博客生成**：*“将这篇论文转换为适合发布在公众号/知乎的学术推文”* -> 自动裁剪插图、处理公式并生成 HTML。
- **触发极速摘要**：*“快速概览这篇文献的核心创新与评分”* -> 输出元信息、摘要与极客评分。

---

## 📄 开源许可证

MIT License.
