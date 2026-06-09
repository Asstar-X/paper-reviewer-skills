# Paper Reviewer Skills 📄🔍

<p align="center">
  <a href="README.md">English</a> • <b>中文</b> • <a href="SHOWCASE.md">Showcase (样例展示)</a>
</p>

<p align="center">
  <img src="https://img.shields.io/badge/Role-The_Ultimate_7--Point_Extractor-black.svg" alt="Role">
  <img src="https://img.shields.io/badge/Engine-LLM%20Agent%20Skill-blue.svg" alt="Engine">
  <img src="https://img.shields.io/badge/Outputs-Bilingual%20Markdown%20%7C%20WeChat-orange.svg" alt="Outputs">
</p>

---

## 🌟 极简文献拆解专家 (The Ultimate 7-Point Extractor)

[SKILL.md](SKILL.md) 定义了一个专门用于学术论文深度精读与高精拆解的智能体技能。它能够自动过滤文献中的低信噪比修饰语，以高度结构化的 7 点架构精准复现论文的核心技术逻辑与实际工程落地价值：

1. **论文基本信息 (Metadata)**：包括文章名称、作者机构、期刊会议、论文类型及一句话定位。
2. **一、 完整摘要 (The Perfect Abstract)**：无损传递原作者的核心意图。
3. **二、 知识背景全景 (Background & Context)**：勾勒前置概念与赛道大局观。
4. **三、 痛点与动机 (Problem & Motivation)**：深挖技术瓶颈与研究契机。
5. **四、 核心方法 (Innovation & Methods)**：公式级别细致剖析系统子板块与设计细节。
6. **五、 实验 (Highlights & Key Takeaways)**：客观呈现量化对比表格与局限性评估。
7. **六、 极客评分 (Geek Evaluation)**：针对创新性、实用性与行业价值进行严苛客观的打分。

### 🛠️ 核心功能特性
* **零废话原则**：直接输出核心干货，严禁包含任何多余寒暄与结论式废话。
* **高精公式与三线表排版**：转换数学公式为标准 LaTeX 方程式，使用标准 GFM 表格整齐排版实验数据。
* **插图自动精准提取与遮罩**：结合 `pymupdf` 动态提取插图，利用内存绘白技术阻断双栏排版中的跨栏文字渗入，以 `3.0x` 解析度导出极其干净的插图。
* **HTML 格式导出**：可直接生成包含内联样式的 HTML，一键复制粘贴至微信公众号、知乎等第三方平台，无损保留排版与公式。
