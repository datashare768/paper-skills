---
name: experiments-writing
description: >-
  Survey datasets/baselines/metrics from parsed reference papers, design the
  experimental plan, and produce a complete standalone LaTeX experiments.tex
  (Experimental Setup / Main Results / Ablation Study / Parameter Sensitivity
  Analysis / optional subsections). Operates in two modes: Academic mode
  (only real experimental results) and Demo mode (synthetic placeholder
  numbers for personal practice / pipeline testing / non-publication projects,
  with explicit Demo disclaimers). Use after idea-and-method-writing has
  produced method.tex. Chinese triggers: 实验部分写作、experiments写作、
  数据集调研、baseline调研、消融实验、参数敏感性分析、主实验结果表格、Demo实验、
  占位实验结果、模拟科研流程、流程测试.
disable-model-invocation: true
---

# Experiments 部分写作

## 前置条件

已经用 `idea-and-method-writing` skill 完成 idea 确认和 `method.tex`，并且参考论文已经下载、解析为 `papers/<slug>/text.md`（见该 skill 的场景 A/B）。

调用本 skill 时，首先判断项目性质：

* 如果用户明确说明用于真实论文投稿、学术发表、科研成果报告，则进入 **Academic 模式**。
* 如果用户明确说明仅用于个人娱乐、Demo、教学、流程测试、模板测试、练习项目或模拟科研流程，则进入 **Demo 模式**。
* 用户已经说明项目性质后，不要重复确认。

### Demo 模式特别说明

Demo 模式的目标是：

> 完整模拟一篇论文 Experiments 部分的组织、表格、数字关系和分析写法，使整个 LaTeX 项目能够完整展示和测试，而不是产生可用于真实论文发表的实验结论。

因此，在 Demo 模式下：

1. 允许生成 synthetic / simulated / placeholder 实验数字；
2. 允许生成 baseline 与 Ours 的完整结果表；
3. 允许生成 Ablation Study 数字；
4. 允许生成 Parameter Sensitivity 数字；
5. 允许根据这些模拟数字完成 Main Results、Ablation、Sensitivity 等分析文字；
6. 不要求用户首先提供真实训练日志；
7. 不因为缺少真实实验结果而停止 Experiments 部分的编写；
8. 所有模拟数字必须明确标记为 Demo / Synthetic / Placeholder，不得描述成真实实验结果。

---

# 总体流程

```text
第1步 调研参考论文的 Datasets / Baselines / Metrics
   ↓
第2步 确定我方实验方案
   ↓
第3步 搭建 experiments.tex 固定结构
   ↓
第4步 根据 Academic / Demo 模式填充结果
   ↓
第5步 撰写完整实验分析
```

---

# 第 1 步：调研参考论文的实验设置

对每篇 `papers/<slug>/text.md`，用关键词定位实验章节：

Windows PowerShell：

```powershell
Select-String -Path papers\<slug>\text.md -Pattern "Dataset|Baseline|Metric" -CaseSensitive
```

Linux / macOS：

```bash
rg -n "Dataset|Baseline|Metric|Experimental|Evaluation" papers/
```

也可以使用：

```bash
python scripts/survey_experiments.py papers/
```

定位后重点记录：数据集名称、规模（节点数/样本数/时间步）、时间跨度、采样间隔、数据来源、是否公开；baseline 名称、venue/年份；评价指标、prediction horizon、train/validation/test 划分；实现细节（batch size、optimizer、lr、hidden dim、epoch、硬件）。

汇总为调研表：`论文 → datasets → baselines → metrics → horizons → split → implementation details`

参考论文主要用于确定：实验章节应有哪些内容、数据集数量、baseline 数量、常见指标、表格布局、分析文字的组织方式。不要机械复制参考论文文字。

---

# 第 2 步：确定我方实验方案

## 2.1 Datasets

优先使用公开数据集，与任务类型匹配，与参考论文保持大致相同的数量（通常 4–7 个）。Demo 模式下如果某些数据集统计无法确认，可暂时写 `% TODO: verify exact dataset statistics before real experiments.`，但应尽量填写完整结构。

## 2.2 Baselines

优先从参考论文中选择重复出现、任务相关且具有代表性的 baseline。推荐结构：

```text
Traditional / Statistical → Deep Learning → Graph-based / Transformer-based → Recent SOTA → Ours
```

通常 8–12 baselines + Ours 较自然。不要为凑数加入明显无关方法。

## 2.3 Metrics

采用参考论文中普遍使用的评价指标（由任务决定，如时序预测 MAE/RMSE/MAPE，分类 Accuracy/F1/AUC，推荐 HR/NDCG/Recall 等）。

