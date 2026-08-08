---
name: abstract-writing
description: >-
  Write a complete Abstract (abstract.tex) for a research paper by reading
  method.tex and experiments.tex for factual grounding. Produces a single dense
  paragraph (~250–350 words) following the top-venue narrative arc:
  background → problem with existing methods → proposed solution → specific
  technical contributions → experimental results → conclusion sentence.
  Chinese triggers: abstract写作、摘要写作、abstract.tex、摘要、写摘要.
disable-model-invocation: true
---

# Abstract 写作

## 前置条件

- `method.tex` 已完成（提取模型名称、缩写、核心模块）
- `experiments.tex` 已完成（提取数据集数量、baseline 数量、关键数值结果）
- `intro.tex` 可选参考（用于确认任务描述措辞一致性）

> **写作规范（强制）**：起草完成后，必须对照 `../WRITING_STANDARDS.md` 逐条自查
> （数值/术语/逻辑一致性、禁止分点与破折号、禁止中式英语套语与无依据夸大断言、
> 加粗仅限规范场景等）。摘要尤其要核对："consistently outperforms all baselines"
> 一类断言必须与 `experiments.tex` 中的表格数据核对，若并非全面领先则改为
> "achieves the best or second-best result on the majority of..." 等可验证措辞。

---

## 总体流程

```text
第1步 读取 method.tex：提取模型名称、缩写、核心模块（3–5个）、任务描述
   ↓
第2步 读取 experiments.tex：提取数据集数量/名称、关键指标名称及最佳数值
   ↓
第3步 按固定5句式结构起草 abstract.tex，严格基于已有事实，不臆造数值
   ↓
第4步 输出独立文件 abstract.tex
```

---

## 第 1 步：从 method.tex 提取写作素材

读取 `method.tex`，记录：

```text
任务 (Task):           <e.g., traffic flow prediction / Ethereum malicious detection>
研究领域 (Domain):     <e.g., spatial-temporal forecasting / blockchain security>
模型名称 (Full name):  <e.g., Metapath-guided LLM-enhanced heterogeneous graph learning ...>
模型缩写 (Short name): <e.g., MPG-LLM>
核心模块列表:
  - 模块A: <名称 + 一句功能>
  - 模块B: ...
  - 模块C: ...
现有方法的核心局限（对应 P2 批评句）:
  - 局限1: <...>
  - 局限2: <...>
```

---

## 第 2 步：从 experiments.tex 提取实验数值

读取 `experiments.tex`，记录：

```text
数据集数量:  N 个
评估指标:    <指标1, 指标2, ...>
关键数值结果（仅取主表中我方最优数值）:
  - 指标1: XX.XX
  - 指标2: XX.XX
  - （最多列 3–4 个最能体现优势的指标）
Baseline 数量: M 个
```

> **Demo Mode 注意**：若 experiments.tex 中的结果为占位符，abstract 中需在数值后
> 标注 `\textcolor{red}{[placeholder]}` 或直接用"competitive"等定性描述代替数字，
> 待真实结果填入后再替换。

---

## 第 3 步：按 5 句式结构起草

### Abstract 固定结构（单段，共 5 个语义单元，约 250–350 词）

---

**S1 — 背景与任务重要性**（1–2 句）

句型选择（参照 intro.tex P1 措辞保持一致）：

```
"<Task> has become increasingly critical for <application domain>, 
attracting significant research attention in recent years~\cite{...}."
```

或直接切入：
```
"<Task> is one of the most critical research challenges in <domain>."
```

规则：
- 不超过 2 句
- 不重复 intro.tex P1 的原句，但措辞方向一致

---

**S2 — 现有方法不足**（1–2 句，以 "However" 起）

固定句型框架：
```
"However, existing methods predominantly <描述现有方法的主要技术路线>,
which <局限1，技术性描述>, and <局限2>."
```

规则：
- 必须以 "However" 或 "Despite ... however" 开头
- 局限必须直接对应 method.tex 中本文解决的问题
- 不要超过 2 句，保持精炼

---

**S3 — 提出方法**（1 句）

固定句型：
```
"To address these limitations, we propose <Full model name>, called \textbf{<Abbr>}."
```

或带架构描述：
```
"To address these limitations, we propose a novel <架构类型> for <task>,
termed \textbf{<Abbr>}."
```

规则：
- 这句话只负责"提出模型"，不展开细节
- 模型全称 + 缩写必须和 method.tex 一致

---

**S4 — 具体技术贡献**（3–5 句，以 "Specifically" 起）

句型框架：
```
"Specifically, <Module A的设计和功能，1句>.
<Module B的设计和功能，1句>.
[<Module C，1句>.]
[Building upon these, <整合机制或最终预测头，1句>.]"
```

