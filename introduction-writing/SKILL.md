---
name: introduction-writing
description: >-
  Write a complete Introduction section (intro.tex) by first reading the reference
  papers' introductions to learn their paragraph structure and writing logic, then
  reading method.tex for model name and contributions. Produces 5–7 paragraphs
  following the top-venue narrative arc (background → challenge → existing methods
  & gaps → motivation → method overview → contributions list → paper outline).
  Always ends with a 4-point contribution list and a fixed "The remainder of this
  paper" paragraph. Chinese triggers: introduction写作、引言写作、intro.tex、
  第一章节写作、研究背景、contributions写作、论文引言.
disable-model-invocation: true
---

# Introduction 写作

## 前置条件

- 参考论文已解析为 `papers/<slug>/text.md`（用于学习写作结构和逻辑）
- `method.tex` 已完成（用于提取模型名称、核心模块、贡献点）
- `experiments.tex` 已完成（用于提取数据集数量/类型、实验结果亮点）

> **写作规范（强制）**：起草完成后，必须对照 `../WRITING_STANDARDS.md` 逐条自查。
> 特别注意：**只有贡献点列表（contributions）可以用 `enumerate`/`itemize`**，
> 其余段落（背景、挑战、现有方法综述、动机、方法概述）必须是连续散文，不能出现
> `(i)(ii)(iii)`、`First,/Second,/Third,` 等分点式表达，也不能使用破折号插入语。

---

## 总体流程

```text
第1步 读取所有 papers/<slug>/text.md，定位并分析每篇参考论文的 Introduction 写法
   ↓
第2步 读取 method.tex，提取：模型名称、3–4 个核心模块/创新点
   ↓
第3步 读取 experiments.tex，提取：数据集数量/名称、baseline 数量、结果亮点
   ↓
第4步 按 5–7 段结构起草 intro.tex，严格参照参考论文的写作逻辑
   ↓
第5步 输出独立文件 intro.tex
```

---

## 第 1 步：分析参考论文的 Introduction 写作结构

对每篇 `papers/<slug>/text.md`，找到 Introduction 节（通常在 Abstract 之后到 Related Work / Method 之前），逐段分析并记录：

| 段落 | 主题 | 关键句型 | 引用方式 |
|------|------|----------|----------|
| P1 | 背景与重要性 | "X plays a vital role in..." | 宏观引用 2–3 篇 |
| P2 | 挑战 | "However, ... remains challenging because..." | 技术性描述 |
| P3 | 已有方法综述 + 不足 | "Existing methods ... [cite]. Despite..., they fail to..." | 按类别引用 |
| P4 | 动机/观察 | "Motivated by..., we observe that..." | 可以无引用 |
| P5 | 方法简介 | "To address these issues, we propose..." | 自引 |
| P6 | 贡献列表 | "In summary, the main contributions are as follows:" | 无引用 |
| P7 | 论文结构 | "The remainder of this paper is organized as follows." | 无引用 |

重点学习：
- **P1 怎么引出任务**：是从应用价值切入，还是从数据规模/问题规模切入，还是从技术背景切入
- **P2 挑战怎么拆解**：是列举 2–3 条具体技术挑战，还是用对比的方式（"static vs dynamic"）
- **P3 已有方法如何分类**：按技术路线（RNN/GNN/Transformer）还是按方法范式（统计/深度学习/预训练）
- **P4 动机句如何衔接 P3 的不足**：通常用 "Motivated by... / Inspired by... / To bridge this gap..."
- **每段的长度**：几句话，是否超过 150 词

---

## 第 2 步：从 method.tex 提取写作素材

读取 `method.tex`，记录：

```text
模型名称: <ModelName>
任务: <task description>
核心创新模块 (4个):
  - Module A: <名称 + 一句功能描述>
  - Module B: ...
  - Module C: ...
  - Module D: ...（若不足4个，可将整体架构设计算作一条）
```

这 4 个模块直接对应「贡献列表」的 4 条。

---

## 第 3 步：从 experiments.tex 提取实验亮点

读取 `experiments.tex`，记录：

```text
数据集: N 个，类型/名称
Baseline 数量: M 个，类别
结果亮点: (用于 P5 末尾或 P6 中点出)
```

---

## 第 4 步：按固定结构起草 intro.tex

### 固定段落结构（严格按此顺序，共 7 段）

**P1 — 背景与重要性**（3–5 句）

句型框架（参照参考论文风格选择一种）：

- 应用价值切入型：`"<Task> has become increasingly critical for <application domain>, enabling <downstream benefit>~\cite{...}. ..."`
- 数据/规模切入型：`"The proliferation of <data type> has created new opportunities for <task>~\cite{...}. ..."`
- 技术背景切入型：`"Accurate <task> is a fundamental problem in <domain>, attracting significant research attention~\cite{...}. ..."`

末句必须点出任务的核心难点引子，为 P2 铺垫。

---

**P2 — 核心挑战**（3–5 句）

句型框架：

```
"Despite its importance, <task> remains challenging due to several inherent
characteristics. First, <挑战1，技术性描述>. Second, <挑战2>. [Third, <挑战3>.]
These challenges collectively make it difficult for existing methods to achieve
satisfactory performance."
```

