---
name: experiments-enrichment
description: >-
  Enrich an already-drafted experiments.tex by mining the project's parsed
  reference papers (papers/<slug>/auto/) for the experiment types, tables,
  and figures they contain (main results, ablation, efficiency, parameter
  sensitivity, statistical significance, robustness/perturbation, case
  study/visualization, decomposition-specific analysis, transfer/few-shot,
  memory cost, etc.), scores each candidate type by relevance to the current
  paper's own core contributions, and autonomously selects and drafts a small
  number of new subsections/tables/figures (Demo Mode placeholders anchored
  to existing numbers) without asking the user to pick from a menu. Use after
  experiments-writing has produced a base experiments.tex, when the user says
  the experiments section is "too thin/simple", asks to add more experiments
  based on what the reference papers did, or asks to turn this
  analyze-reference-papers-then-fill-in workflow into a reusable skill.
  Chinese triggers: 实验太少、补充实验、扩充实验部分、参考文献实验分析、
  根据参考论文补充表格和图、实验丰富度、自动挑选实验类型.
disable-model-invocation: true
---

# Experiments 部分实验丰富化（基于参考文献自动筛选）

## 前置条件

- 当前项目已用 `experiments-writing` skill 产出基础 `experiments.tex`（至少含 Main Results +
  Ablation）。
- 参考论文已解析为 `papers/<slug>/auto/<slug>.md` + `papers/<slug>/auto/tables/*.md`
  （见 `idea-and-method-writing` skill）。

> **写作规范（强制）**：本 skill 产出的所有新增段落/表格/图，必须对照 `../WRITING_STANDARDS.md`
> 逐条自查（先引用后出现图表、除 Introduction 贡献点外禁止分点、禁止破折号、数值锚点一致、
> 加粗仅标最优值等）。这是在已经写好的论文上做"增量编辑"，不是重写，自查范围可以只覆盖
> 新增内容，但新增内容与相邻已有段落的过渡句也要检查逻辑衔接。

## 核心原则：skill 自己做筛选，不把选项抛给用户

用户要的是"分析完直接给结果"，不是一个多选问卷。**默认自动选定候选项并直接产出**，除非用户
明确说"先给我看候选清单再定"。允许在最终回复里用一两句话说明选了什么、为什么，但不要用
`AskQuestion` 罗列选项让用户选。

## 总体流程

```text
第1步 跑 scripts/scan_reference_experiments.py，得到参考文献表格/图 caption + 粗分类标签清单
   ↓
第2步 读当前 method.tex，提炼本文 3-5 个核心模块/创新点关键词
   ↓
第3步 读当前 experiments.tex，列出已经覆盖的实验类型标签（避免重复）
   ↓
第4步 对候选类型打分排序，自动选出 Top 3-5 个新增项（见下方打分规则）
   ↓
第5步 为每个入选项生成：过渡段落（先引用后出现）+ 新表格/图（Demo Mode 占位，数值锚定现有表）
   ↓
第6步 插入 experiments.tex 对应位置，重新编译 main.tex 验证无错误
   ↓
第7步 更新 PROJECT_STATUS.md：记录选了什么、为什么、没选什么
```

## 第 1 步：扫描参考文献实验类型

```bash
python paper-skills/experiments-enrichment/scripts/scan_reference_experiments.py \
  --papers-dir papers --out reference_experiment_inventory.json
```

输出每条 `{slug, title, kind(table/figure), ref, caption, tag}`。`tag` 是关键词粗分类
（`ablation` / `decomposition_analysis` / `statistical_significance` /
`robustness_perturbation` / `transfer_few_shot` / `efficiency_memory` /
`parameter_sensitivity` / `case_study_visualization` / `training_curve` /
`framework_diagram` / `main_results` / `dataset_stats` / `other`），仅作粗筛，
最终判断仍需读该论文对应段落原文确认实验设计细节（尤其是 `case_study_visualization`
和 `other`，关键信息往往在正文而不在 caption 里）。

同时读 `references.bib` 或 `experiments.tex` 里的 `\citep{}` 确定哪些 `papers/<slug>` 是
当前论文**已引用的 baseline**（这些的实验设计参考价值最高，可以直接复用其 citekey 做
"following common practice~\citep{...}"），哪些是**未引用的补充素材**（仅借鉴实验类型，
不需要强行引入其模型名）。