规则：
- 每个核心模块写 1 句，过长可合并 2 个小模块为 1 句
- 动词多样化：we design / we propose / we introduce / we construct / we employ
- 不使用项目符号，必须是连续散文

参照示例（来自用户提供的 abstract）：
```
"Specifically, we design structured instruction prompts for contract opcode sequences
and apply LoRA to fine-tune a large language model for extracting deep semantic embeddings
from contract opcodes. Meanwhile, we abstract opcode sequences into an opcode trace graph
and employ a time-aware graph convolutional network to extract contract-level structural
embeddings. Building upon these representations, we propose a Gated Cross-Attention Fusion
(GCAF) module that leverages a cross-modal attention mechanism..."
```

---

**S5 — 实验结论**（2–3 句）

**先看参考文献摘要怎么写，再决定要不要列数据集名/指标名/具体数值**——不要预设"必须列出具体数字"。实测统计（交通流预测领域 8 篇参考论文的摘要）显示：

| 写法 | 出现频率 | 例子 |
|------|----------|------|
| 只说"N 个真实世界/公开数据集"，**不点名数据集，不点名指标，不给数值** | 多数（约 5/8，如 STPGNN、DSTAGNN、STADNN、DeepSTUQ、STDN） | "Experiments on seven real world traffic datasets verify our proposed method's effectiveness..." |
| 点名数据集名称，但仍不给指标名/数值 | 少数（如 ASPMformer） | "...on five public benchmark datasets, including PeMS03, PeMS04, ..., show that ASPMformer achieves competitive and consistent improvements over strong baselines." |
| 点名指标名称 + 具体数值（通常是分类/检测任务，AUC/F1/Recall 等一次性汇总指标，而不是回归任务在多个数据集/步长下变化的 MAE/RMSE 等指标） | 视任务类型，偏分类/检测类任务更常见 | 见下方 MPG-LLM 参考示例（Macro-AUC 0.9887 等） |

判断规则：
1. **默认不点名具体数据集、不点名具体指标、不写具体数值**，用"N widely-used public benchmarks"、"M competitive baselines"这类概括性说法——这是回归/预测类任务（时间序列预测、traffic forecasting 等，同一指标在多个数据集/多个步长下取值差异很大，无法用一两个数字概括全局结论）中的主流写法。
2. **仅当**任务是分类/检测/排序类，有 1–2 个"一次性汇总"型指标（如整体 AUC、F1、Accuracy）且参考文献摘要普遍这样写时，才在 S5 里给出具体数值（参照下方 MPG-LLM 示例）。
3. 拿不准时，直接读取本项目已解析的参考论文摘要段落，统计"点名数据集/指标/数值"的比例，按多数惯例执行，而不是套用固定模板。
4. 摘要正文里不要出现 `\citep{}` 引用的数据集名（如 `PEMS03~\citep{...}`）——数据集/引用细节留给正文 Experiments 部分。

句型框架 A（默认，不点名数据集/指标，回归/预测类任务推荐）：
```
"Extensive experiments on <N> widely-used public <domain> benchmarks [spanning <数据特征差异，可选>] show that
\textbf{<Abbr>} consistently outperforms <M> competitive baselines, while ablation studies confirm
the contribution of each proposed component[, and <可选：效率/泛化性等补充发现>].
These results indicate that <核心设计思路> offers an effective mechanism for <任务目标>."
```

句型框架 B（点名指标+数值，分类/检测类任务且参考文献多数这样写时使用）：
```
"Experimental results on <N> <数据集类型> datasets demonstrate that \textbf{<Abbr>}
significantly outperforms existing state-of-the-art methods across multiple evaluation metrics,
achieving <指标1> of <值1>, <指标2> of <值2>[, and <指标3> of <值3>].
These results indicate that \textbf{<Abbr>} can effectively <任务目标>, 
demonstrating practical applicability in real-world scenarios."
```

规则：
- 数值只来自 experiments.tex，不捏造
- 如果是 Demo Mode 且采用框架 B，用定性描述替代具体数值：
  `"...consistently achieves competitive performance across all benchmarks."`
- 末句可选："These results confirm that <核心设计思路> is both effective and generalizable."

---

## 写作质量检查清单（输出前逐项确认）

