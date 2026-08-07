---
name: related-work-writing
description: >-
  Extract references cited in already-parsed reference papers, fetch proper
  BibTeX via CrossRef API, assemble a 40-50 entry .bib file, then write a
  Related Work section (Section 2) with 3 subsections in a standalone
  related_work.tex. Subsection themes are derived from method.tex (what the
  paper proposes). Each subsection surveys related approaches with inline
  citations in survey style. Use after idea-and-method-writing has produced
  method.tex and parsed reference papers into papers/<slug>/text.md. Chinese
  triggers: 相关工作写作、related work写作、文献整理bib、提取参考文献、
  BibTeX生成、related_work.tex、第二章节写作.
disable-model-invocation: true
---

# Related Work 写作

## 前置条件

- `method.tex` 已完成（用于确定 3 个 subsection 的主题）
- 参考论文已解析为 `papers/<slug>/text.md`（用于提取被引文献列表）

---

## 总体流程

```text
第1步 读取 method.tex，确定 3 个 Related Work subsection 主题
   ↓
第2步 从每篇参考论文的 References 部分提取被引文献列表
   ↓
第3步 用 CrossRef API 查询并生成规范 BibTeX，去重后保存 references.bib（40–50 条）
   ↓
第4步 按 3 个主题分配文献，写 related_work.tex
```

---

## 第 1 步：确定 3 个 subsection 主题

读取 `method.tex`，提取：
- 方法解决的核心任务（如时空图预测、文本分类、推荐等）
- 方法借鉴的主要技术路线（如 GNN、Transformer、分解方法、LLM 等）
- 方法的创新角度（如动态图结构学习、不确定性建模、跨模态融合等）

将这些归纳为 3 个 subsection，通常遵循：

```
Subsection 1: 任务本身的传统/早期方法（问题背景）
Subsection 2: 与本文方法技术路线最相关的方法（核心对比）
Subsection 3: 最近出现的、与本文创新角度最相关的方法（近期进展）
```

主题名称必须与 method.tex 中的实际内容强关联，不要套用通用模板标题，例如：
- ✅ `\subsection{Spatial-Temporal Graph Neural Networks}`
- ✅ `\subsection{Uncertainty Quantification in Forecasting}`
- ❌ `\subsection{Related Methods}`（过于通用）

---

## 第 2 步：从参考论文中提取被引文献

对每篇 `papers/<slug>/text.md`，定位 References 节并提取文献条目：

```bash
python scripts/extract_references.py papers/ --out raw_refs.json
```

脚本逻辑：
- 找到文本中的 "References" 或 "Bibliography" 行（通常在最后几页）
- 提取格式为 `[N] Author, Title, Venue, Year` 或 `Author et al. (Year). Title. Venue.` 的条目
- 去除重复标题，输出 JSON 列表：`[{"title": "...", "authors": "...", "year": "...", "raw": "..."}]`

---

## 第 3 步：查询 BibTeX，生成 references.bib

```bash
python scripts/fetch_bibtex.py raw_refs.json \
    --out references.bib \
    --target 40 --max-query 80
```

脚本逻辑（使用 CrossRef 公开 API，无需注册）：
- 对每条 raw_ref，以标题为关键词查询 `https://api.crossref.org/works?query.title=...&rows=1`
- 匹配度高（标题相似度 > 0.85）则取其 metadata（DOI、作者、年份、venue/container-title）
- 格式化为 BibTeX（`@article` / `@inproceedings` / `@misc`）
- 用 DOI 去重，优先保留有 DOI 的条目
- 未查到的条目生成基于原始字符串的近似 BibTeX（`@misc`），并标注 `% VERIFY` 供人工检查
- 目标 40–50 条：按与 method.tex 主题的相关性排序后截取（先保留有明确 DOI 的，再补充 `@misc`）

**注意**：CrossRef 结果不一定100%准确，生成的 .bib 必须告知用户检查有 `% VERIFY` 标记的条目。

---

## 第 4 步：写 related_work.tex

```latex
% related_work.tex
\section{Related Work}
\label{sec:related}

\subsection{<主题1>}
\label{subsec:rw1}
% 段落结构：按时间/方法演进顺序，每句引用 2–4 篇，末句指出不足并引出本文贡献
...

\subsection{<主题2>}
\label{subsec:rw2}
...

\subsection{<主题3>}
\label{subsec:rw3}
...
```

用 `\input{related_work.tex}` 从主文档引入（通常在 Introduction 之后、Method 之前）。

### 每个 subsection 的写作逻辑（survey 段落结构）

每个 subsection **1–2 个段落**，每段 **5–8 句**，总计每个 subsection 约 8–14 句：

```
句1: 领域/方向的背景句（范围限定）
句2–3: 早期/基础代表方法，指出贡献 [cite1, cite2, cite3]
句4–5: 中期进展，技术演化 [cite4, cite5, cite6]
句6–7: 近期 SOTA，最接近本文的工作 [cite7, cite8]
句8: 指出现有方法共同局限，过渡句（"However, ..."），不超过 1 句
（不要在 Related Work 里过多宣传自己方法，只需最后一句简要说"In contrast, our method..."）
```

### 引用分配原则

| Subsection | 引用数量 |
|------------|----------|
| Subsection 1 | 12–18 篇 |
| Subsection 2 | 12–18 篇 |
| Subsection 3 | 10–15 篇 |
| 合计 | **40–50 篇** |

同一篇文献可以在多个 subsection 都引用（跨主题相关时）。

### 写作风格要求（参考顶会顶刊 Related Work）

- 每句必须有引用，不要出现没有 `\cite{}` 的陈述句（第一句背景句除外）
- 引用放在句末 `.` 之前：`... proposed method~\cite{author2024xyz}.`
- 用 `\citet{}` 引入论文名字时："Smith et al.~\cite{smith2024} proposed..."
- 避免"Paper A said..." 风格，用被动/主动描述方法特性
- 每个 subsection 末尾必须有过渡句，明确指出现有方法的某个局限

---

## 工具清单

| 脚本 | 功能 |
|------|------|
| `scripts/extract_references.py` | 从 text.md 解析 References 节，输出结构化 JSON |
| `scripts/fetch_bibtex.py` | CrossRef API 查询 → 生成 .bib，未命中条目标注 `% VERIFY` |