## 2.4 输出实验方案

Academic 模式下让用户确认后继续；Demo 模式下如果方案无明显歧义，直接继续，不因等待确认而停止任务。

---

# 第 3 步：experiments.tex 固定结构

创建独立文件 `experiments.tex`，由主文档 `\input{experiments.tex}` 引入：

```latex
% experiments.tex
\section{Experiments}
\label{sec:experiments}

\subsection{Experimental Setup}
\subsubsection{Datasets}
\subsubsection{Baseline Methods}
\subsubsection{Implementation Details}
\subsubsection{Evaluation Metrics}

\subsection{Main Results}
\subsection{Ablation Study}
\subsection{Parameter Sensitivity Analysis}

% Optional:
% \subsection{Efficiency Analysis}
% \subsection{Case Study}
% \subsection{Visualization}
```

## 3.1 多数据集结果必须合并为一个表格（重要）

**同一个 subsection（Main Results / Ablation Study / Efficiency 等）如果在多个数据集上跑实验，必须合并成一张表，而不是每个数据集单独一张表。** 这是主流顶会/顶刊论文的通用排版惯例（例如 STPGNN Table 2、DeepSTUQ Table II 都是把 PEMS03/04/07/08 四个数据集堆叠在同一张表里），逐数据集单独开表是不推荐的反例。

合并表格的标准样式（Metric 为行、Model 为列、Dataset 用 `\multirow` 纵向合并）：

```latex
\begin{table*}[t]
  \centering
  \scriptsize
  \resizebox{\textwidth}{!}{%
  \begin{tabular}{l|l|ccccccccccc}
    \toprule
    Dataset & Metric & Baseline1 & ... & \textbf{OurModel}$^\dagger$ \\
    \midrule
    \multirow{3}{*}{PEMS03} & MAE  & ... & ... & ... \\
     & RMSE & ... & ... & ... \\
     & MAPE & ... & ... & ... \\
    \midrule
    \multirow{3}{*}{PEMS04} & MAE  & ... & ... & ... \\
     & RMSE & ... & ... & ... \\
     & MAPE & ... & ... & ... \\
    \bottomrule
  \end{tabular}%
  }
\end{table*}
```

用 `scripts/build_latex_table.py` 的 `--combine` 参数一步生成（见第 6 步工具清单），**不要**为每个数据集分别调用脚本生成分表再手动拼接章节。适用范围：

- **Main Results**：所有数据集合并为一张表（`--label tab:main_results`）。
- **Ablation Study**：如果消融实验也在多个数据集上做（如 PEMS04 + PEMS08），同样合并为一张表（`--label tab:ablation`），不要每个数据集单开一张。
- **Parameter Sensitivity / Efficiency Analysis** 等如果也涉及多个数据集，同样适用本原则；若只在单一数据集上做（如仅 PEMS04 的敏感性分析），保持单表即可，无需强行合并。
- 模型列统一显示真实模型名（如 `DAPGN`），不要用占位符 `Ours` 展示给读者；`--ours-label` 参数可以把内部数据里的 `Ours` 行替换成实际模型名再渲染。

### 3.1.1 另一种合并方向：Variant/Model 为行，Dataset 为列分组

Ablation Study 等"行数不多但每个数据集要展示多个指标"的场景，也可以反过来：第一列是消融变体（或 baseline 模型），后面按数据集分组，每个数据集下面再拆 MAE/RMSE/MAPE 三个子列（`\multicolumn` + `\cmidrule`）。做法：

1. 把各数据集的结果 CSV 按 `model` 列对齐合并成一张宽表，列名加数据集前缀，如 `PEMS04_MAE,PEMS04_RMSE,PEMS04_MAPE,PEMS08_MAE,PEMS08_RMSE,PEMS08_MAPE`。
2. 调用 `build_latex_table.py`（不加 `--transpose`）并传 `--dataset-groups "PEMS04:3,PEMS08:3"`：脚本会自动去掉列名里的数据集前缀，只在表头显示裸指标名（`MAE`/`RMSE`/`MAPE`），并在每个数据集分组内分别计算 bold/underline。

```bash
python scripts/build_latex_table.py wide.csv \
    --dataset-groups "PEMS04:3,PEMS08:3" \
    --label tab:ablation \
    --caption "Synthetic ablation study on PEMS04 and PEMS08." \
    --out results/table_ablation.tex
```

两种合并方向（Dataset 为行 vs. Dataset 为列分组）都可以接受，按具体表格的行数/列数选择更紧凑的一种；核心原则不变——**同一 subsection 里的多数据集结果永远合并进同一张表**。

---

# 第 4 步：结果数字规则

