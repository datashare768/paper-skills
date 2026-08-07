---
name: experiments-writing
description: >-
  Survey the datasets, baseline methods, and evaluation metrics used by already-analyzed
  reference papers, decide the experimental plan (public datasets only, baseline count
  aligned with references), and write a standalone LaTeX Experiments section (Experimental
  Setup / Main Results / Ablation Study / Parameter Sensitivity Analysis). Use after the
  idea-and-method-writing skill has produced method.tex and downloaded/parsed reference
  papers. Never fabricates the user's own method's performance numbers -- only real,
  citable baseline numbers or user-supplied real results go into result tables. Chinese
  triggers: 实验部分写作、experiments写作、数据集调研、baseline调研、消融实验、参数敏感性分析、
  主实验结果表格.
disable-model-invocation: true
---

# Experiments 部分写作

## 前置条件

已经用 `idea-and-method-writing` skill 完成了 idea 确认和 `method.tex`，并且参考论文已经下载、解析为 `papers/<slug>/text.md`（见该 skill 的场景 A/B）。

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

## 第 4 步：结果数字红线（必须遵守，不可绕过）

- **baseline 的数字**：只能使用 baseline 论文中**真实报告**过的数字，并标注引用来源；如果我方实验设置（数据划分、输入输出窗口长度等）与原论文不同导致数字不可直接复用，必须说明需要重新真实运行获得，不能编造替代。
- **用户自己方法的数字**：**必须来自真实跑出来的实验结果**，绝不凭空生成、绝不为了让结果"看起来最优"而编造性能数字或人为设计"比第二名高 5%-10%"这类提升幅度。这是学术诚信红线，不因用户要求而放开。
- 如果用户此时还没有真实实验结果：表格里用占位符（如 `XX.XX`）填充并显式标注 `% TODO: 替换为真实实验结果`，先把结构、引用、讨论文字的框架搭好。
- 一旦用户提供真实的实验日志/结果文件，直接读取并代入表格，再按第 5 步撰写讨论文字；不需要、也不允许在没有真实数据时"预先"编好一套数字。

## 第 5 步：结果分析写作（拿到真实数字后）

参考调研到的论文的写法：

- **Main Results**：先给整体表格，再按数据集/指标/预测步长分层讨论，指出哪些场景优势更明显、可能的原因
- **Ablation Study**：逐个模块讨论"去掉/替换后性能下降多少"，对应到方法部分的具体创新点
- **Parameter Sensitivity Analysis**：说明扫描了哪些超参数、最终选择依据、性能曲线走势

## 依赖 / 工具

复用 `idea-and-method-writing/scripts/extract_pdf.py` 解析出的 `text.md`；本 skill 的 `scripts/survey_experiments.py` 用于批量定位调研关键词所在位置。
