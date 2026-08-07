---
name: experiments-writing
description: >-
  Survey the datasets, baseline methods, and evaluation metrics used by already-analyzed
  reference papers, decide the experimental plan (public datasets only, baseline count
  aligned with references), and write a standalone LaTeX Experiments section (Experimental
  Setup / Main Results / Ablation Study / Parameter Sensitivity Analysis). Use after the
  idea-and-method-writing skill has produced method.tex and downloaded/parsed reference
  papers. Applies to any task type (time-series forecasting, classification, ranking,
  etc.), not just one domain. Baseline numbers must always be copied verbatim from the
  cited papers, never altered. The user's own method's numbers must come from real
  experiments when the work targets real publication; for explicitly non-publication
  practice/simulation projects, a disclosed placeholder estimate may be generated instead
  (never silently, always flagged in the table caption). Chinese triggers: 实验部分写作、
  experiments写作、数据集调研、baseline调研、消融实验、参数敏感性分析、主实验结果表格、占位实验结果.
disable-model-invocation: true
---

# Experiments 部分写作

## 前置条件

已经用 `idea-and-method-writing` skill 完成了 idea 确认和 `method.tex`，并且参考论文已经下载、解析为 `papers/<slug>/text.md`（见该 skill 的场景 A/B）。

调用本 skill 时，若用户未说明过，先确认一件事：**这份 Experiments 是否用于真实学术投稿/发表**，这决定了第 4 步"自己方法的数字"怎么填（真实发表 = 必须真实实验；个人练习/模拟流程 = 可用标注清楚的理论占位值）。

## 总体流程

```
第1步 调研参考论文的 Datasets / Baselines / Metrics
   ↓
第2步 确定我方实验方案（数据集必须公开、baseline 数量与参考论文对齐）
   ↓
第3步 搭建 experiments.tex 固定结构
   ↓
第4步 填充结果表格 —— 见下方「结果数字红线」，真实数字未就绪时用占位符
   ↓
第5步 有真实数字后，参考论文的写法撰写结果分析文字
```

---

## 第 1 步：调研参考论文的实验设置

对每篇 `papers/<slug>/text.md`，用关键词定位实验章节（Windows PowerShell 用 `Select-String`，其它平台用 `rg`/`grep`）：

```powershell
Select-String -Path papers\<slug>\text.md -Pattern "Dataset|Baseline|Metric" -CaseSensitive
```

或用脚本批量跑所有论文：

```bash
python scripts/survey_experiments.py papers/
```

定位到章节后通读，为每篇论文记录：

- **数据集**：名称、规模（节点数/时间步/时间跨度）、采样间隔、数据来源链接、是否公开
- **baseline 方法**：名称 + 发表 venue/年份（如 `GWNet [IJCAI 2019]`）
- **评价指标**：如 MAE / RMSE / MAPE，以及预测步长设置（如 15/30/60 min）
- **数据划分比例**：如训练/验证/测试 6:2:2

汇总成一张调研表（论文 → 数据集列表 → baseline 数量与名单 → 指标 → 数据是否公开），供第 2 步决策使用。

## 第 2 步：确定我方实验方案

- **数据集选择**：只保留调研表中标记为**公开**的数据集；参考论文用了几个公开数据集，我方原则上用相近数量（通常 4–7 个）。若某篇参考论文用的是私有/未公开数据，只借鉴其写法结构，不借用其数据和数字。
- **baseline 选择**：从调研表里挑选在多篇参考论文中反复出现、且公开可比的方法，凑够约 10 个，加上用户自己的方法共 11 个左右。**不要为了凑数量硬塞不相关方法**，最终数量服从参考论文的合理范围。
- **指标选择**：采用参考论文里普遍使用的指标（通常 MAE/RMSE/MAPE），预测步长设置向参考论文对齐（如 15/30/60 min 或多步平均）。

产出一份「实验方案」给用户确认：数据集清单（含来源链接）、baseline 清单（含引用）、指标清单。**确认后再进入第 3 步搭建 LaTeX。**

## 第 3 步：experiments.tex 固定结构

独立 LaTeX 文件 `experiments.tex`，用 `\input{experiments.tex}` 从主文档引入，结构固定为：