## 4.1 Academic 模式

**Baseline**：优先在完全相同实验协议下自行复现；或使用论文明确报告且设置一致的数字。数据划分、horizon、输入长度、preprocessing、metric 定义任何一项不同，则不能直接把原论文数字描述为严格可比结果，应用 `--` 或 `XX.XX` 并标注 `% TODO: replace with reproduced result`。

**Ours**：必须使用真实实验结果。缺失时用 `XX.XX` + `% TODO: replace with real result`，不得编造。

## 4.2 Demo 模式

用户明确说明为 personal demo / entertainment / educational demo / workflow test / LaTeX test / simulated research / non-publication exercise 后，**不再询问是否用于学术发表，直接进入 Demo 模式**。

### 4.2.1 Demo baseline 数字

**A. 可从参考论文可靠读取**：使用真实报告数字，不修改，正确引用，不把不同设置的数据宣称为严格公平比较。

**B. 无法取得统一可比的 baseline 数字**：允许直接生成 synthetic baseline results，caption 明确写：

```latex
\caption{Synthetic performance comparison constructed for demonstration purposes.
All numerical results in this table are simulated placeholders and do not
represent reproduced or reported experimental results.}
```

### 4.2.2 Demo 中 Ours 的数字

允许生成 synthetic/placeholder Ours 数字，生成原则：

- **Lower-is-better**（MAE/RMSE/MAPE/MSE 等）：Ours 通常优于较强 baseline，改进幅度在 0.5%–8% 之间随机变化，难度高的数据集提升较小，优势更匹配的数据集提升稍大。
- **Higher-is-better**（Accuracy/F1/AUC/NDCG 等）：相对最好 baseline 有合理小幅提升，避免所有列刚好 +1% 等机械规律。

用脚本生成，不要手工编数字：

```bash
python scripts/generate_demo_results.py \
    --seed 42 \
    --datasets datasets.json \
    --baselines baselines.json \
    --metrics MAE RMSE MAPE \
    --ours "Ours"
```

或使用更简单的 `generate_placeholder_results.py`（仅生成 Ours 行，baselines 已有真实数字时用）：

```bash
python scripts/generate_placeholder_results.py baselines.csv \
    --seed 42 --min-improve 0.05 --max-improve 0.10 --name Ours \
    --higher-is-better acc f1 > filled.csv
```

### 4.2.3 Demo 数字必须具有合理结构

- **RMSE ≥ MAE** 通常成立；MAPE 保持合理数量级
- **Horizon 越远误差越高**（MAE/RMSE/MAPE 随步长单调递增）
- **方法排名有层次**：老旧 baseline < 有竞争力的 baseline < recent SOTA ≈ Ours（允许局部排名变化）
- **Ours 不要求每格都第一**，更自然的 Demo 结果是"多数指标最优，少数指标次优"
- **禁止机械规律**：Ours 永远精确提升 5%、所有 ablation 都下降 3%、所有小数尾数模式一致等均禁止

### 4.2.4 Demo Ablation Study

基本规律：Full Model 整体最优；去掉关键组件性能下降；不同模块贡献程度不同（主要/适中/互补）；不能机械写"每去掉一个模块固定下降 2%"。模块名称**必须与 method.tex 中的真实模块名称一致**，不得凭空发明。

### 4.2.5 Demo Parameter Sensitivity

模拟关键参数扫描（hidden dim / num layers / input window / lr 等），结果体现合理趋势：性能先改善后趋于饱和或下降，曲线不要完美对称，默认参数处于性能较好区域但不要求极端明显优势。

### 4.2.6 Demo 统一声明

在 Experiments 开头统一加入：

```latex
\paragraph{Demo Disclaimer.}
The experiments in this section are constructed solely for demonstration
and pipeline-testing purposes. Unless explicitly stated otherwise, numerical
results are synthetic placeholders rather than outcomes of actual model
training or reproduction.
```

---

# 第 5 步：实验分析写作

## 5.1 Academic 模式

必须基于真实实验结果分析，不要提前声称 SOTA 除非真实数字支持。

## 5.2 Demo 模式

允许根据 synthetic 数字完整生成实验分析，措辞体现 Demo 属性：

- 推荐："The synthetic results suggest..." / "Within this synthetic setting..." / "The demo results illustrate..."
- 避免："Experiments prove that..." / "Our method achieves state-of-the-art..."

## 5.3 Main Results 分析结构（四段式，参考顶会写法）