- [ ] 全文为单段，没有分行或 `\\` 换行
- [ ] S1 不超过 2 句，不重复 intro.tex 原句
- [ ] S2 以 "However" 开头，局限与方法解决方案直接对应
- [ ] S3 只有 1 句，模型全称和缩写与 method.tex 完全一致
- [ ] S4 中每个核心模块对应 1 句，动词不重复
- [ ] S5 已核对参考文献摘要的写作惯例，默认不点名具体数据集/指标/数值（回归预测类任务），仅在分类/检测类任务且参考文献多数点名时才写具体数值；数值只能来自 experiments.tex（Demo Mode 用定性描述）
- [ ] 全文词数符合用户要求（未特别说明时目标 250–350 词，若用户要求"N 词以内"则严格数一遍单词数确认 ≤ N）
- [ ] 不出现"In this paper, we..."流水账开头（用 S1 背景句开头）
- [ ] 不出现 section 引用如 "Section 3"（abstract 独立于正文）
- [ ] 不出现 `\cite{}` 引用（abstract 通常无引用）

---

## 输出文件

```latex
% abstract.tex
\begin{abstract}
<S1: 背景，1–2句>
However, <S2: 现有方法局限，1–2句>
To address these limitations, we propose <S3: 提出方法，1句>
Specifically, <S4: 技术细节，3–5句>
Experimental results <S5: 实验结论，2–3句>
\end{abstract}
```

用 `\input{abstract.tex}` 从主文档引入，或直接将内容嵌入主文档 `\begin{abstract}...\end{abstract}` 块中。

> **词数核查**：用户给出具体词数上限（如"300 词以内"）时，不要凭感觉估算，写完后用脚本精确核对：
> `python -c "print(len(open('abstract.tex', encoding='utf-8').read().split()))"`，
> 超出则逐句精简（优先删多余的从句/形容词，不要删掉贡献点），直到严格满足限制。

> **⚠️ Elsevier `cas-sc` / `cas-dc` 模板已知坑**：这两个模板的 `abstract` 环境（定义在
> `cas-common.sty`）通过 `\verbatimwrite` 把环境体逐字符原样写入 `\jobname.abs`，再用
> `\file_input:n` 读回排版。这个原始写入阶段**不会正常展开 `\input{abstract}`**（实测
> 会把结果吃掉、只剩残缺文本或空文件），导致编译出的摘要显示成字面量 `abstract` 或空白。
> **解决方法**：对 `cas-sc`/`cas-dc` 模板，不要在主文档的 `\begin{abstract}...\end{abstract}`
> 里写 `\input{abstract}`，而是把 `abstract.tex` 的纯文本内容直接复制粘贴进主文档的
> abstract 环境中（保留独立的 `abstract.tex` 作为本 skill 的规范产出文件，两者内容保持同步）。
> 编译后务必用 `pdftotext` 或直接读取 PDF 检查摘要页是否显示了真实文字而不是字面量 "abstract"。

---

## 参考示例（用户提供）

以下为高质量 abstract 示例，写作时参照其句式密度和模块组织方式：

```
Ethereum malicious detection is one of the most critical research in blockchain security.
However, existing methods predominantly model the Ethereum transaction network as a
homogeneous graph, which fails to effectively characterize the complex heterogeneous
interactions between externally owned accounts and contract accounts, and lacks the
capability for unified detection across multiple types of malicious accounts.
To address these limitations, we propose a novel approach that Metapath-guided
LLM-enhanced heterogeneous graph learning for Ethereum malicious detection, called MPG-LLM.
Specifically, we design structured instruction prompts for contract opcode sequences and
apply LoRA to fine-tune a large language model for extracting deep semantic embeddings from
contract opcodes. Meanwhile, we abstract opcode sequences into an opcode trace graph and
employ a time-aware graph convolutional network to extract contract-level structural
embeddings. Building upon these representations, we propose a Gated Cross-Attention Fusion
(GCAF) module that leverages a cross-modal attention mechanism to model the correlation
between opcode semantic features and structural features, and further employs a gating
mechanism to adaptively fuse semantic, structural, and on-chain transaction features into
comprehensive contract account representations. For externally owned accounts, initial node
representations are obtained by directly projecting transaction features through a
multi-layer perceptron. Furthermore, we construct four metapath-guided interaction patterns
and aggregate nodes and edges within each pattern to form the corresponding heterogeneous
subgraphs. An edge-aware heterogeneous graph attention network is then applied to perform
targeted message passing and neighborhood aggregation over each subgraph.
Experimental results demonstrate that MPG-LLM significantly outperforms existing
state-of-the-art methods across multiple evaluation metrics, achieving a Macro-AUC of
0.9887, a Macro-F1 of 0.6656, a detection rate of 0.8148, and a false alarm rate of 0.0328.
These results indicate that MPG-LLM can effectively distinguish malicious accounts from
normal ones on Ethereum, demonstrating practical applicability in real-world scenarios.
```
