---
name: idea-and-method-writing
description: >-
  Generate a research idea by combining methods from reference papers (70% combination,
  30% innovation), or write a paper's Method section by mining top-venue (ACL, NeurIPS,
  ICLR, ICML, AAAI, WWW, ACMMM, etc.) papers from arXiv. Use when the user provides
  reference PDFs and wants an idea; gives only a research direction/topic and wants idea
  candidates from top-conference papers; or provides a method framework diagram / draft
  method description and needs the Method section written using similar papers as style
  references. The Method section is always produced as a standalone LaTeX file (method.tex)
  with at least one algorithm pseudocode block, strictly mirroring the introduction/structure/
  writing logic of the reference top-venue papers. Chinese triggers: 想idea、生成idea、组合创新、
  方法部分写作、方法部分latex、算法伪代码、检索顶会论文、arxiv下载论文、解析文献PDF.
disable-model-invocation: true
---

# Idea 构思与方法部分写作

## 总体流程（默认路径，先想 idea 再写方法）

```
第1步 获取论文 (场景 A: 已有PDF / 场景 B: 只给方向→检索下载)
   ↓
第2步 解析论文，提取文字+图片 (extract_pdf.py)
   ↓
第3步 生成组合创新 idea（70%组合 + 30%创新），输出候选 idea 列表
   ↓
第4步 【停下来，等待用户确认/选定其中一个 idea，或提出修改意见】
   ↓
第5步 基于确定的 idea，检索/复用方法相近的顶会论文，参考其方法部分写作结构，
       撰写正式的 Method 部分文字
```

**关键点：第 3 步产出 idea 后必须停下来向用户确认，不要在没有确认 idea 的情况下直接写方法部分。** 只有用户明确选定或认可某个 idea 之后，才进入第 5 步的方法写作（第 5 步的具体做法见下方「撰写方法部分」章节，与场景 C 共用）。

如果用户已经给了明确的方法框架图/草稿（idea 已经定了，不需要再生成 idea），直接跳到「场景 C」，跳过第 3、4 步。

## 判断入口场景

1. **用户给了参考文献 PDF，且还没有 idea** → 场景 A → 第 3 步生成 idea → 第 4 步确认 → 第 5 步写方法
2. **用户只给了研究方向/关键词，且还没有 idea** → 场景 B → 第 3 步生成 idea → 第 4 步确认 → 第 5 步写方法
3. **用户已经有方法框架图/方法草稿（idea 已定）** → 场景 C → 直接进入第 5 步写方法

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

## 场景 C / 第 5 步：撰写方法部分（idea 已确定后）

无论 idea 来自场景 A/B 用户确认后，还是用户直接给了框架图/草稿，写方法部分都走这一步：

1. 判断已有的参考论文（场景 A/B 阶段下载的，或用户直接给的框架图对应领域）是否已包含 **方法结构相近** 的写作样本。若不够，根据 idea/框架图里的技术关键词（模型结构、损失函数、任务类型等），用 `scripts/arxiv_search.py` + WebSearch 再定位 **5 篇** 方法相近、发表于顶会/顶刊的论文。
2. 用 `scripts/arxiv_download.py --source` 下载并解压（优先拿到 LaTeX 源码而非仅 PDF，方便直接照抄写作范式，如小节命名、公式环境、算法环境用法），重点分析这些论文的 **Method/Approach 章节**：
   - **怎么引出**：每一节开头是先给整体 pipeline/框架图描述，还是先复述 problem formulation，还是先点出与已有方法的差异再引出本节方案？记录其引出套路。
   - **怎么组织**：小节划分方式（按模块、按数据流顺序、按 Encoder/Decoder 划分等）、每小节篇幅比例、公式如何编号与引用、图表在何处插入并如何在正文呼应、符号表是否单独给出。
   - **怎么收尾**：小节/整章末尾是否有小结句、是否呼应最初提出的问题或创新点。
3. 严格模仿以上写作逻辑（引出方式、组织顺序、过渡句风格、术语习惯），但内容必须是用户自己方法的真实描述，不得照抄参考论文的句子或结论。
4. **产出独立的 LaTeX 文件**（不要直接写进主文档正文），命名如 `method.tex`，用 `\input{method.tex}` 或 `\include{method}` 从主文档引入。文件需可独立编译审阅（含必要的 `\subsection`/`\subsubsection` 结构、公式、图表占位、算法环境）。
5. **方法部分必须包含至少一个算法伪代码**，用 `algorithm` + `algorithmic`（或 `algorithm2e`）宏包按参考论文中出现的伪代码风格给出，需要在正文中用 `Algorithm~\ref{...}` 引用并做文字说明（输入、输出、每一步在做什么、对应哪个创新模块）。

模板骨架（按参考论文实际风格调整章节数量与命名）：

```latex
% method.tex
\section{Methodology}
\label{sec:method}

% 1. 引出：problem formulation / 整体框架图描述，模仿参考论文的引出方式
\subsection{Problem Formulation}
...

\subsection{Overall Framework}
% 插入框架图 \includegraphics，呼应 idea 中的组合+创新模块
...

% 2. 逐模块展开，每个模块一个 subsection，公式 + 图表按参考论文习惯呼应
\subsection{<模块A名称>}
...

\subsection{<模块B / 创新点名称>}
...

% 3. 算法伪代码，风格参考顶会论文
\begin{algorithm}[t]
\caption{<算法名称>}
\label{alg:method}
\begin{algorithmic}[1]
\Require 输入
\Ensure 输出
\State ...
\end{algorithmic}
\end{algorithm}

% 4. 收尾/小结，呼应最初的问题或创新点（如参考论文有此习惯）
```

---

## 第 3 步：产出组合创新 idea（场景 A / B 通用）

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

5. 输出 idea 后**必须停下来**，向用户提问确认：是否选定某个 idea、是否需要调整组合方式或创新点，得到明确答复后再进入第 5 步写方法部分。

## 依赖

`pip install pymupdf requests`（PyMuPDF 用于 PDF 文字/图片提取，requests 用于 arXiv API 与下载）。