1. **总体结果**：与多少 baseline 比较、覆盖多少数据集、使用哪些指标、Ours 总体表现
2. **不同数据集**：哪些数据集优势明显/差距较小，数据集特征可能的影响
3. **不同预测步长**（如有）：重点讨论 long-term forecasting
4. **方法解释**：把性能趋势与 method.tex 中的具体模块对应（不能只写"因为我们方法更好"，要联系具体设计）

## 5.4 Ablation 分析

逐组件讨论（Full / w/o A / w/o B / w/o C），说明：性能变化绝对值/相对值、贡献最大的模块、模块互补性、与 Method 设计动机的对应。

## 5.5 Parameter Sensitivity 分析

说明：扫描范围、性能变化趋势、最终选择、参数过小/过大各自的问题（不够表达力 / 过拟合 / 优化困难），解释趋势而非只说"X 最好所以选 X"。

---

# 第 6 步：Demo 模式下的默认执行行为

当用户已明确说明项目是个人娱乐/Demo/教学/模拟科研流程/测试 LaTeX/非投稿用途后，**不再询问是否用于学术发表，直接执行**：

1. 阅读 `method.tex`，提取方法名称和创新模块
2. 调研参考论文 experiments（datasets/baselines/metrics）
3. 确定实验方案（数据集/baseline/指标）
4. 创建完整 `experiments.tex`
5. 生成 synthetic main results（含 baseline + Ours）
6. 生成 synthetic ablation results
7. 生成 synthetic parameter sensitivity results
8. 填充全部 LaTeX tables（含 bold/underline/caption 声明）
9. 撰写完整 Main Results 分析（四段式）
10. 撰写 Ablation Study 分析
11. 撰写 Parameter Sensitivity Analysis 分析
12. 添加 Demo Disclaimer
13. 检查引用、label、table formatting 和 LaTeX 语法

除非缺少会导致实验设计完全无法判断的核心信息，否则不要中途停止等待用户确认。

---

# 第 7 步：最终交付内容（Demo 模式）

至少一次性产出完整的 `experiments.tex`，包含：

- Experimental Setup（Datasets / Baseline Methods / Implementation Details / Evaluation Metrics）
- Main Results（Table + Discussion）
- Ablation Study（Table + Discussion）
- Parameter Sensitivity Analysis（Results + Discussion）
- Demo Disclaimer

如果项目结构允许，还可同时生成：`results/demo_main_results.csv` / `results/demo_ablation.csv` / `results/demo_sensitivity.csv` / `scripts/generate_demo_results.py`。所有 synthetic 数据统一使用固定随机 seed，以便重复生成。

---

# 核心原则

| 模式 | 数字来源 | 分析文字 | 标注要求 |
|------|----------|----------|----------|
| Academic | 必须真实实验 | 只基于真实数字 | 缺失用 TODO |
| Demo | synthetic/placeholder | 可基于 synthetic 数字，措辞体现 Demo | 统一 Demo Disclaimer |

Demo 模式的重点是：**让用户能够完整测试论文 Experiments 写作、LaTeX 表格、结果分析和整个科研写作 pipeline**。不能因为缺少真实训练日志而只生成 `XX.XX`，也不能在用户已明确 Demo 用途之后不断要求提供真实实验结果。

---

# 工具清单

| 脚本 | 用途 |
|------|------|
| `idea-and-method-writing/scripts/extract_pdf.py` | PDF 文字+图片提取 |
| `scripts/survey_experiments.py` | 批量定位 Dataset/Baseline/Metric 章节位置 |
| `scripts/generate_placeholder_results.py` | baselines 已有真实数字时，生成 Ours 占位行 |
| `scripts/generate_demo_results.py` | Demo 模式下生成完整的 synthetic 对比结果（含所有 baselines） |
| `scripts/build_latex_table.py` | CSV → 带 bold/underline/caption 声明的完整 LaTeX 表格 |
| `scripts/split_by_dataset.py` | 把 `generate_demo_results.py` 生成的宽表拆分成每个数据集一个 CSV，供 `build_latex_table.py` 使用 |

`build_latex_table.py` 关键参数：

- `--transpose`：单数据集内 Metric 为行、Model 为列（DeepSTUQ/STPGNN 单表风格），替代默认的 Model 为行、Metric 为列。
- `--combine "Name1:csv1.csv" "Name2:csv2.csv" ...`：把多个数据集（相同的 model/metric 结构）合并为一张表，自动加 `Dataset` 列（`\multirow`），**Main Results / Ablation 等涉及多个数据集时必须使用**（见 3.1）。
- `--ours-label DAPGN`：把内部数据行名 `Ours` 渲染成实际模型名称，而不是显示占位符 `Ours`。
- `--higher-is-better acc f1`：指定哪些列/指标是越大越好（默认全部越小越好）。