挑战必须与方法模块直接对应——P2 提出的挑战，P5 中的模块必须分别解决，否则逻辑不自洽。

---

**P3 — 已有方法综述与不足**（4–7 句）

按方法类别分组（2–3 组），每组 1–2 句 + 引用，末尾统一指出共同不足：

```
"Early approaches, such as <方法类别A>, leverage <技术> to <目标>~\cite{...},
but <局限A>. <方法类别B> methods~\cite{...} further improve <aspect>, yet
<局限B>. More recently, <方法类别C>~\cite{...} have shown promising results;
however, <核心不足，直接引出我们的动机>."
```

类别划分必须参照参考论文 Introduction P3 的分类方式（不要自创）。

---

**P4 — 动机与观察**（2–4 句）

```
"Motivated by <观察或洞察>, we argue that <核心设计思路>.
[具体说明观察到什么现象/理论支持这个设计方向的直觉。]
This leads us to propose a <形容词> framework that <核心机制简述>."
```

P4 是过渡段，不要太长，重点是逻辑衔接 P3 的不足 → P5 的方案。

---

**P5 — 方法概览**（4–6 句）

```
"To address the aforementioned challenges, we propose <ModelName>, a
<架构描述 1–2 句>. Specifically, <Module A> is designed to <解决挑战1>.
<Module B> enables <解决挑战2> through <机制>. [<Module C/D 同理>.]
Extensive experiments on <N> <数据集类型> datasets demonstrate that <ModelName>
achieves <结果亮点，如 consistently outperforms M competitive baselines>."
```

注意：P5 末句提前给出实验结论，为贡献列表做铺垫。

---

**P6 — 贡献列表**（固定格式，4 条）

```latex
In summary, the main contributions of this paper are as follows:
\begin{itemize}
  \item We propose \textbf{<ModelName>}, a <一句话核心架构描述>.
  \item We design <Module A/核心创新1>，which <功能+解决的问题>.
  \item We introduce <Module B/核心创新2>，which <功能+解决的问题>.
  \item Extensive experiments on <N> real-world datasets demonstrate that
        <ModelName> consistently outperforms <M> competitive baselines,
        achieving state-of-the-art performance across multiple metrics.
\end{itemize}
```

规则：
- 第1条：提出整体模型（可以先用一句话点出建模视角/问题设定，但整条的落点必须是
  "we propose <ModelName>, a ..."，即以提出方法收尾）。
  **第1条禁止写成纯粹的问题陈述/gap identification**（如 "We identify and address
  a gap ...: the lack of ..."、"We observe that existing methods fail to ..."），
  这类句子只指出了问题而没有说明做了什么，读起来像是把 P4（Motivation）段落又
  重复了一遍，必须改写为以"we propose/we formulate ... and propose ..."为主干、
  在从句里带出问题动机的句子（可参考："We formulate <task> from a <视角>
  perspective that explicitly <解决的问题>, and propose <ModelName>, a unified
  framework that ..."）。
- 第2、3条：提出关键模块（对应 method.tex 中的核心创新，不超过 2 条模块级别的贡献）
- 第4条：实验结论（固定最后一条）
- 每条用"We propose / We design / We introduce / Extensive experiments"等动词开头，不重复

---

**P7 — 论文结构**（固定格式，1 段）

按实际 section 结构填写（参照用户提供的模板，替换括号内容）：

```latex
The remainder of this paper is organized as follows.
Section~\ref{sec:related} reviews related work on <主题1>, <主题2>, and <主题3>.
Section~\ref{sec:method} presents the detailed methodology of <ModelName>.
Section~\ref{sec:experiments} reports experimental results and analyses.
Finally, Section~\ref{sec:conclusion} concludes the paper and discusses
future research directions.
```

---

## 写作质量检查清单（输出前逐项确认）

- [ ] P1 的引用 ≥ 2 篇，来自 references.bib
- [ ] P2 的挑战数量与 method.tex 中的模块数量对应（1对1或多对1）
- [ ] P3 的方法分类与参考论文 Introduction 的分类方式一致
- [ ] P4 末句明确说明"这导致我们提出..."，不含方法细节
- [ ] P5 末句包含实验结论数字（数据集数 N、baseline 数 M）
- [ ] P6 贡献列表正好 4 条，第1条整体，第2/3条模块，第4条实验
- [ ] P6 第1条不是纯问题陈述/gap identification（不以 "We identify.../We observe
      that existing methods fail..." 收尾），而是落在 "we propose <ModelName>" 上
- [ ] P7 section 编号与主文档 label 一致
- [ ] 全文不出现"In this paper, we first... then... finally..."流水账
- [ ] 总字数在 600–1000 词之间（不要过短也不要过长）

---

## 输出文件

```latex
% intro.tex
\section{Introduction}
\label{sec:intro}

% P1: Background
...

% P2: Challenges
...

% P3: Existing methods & gaps
...

% P4: Motivation
...

% P5: Method overview
...

% P6: Contributions
In summary, the main contributions of this paper are as follows:
\begin{itemize}
  \item ...
\end{itemize}

% P7: Paper outline
The remainder of this paper is organized as follows. ...
```

用 `\input{intro.tex}` 从主文档引入（在 Abstract 之后、Related Work 之前）。