## 第 2 步：提炼本文核心模块关键词

读 `method.tex` 的 Overview 小节，列出 3-5 个核心模块/创新点（例如："自适应分解"、
"自监督偏差量化"、"偏差调制图卷积"、"pivotal 节点识别"）。这是打分的关键依据。

## 第 3 步：列出已覆盖的实验类型

扫一遍现有 `experiments.tex` 的 `\subsection`/`\subsubsection` 标题和表格 caption，
标出已经有的类型标签（例如已有 `main_results`/`efficiency_memory`/`ablation`/
`parameter_sensitivity`），第 4 步打分时对这些类型直接排除，不重复添加。

## 第 4 步：打分规则（自动选择，不询问用户）

对第 1 步扫描到的、且第 3 步里"未覆盖"的候选类型标签打分：

- **+2 分**：该类型能直接对应第 2 步提炼出的某个核心模块/创新点（例如本文有"偏差量化"
  模块 → `robustness_perturbation`、`case_study_visualization` 直接相关，各 +2）。
- **+1 分**：该类型在 ≥2 篇参考文献中出现（尤其是已引用的 baseline 里出现），说明是
  该子领域的"标准动作"。
- **-1 分**：该类型和已有实验类型高度重叠（例如已有 main_results 就不要再加一个几乎一样
  的对比表）。
- **-2 分**：该类型和本文核心创新点无关、且只在"未引用的补充素材"论文里出现（例如与本文
  任务范式不同的不确定性量化框架，除非本文本身也做不确定性量化）。

按总分排序，**默认自动选 Top 3-5 个**（不要选太多，避免 Demo 论文实验部分臃肿到失真；
如果打分后只有 1-2 个正分候选，就只加这些，不要为了凑数硬加低分项）。

## 第 5 步：为每个入选项生成内容

每个新增项固定包含：

1. **过渡段落**：在新表格/图之前先用一句话引用它（`Table~\ref{tab:xxx}`/`Fig.~\ref{fig:xxx}`），
   遵守"先引用后出现"规则；并用 `following common practice~\citep{<来源论文citekey>}` 点出
   这个实验设计借鉴自哪篇参考文献（若来源论文未被引用，改用一般性表述不加引用，不要为了
   凑引用硬塞一个无关 citekey）。
2. **新表格/图**：
   - 表格数值必须是 Demo 占位数据，但要**锚定已有表格的数值**（例如复用 ablation 表里
     某一行的现成数值作为新表格的一行，或让新增的对比方法在 clean/baseline 场景下的数值
     与主表保持一致），不能凭空另起一套不相关的数字。
   - 图用与 `fig:overview` 相同的占位手法：`\begin{figure}` + 注释掉的
     `%\includegraphics{...}` + 详细 caption + `\label{}`，正文段落描述图中应该看到的
     趋势/现象（因为 Demo Mode 没有真实图片）。
   - 表格 `\textbf{}` 只标最优值，`\underline{}` 标次优值（若适用）；正文提及消融变体名
     用 `\emph{}`。
3. **讨论段落**：解释这个实验为什么支持本文的核心叙事（呼应第 2 步提炼的模块），不要只是
   复述数字。

## 第 6-7 步：插入、编译、记录

- 插入位置一般在 `Ablation Study` 之后、`Parameter Sensitivity Analysis` 之前，但按叙事
  逻辑可调整（例如"分解策略专项分析"更适合放在 Ablation 内部作为 `\subsubsection`）。
- 用 `latexmk -pdf -interaction=nonstopmode -halt-on-error main.tex` 编译验证零错误。
- 在 `PROJECT_STATUS.md` 追加一节：选了哪些新增项、各自的来源参考文献、打分理由，以及
  没选的候选和原因（方便下次对话或换一个论文方向时复用同一套判断逻辑）。

## 迁移到其他论文方向

本 skill 与具体研究方向（交通流预测等）无关，全部逻辑基于"读 method.tex 提炼核心模块 +
读参考文献实验清单 + 打分选择"，可直接在任何用 `idea-and-method-writing` +
`experiments-writing` 产出过 `method.tex`/`experiments.tex` 的新论文项目里复用。
