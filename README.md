# Paper Reviewer Skills 📄🔍

<p align="center">
  <b>English</b> • <a href="README_ZH.md">中文</a> • <a href="SHOWCASE.md">Showcase (样例展示)</a>
</p>

<p align="center">
  <img src="https://img.shields.io/badge/Version-2.0.0-blue.svg" alt="Version">
  <img src="https://img.shields.io/badge/Role-The_Ultimate_7--Point_Extractor-black.svg" alt="Role">
  <img src="https://img.shields.io/badge/Spec-Agent_Skill_Standard-green.svg" alt="Agent Skill">
  <img src="https://img.shields.io/badge/Typography-WeChat_&_Zhihu-orange.svg" alt="Typography">
  <img src="https://img.shields.io/badge/Math-Hybrid_Dual--Engine-purple.svg" alt="Math">
</p>

---

## 🌟 Overview: The Ultimate 7-Point Extractor (v2.0)

`paper-reviewer-skills` is a production-grade agent skill designed for high-density academic literature deconstruction, objective peer-review evaluation, and high-fidelity social media publication (e.g. WeChat Public Platform, Zhihu, Feishu).

It filters out academic fluff, enforces a brutal-yet-fair 10-point scoring scale, and reconstructs papers into a structured **7-Point Technical Framework**:

1. **Metadata & Micro-Narrative**: Core details, venue tier, and an end-to-end algorithmic data-flow narrative.
2. **The Perfect Abstract**: High-fidelity summary capturing the problem, method, contributions, and real outcomes.
3. **Background & Context**: Fundamental concepts, technology landscape, and "Why Now?".
4. **Problem & Motivation**: Physical/mathematical bottlenecks, root causes, explicit/implicit assumptions, and "What-If" failure boundary simulations.
5. **Innovation & Methods**: Exhaustive sub-module architectures, equation derivations, and data structures.
6. **Experiments & Quantitative Tables**: Complete transcription of paper benchmark tables (`Table 1 ~ Table X`) with bolded SOTA metrics and rapid-skimming data insights.
7. **Geek Evaluation & Reality Check**: Brutally honest scores (out of 10) for *Innovation*, *Practicality*, and *Industry Value*, augmented with compute budget checks, deployment boundaries, unsaid caveats, and actionable adoption verdicts.

---

## 🚀 Key Features (v2.0 Highlights)

### 1. 🛡️ Indirect Prompt Injection Isolation
Treats all academic PDFs and research texts strictly as passive data rather than executable directives. Defends against hidden jailbreaks, role-reset tokens, or score-manipulation texts embedded in adversarial papers.

### 2. 📐 Adaptive Multi-Column Figure Extraction (`figure-extraction.md`)
- **Dynamic Gutter & Layout Detection**: Replaces fragile hardcoded coordinate splits with automatic text block clustering to detect single-column, double-column, or full-width layouts.
- **Drawing Hull Safe-Zone Protection**: Prevents accidental masking of internal figure legends, module titles, and parameter annotations inside diagrams.
- **In-Memory White-Out Masking**: Blocks cross-column text bleed at `3.0x` zoom without modifying the source PDF on disk.

### 3. 🧮 Hybrid Dual-Engine Math Typography (`html-template.md`)
- **Tier 1 (Native Semantic HTML)**: Lightweight fractions, sums, and inline variables rendered via pure HTML semantics (`<span>`, Times New Roman, CSS dividers) for zero-loss, image-free copying.
- **Tier 2 (High-Dimensional Equations)**: Renders complex multi-dimensional matrices (`bmatrix`), multi-line cases (`cases`), and tensor contractions into transparent-background, high-DPI Base64 PNGs via Python's built-in `matplotlib.mathtext` (zero external LaTeX installation required).

### 4. 📰 WeChat Editorial Platform Immunity
- Full inline CSS styles (`style="..."`).
- Border cards wrapped in whitelisted `<section style="box-sizing: border-box; border-left: ...">` to prevent WeChat rich text cleaners from unwrapping and stripping borders.
- Three-line academic tables (Booktabs) protected by explicit cell negation (`border: none;`) inside horizontal touch-scrolling containers (`overflow-x: auto;`).

### 5. 🔄 Graceful Degradation Matrix
Automatically detects execution capabilities in the host environment:
- **Full Pipeline**: Shell + Python + PyMuPDF + Multimodal tool → High-res figures + Hybrid formulas + Base64 HTML export.
- **Lightweight Mode**: Python available without PyMuPDF → Full typography HTML export with structured ASCII/diagrammatic notes.
- **Sandboxed Mode**: Read-only / restricted sandbox → Seamless fallback to high-fidelity GitHub-Flavored Markdown.

---

## 📂 Repository Structure

```text
paper-reviewer-skills/
├── SKILL.md                 # Primary Agent Skill specification (with YAML frontmatter)
├── figure-extraction.md     # Adaptive figure extraction, column detection & safe-zone masking
├── html-template.md         # WeChat-immune typography & Hybrid Dual-Engine Math specification
├── README.md                # English documentation
├── README_ZH.md             # Chinese documentation
├── SHOWCASE.md              # Complete walkthrough showcase review (BEATs - ICML 2023)
├── Beats.html               # Reference rendered HTML publication
├── figure/                  # Extracted high-res figures (figure_1 ~ figure_4)
└── BEATS - ... .pdf         # Sample academic PDF
```

---

## 💡 Quick Start

Add this skill to your agent environment (`~/.gemini/antigravity/skills/` or `.claude/skills/`).

Trigger phrases:
- *"精读这篇论文并做标准拆解"* -> Executes **Standard Extraction** (Full 7-Point framework).
- *"将这篇论文转换为适合发布在公众号的深度学术推文/HTML"* -> Executes **Blog Generation** (Extracts figures, renders math, exports HTML).
- *"快速概览这篇文献的核心创新与评分"* -> Executes **Fast Summary** (Metadata, Abstract, and Geek Scores).

---

## 📄 License

MIT License.