```latex
% experiments.tex
\section{Experiments}
\label{sec:experiments}

\subsection{Experimental Setup}

\subsubsection{Datasets}
% 数据集表格：名称/节点数/时间步/采样间隔/来源引用
...

\subsubsection{Baseline Methods}
% 逐个 baseline 一句话描述 + 引用，风格参考调研到的论文
...

\subsubsection{Implementation Details}
% 训练/测试划分比例、硬件、优化器、超参数、输入输出窗口长度等
...

\subsubsection{Evaluation Metrics}
% MAE/RMSE/MAPE 公式定义
...

\subsection{Main Results}
% 主结果表格（见下方红线），文字讨论跟随参考论文的引出/讨论套路
...

\subsection{Ablation Study}
% 逐个移除/替换创新模块，验证各模块贡献
...

\subsection{Parameter Sensitivity Analysis}
% 关键超参数（如隐藏维度、层数、窗口长度）扫描结果
...

% 视参考论文情况补充，如 Case Study / Efficiency Analysis / Visualization
```

## 第 4 步：结果数字规则（先确认项目性质，再决定怎么填）

**开始填表前，先明确这份 Experiments 是否用于真实学术投稿/发表**：

- **baseline 的数字**：无论哪种情况、无论任务类型（时序预测误差指标、分类 accuracy/F1、排序指标等），都**必须原样使用 baseline 论文中真实报告过的数字**，并标注引用来源。**不能对真实数字做任何"稍微改一下不要一模一样"式的人为改动**——那本质上是篡改别人已发表的实验结果，属于红线，不因是否用于发表、是否个人练习而改变。如果我方实验设置（数据划分、输入输出窗口长度等）与原论文不同导致数字不可直接复用，要说明需要重新真实运行获得，不能编造替代。
- **用户自己方法的数字**，分两种情况：
  1. **用于真实学术投稿/发表**：数字**必须来自真实跑出来的实验结果**，绝不凭空生成、绝不为了让结果"看起来最优"而编造性能数字或设计固定的提升幅度。真实结果没出来之前，表格里用占位符（如 `XX.XX`）+ `% TODO: 替换为真实实验结果`，先把结构、引用、讨论文字框架搭好。这是学术诚信红线，不因用户要求而放开。
  2. **用户明确说明不用于真实学术发表**（如个人练习项目、模拟标准科研流程、demo/教学用途）：可以基于 baseline 真实数字，生成一个**理论预期占位值**——在每一列（每个数据集/指标/任务）上，让自己方法的数字略优于该列最好的 baseline（误差类指标降低、准确率类指标提高），幅度保持合理、不同列不用同一个机械百分比。用 `scripts/generate_placeholder_results.py` 生成，避免手工编数字出现不合理规律：

     ```bash
     python scripts/generate_placeholder_results.py baselines.csv --seed 42 \
       --min-improve 0.05 --max-improve 0.10 --name Ours \
       --higher-is-better accuracy f1   # 只有"越大越好"的列才需要列在这里，误差类指标不用写
     ```

     `baselines.csv` 第一列是模型名，其余列是从参考论文原样抄来的真实 baseline 数字（每个任务类型的列名自定）。脚本只生成新增的占位行，不改动、不接触已输入的真实数字。生成后**必须在表格 caption 里用一句话明确标注**，例如：

     ```latex
     \caption{Performance comparison on <task/datasets>. Baseline numbers are taken from
     their original papers~\cite{...}. \textdagger~Results for our method are a
     theoretical/placeholder estimate and will be replaced with real experimental
     results once available.}
     ```

- 一旦用户提供真实的实验日志/结果文件，直接读取并代入表格，去掉占位标注，再按第 5 步撰写讨论文字。

## 第 5 步：结果分析写作（拿到真实数字后）

参考调研到的论文的写法：

- **Main Results**：先给整体表格，再按数据集/指标/预测步长分层讨论，指出哪些场景优势更明显、可能的原因
- **Ablation Study**：逐个模块讨论"去掉/替换后性能下降多少"，对应到方法部分的具体创新点
- **Parameter Sensitivity Analysis**：说明扫描了哪些超参数、最终选择依据、性能曲线走势

## 依赖 / 工具

复用 `idea-and-method-writing/scripts/extract_pdf.py` 解析出的 `text.md`；本 skill 的 `scripts/survey_experiments.py` 用于批量定位调研关键词所在位置；`scripts/generate_placeholder_results.py` 用于非发表模式下生成"自己方法"的占位数值（通用于任意任务类型，不限时序预测）。
