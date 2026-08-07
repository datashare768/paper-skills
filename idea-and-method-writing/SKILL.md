---
name: idea-and-method-writing
description: >-
  Generate a research idea by combining methods from reference papers (70% combination,
  30% innovation), or write a paper's Method section by mining top-venue (ACL, NeurIPS,
  ICLR, ICML, AAAI, WWW, ACMMM, etc.) papers from arXiv. Use when the user provides
  reference PDFs and wants an idea; gives only a research direction/topic and wants idea
  candidates from top-conference papers; or provides a method framework diagram / draft
  method description and needs the Method section written using similar papers as style
  references. Chinese triggers: 想idea、生成idea、组合创新、方法部分写作、检索顶会论文、
  arxiv下载论文、解析文献PDF.
disable-model-invocation: true
---

# Idea 构思与方法部分写作

## 三种输入场景，先判断走哪条路线

1. **用户给了参考文献 PDF** → 走「场景 A：解析已给文献」
2. **用户只给了研究方向/关键词** → 走「场景 B：顶会检索」
3. **用户给了方法框架图或方法部分草稿** → 走「场景 C：对标顶会写作」

三种场景最终都产出：**每篇参考论文的结构化摘要（方法要点+图片）** + **组合创新的 idea 或方法部分文字**，遵循 **70% 组合已有方法 + 30% 改进创新** 的比例。

---

## 场景 A：解析已给的参考文献 PDF

1. 为本次 idea 建一个工作目录，例如 `workspace/<idea-slug>/papers/`。
2. 对每篇 PDF 运行文字+图片提取脚本：

```bash
python scripts/extract_pdf.py <pdf路径> workspace/<idea-slug>/papers/<paper-slug>/
```

输出：`<paper-slug>/text.md`（全文文字，按页分段）+ `<paper-slug>/figures/pageN_imgM.png`（所有嵌入图片）。

3. 逐篇通读 `text.md`，重点提取：**要解决的问题、核心方法/模块、创新点、实验结论**。
4. 进入「产出组合创新 idea」步骤。

## 场景 B：只给了研究方向，需要检索顶会论文

1. 用 `scripts/arxiv_search.py` 按方向关键词在 arXiv 检索候选论文（arXiv 元数据不含会议名，需结合标题/摘要判断，或用 WebSearch 交叉确认某论文发表于 ACL/NeurIPS/ICLR/ICML/AAAI/WWW/ACMMM 等顶会，例如搜索 `"<论文标题>" ACL 2025 site:aclanthology.org` 或 `NeurIPS 2025 openreview`）：

```bash
python scripts/arxiv_search.py "<检索关键词>" --max-results 30
```

2. 从结果中筛选 **6-10 篇** 确认发表于目标顶会的论文，记录其 arXiv ID。
3. 下载源码压缩包（优先，含矢量图源文件）或 PDF：

```bash
python scripts/arxiv_download.py <arxiv_id> --dest workspace/<idea-slug>/papers/ --source   # 优先：下载 e-print 并自动解压
python scripts/arxiv_download.py <arxiv_id> --dest workspace/<idea-slug>/papers/ --pdf       # 备选：直接下 PDF
```

4. 对下载到的 PDF 运行场景 A 中的 `extract_pdf.py` 提取文字和图片（若下载的是 LaTeX 源码包，直接读取 `.tex` 文字部分，图片在源码目录里，无需再跑 PDF 提取）。
5. 进入「产出组合创新 idea」步骤。

## 场景 C：已有方法框架图 / 方法写作草稿，需要完成方法部分写作

1. 根据框架图或草稿描述的技术关键词（模型结构、损失函数、任务类型等），用 `scripts/arxiv_search.py` + WebSearch 定位 **5 篇** 方法相近、发表于顶会的论文。
2. 用 `scripts/arxiv_download.py --source` 下载并解压，重点阅读这 5 篇论文的 **Method/Approach 章节**（不是整篇），记录：小节划分方式、公式呈现习惯、图表引用方式、术语用词。
3. 参考这 5 篇的写作结构和语言风格（而非照抄内容），结合用户提供的框架图/草稿，撰写自己的方法部分：结构可借鉴，公式符号、创新模块必须是用户自己方法的真实描述。

---

## 产出组合创新 idea（场景 A / B 通用）

1. 为每篇参考论文写一段结构化摘要：`问题 -> 方法要点 -> 创新点`。
2. 找出可组合的方法要点组合空间（不同论文的模块可以互相拼接、迁移到新场景、叠加使用）。
3. 按 **70% 组合 + 30% 创新** 起草 idea：
   - 70%：直接说明借用了哪几篇论文的哪个具体模块/机制，如何拼接。
   - 30%：明确指出针对现有方法的不足做了什么改进（新模块、新约束、新场景适配等），不能只是缝合。
4. 输出格式：

```markdown
## Idea: <标题>

### 参考论文
- [标题1](arxiv链接) — 借用点：...
- [标题2](arxiv链接) — 借用点：...

### 方法组合（70%）
...

### 创新改进（30%）
...

### 待验证问题
...
```

## 依赖

`pip install pymupdf requests`（PyMuPDF 用于 PDF 文字/图片提取，requests 用于 arXiv API 与下载）。
