# Project Reader — WeChat Technical Project Deep Reader 🚀📱

<p align="center">
  <b>English</b> • <a href="README_zh.md">中文文档</a> • <a href="SHOWCASE.md">Showcase</a>
</p>

---

## 📖 Introduction

`project-reader` is a specialized Agent skill engineered for technical content creators, independent developers, and tech bloggers publishing to **WeChat Official Accounts (微信公众号)**.

Provide any project link (GitHub repository, product documentation, AI demo page, or whitepaper), and it will analyze the project through the lens of a **genuine, experienced tech blogger ("Digital Life Kazik" style)**. It explains the project's background, core breakthrough, and architecture in plain human analogies, verifies hands-on instructions against factual evidence (falling back to official repository links when no simple CLI exists), bluntly exposes hidden limitations, and outputs a **minimalist, elegant, 100% inline-CSS WeChat HTML file**.

---

## 🎯 Core Principles

1. **Evidence-First & Zero Hallucination**:
   - Strict adherence to verifiable facts from the provided webpage or documentation.
   - **Never invent non-existent commands or fake benchmarks** to feign a "tested" experience.
   - If quickstart commands exist in the repository, extract the minimal verified steps; if it is a web demo, direct readers there; if no simple CLI is provided, honestly provide the official repo URL as a fallback.
2. **Conversational First-Person Narrative**:
   - Speaks like a knowledgeable peer sharing an exciting finding over coffee.
   - Zero AI buzzwords ("closed loop", "paradigm shift", "empowerment").
3. **Bridges Beginners and Industry Practitioners**:
   - Everyday metaphors for beginners ("digital acoustic filter", "dusting off vs. photo restoration").
   - Under-the-hood architectural insights and blunt trade-offs for seasoned engineers.
4. **Mobile Visual Breathing Rhythm**:
   - Paragraphs limited to 1~3 lines for effortless scrolling.
   - Outputs a ready-to-publish `.html` file that preserves styling perfectly when pasted into the WeChat Official Account editor.

---

## 🏗️ Standard Article Schema

1. **Author Reference Toolbox (Top Dashed Box)**: 3 high-impact headlines (Personal Story, Pain-Point Curiosity, Practical Utility) + WeChat cover image design (2.35:1) and punchy text.
2. **First-Person Scenario Opening**: Connects with readers via an authentic everyday pain point or genuine curiosity.
3. **Plain Human Summary**: Plain-language one-liner metaphor + 2~3 core takeaways.
4. **Context & Under-the-Hood**: Historical pain points + author's architectural breakthrough + plain-English background tags (`【补充背景】`).
5. **How to Try It (Evidence-Grounded)**: Verified quickstart commands or official links/demo fallback.
6. **Reality Check & Cold Water**: Brutally honest assessment of trade-offs, limitations, and edge-case pitfalls.
7. **Warm & Grounded Closing**: Objective verdict and audience recommendation.

---

## 📂 File Structure

```
c:\Users\letv\Desktop\MTB\skills\paper\project-reader\
├── SKILL.md                          # Core Agent skill definition & execution prompt
├── README.md                         # English documentation (this file)
├── README_zh.md                      # Chinese documentation
├── SHOWCASE.md                       # Full production article showcase
├── demo-article.html                 # Pre-compiled high-aesthetic WeChat HTML demo
└── templates\
    └── wechat-style-guide.md         # WeChat inline CSS & mobile typography specification
```

---

## 🚀 Usage

Send any technical project URL in your conversation:

```text
Please introduce this project as a WeChat Official Account article:
https://github.com/inworld-ai/voice-isolator
```

The Agent will inspect the link and generate a publication-ready `[project-name].html` in your directory.
