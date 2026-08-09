---
name: conclusion-writing
description: >-
  Write a concise, standalone LaTeX conclusion section (conclusion.tex) for an
  academic paper. Follows a fixed two-paragraph structure: (1) a self-contained
  main conclusion paragraph covering the proposed method, key components,
  experimental results, and broader significance; (2) a brief, non-verbose
  limitations and future work paragraph (2–3 sentences max, no over-emphasis).
  Must read method.tex and experiments.tex first to extract model name, modules,
  datasets, baselines, and result highlights before writing. Chinese triggers:
  结论部分写作、conclusion写作、conclusion.tex、总结部分、Conclusion and Future Work.
disable-model-invocation: true
---

# Conclusion 部分写作

## 前置条件

已完成 `method.tex`（方法）和 `experiments.tex`（实验），读取它们提取：方法名称、核心模块/创新点、实验数据集数量和名称、对比 baseline 数量和类别、主要结果亮点（最优指标/数据集）。

> **写作规范（强制）**：起草完成后，必须对照 `../WRITING_STANDARDS.md` 逐条自查。
> 结论段中总结实验效果的措辞必须与 `experiments.tex` 的真实数据一致，不能笼统写
> "consistently outperforms all baselines"，应改为如实反映主表结果的可验证表述
> （如"achieves the best or second-best result on the majority of evaluated metric
> combinations"）。
> 同时需检查：第一段若用一句话堆叠"提出方法+核心组件+实验结论+整体意义"多层信息，
> 应按语义拆成 2-3 句（`WRITING_STANDARDS.md` 第 18 章）；"Extensive experiments...
> demonstrate/demonstrated that..."这类句子的时态要统一（本文作者的实验动作/结果
> 用过去时，一般性结论用现在时，见第 16 章）。

---

## 固定结构（两段，独立文件 `conclusion.tex`）

```latex
% conclusion.tex
\section{Conclusion and Future Work}
\label{sec:conclusion}

% 第一段：主结论（必写，参考下方写作逻辑）
...

% 第二段：局限与展望（简短，2–3 句，不过度展开）
...
```

用 `\input{conclusion.tex}` 从主文档引入。

---

## 第一段写作逻辑（严格按此顺序，参考结构见下方示例）

1. **引出提出方法**："This paper proposes [ModelName], a [简洁描述架构核心] that ..."
2. **核心组件展开**：逐一点名方法章节的关键模块（与 method.tex 严格一致），说明每个模块的作用（动宾结构，不超过一句话一个模块）
3. **实验结论**："Extensive experiments on [N] [数据集描述] demonstrate that [ModelName] consistently outperforms [M] competitive baselines, including [类别列表]..."
4. **整体意义**：末句提炼方法背后的更广泛意义——"These results highlight / suggest that ..."，点出架构方向或技术路线的价值

**禁止**：
- 不要重复 Introduction 里已有的背景铺垫
- 不要用"In this paper, we first/then/finally"的流水账结构
- 不要超过 6–7 句话（保持紧凑）

---

## 第二段写作逻辑（简短，不过度强调局限）

格式：

```
Despite these contributions, [1–2 句点出局限，选最主要的 1–2 条，不要列举 4 条以上]。
In future work, we plan to [1–2 条具体可行的方向]。
```

**原则**：
- 局限最多写 2 句（不要单独成段、不要用 First/Second/Third 列举四五条）
- 未来工作最多写 1–2 个方向，要与方法强关联，不要泛泛地写"我们将 extend to more scenarios"
- 整段合计不超过 3–4 句话

---

## 参考写作示例（顶会风格，可以模仿此节奏）

```latex
\section{Conclusion and Future Work}
\label{sec:conclusion}

This paper proposes [ModelName], a [dual-branch / graph-enhanced / decomposition-based ...] framework
that integrates [Module A] for [功能A] with [Module B] for [功能B].
Through [核心机制，如 cross-attention fusion / adaptive graph learning / frequency decomposition],
the proposed model achieves [关键性质，如 effective bidirectional knowledge exchange / scalable
capacity via conditional computation].
[Optional: 一句补充第三个创新点（如多分辨率预测头、自适应调度等）]。
Extensive experiments on [N] real-world [任务类型] datasets demonstrate that [ModelName]
consistently outperforms [M] competitive baselines, including [类别，如 deep learning,
Transformer-based, and LLM-based methods], across multiple [evaluation dimensions].
These results highlight the effectiveness of [核心设计思路], suggesting that [方向性结论].

Despite these contributions, the current framework [1–2 句局限，如 relies on general-purpose
pretrained models / does not explicitly incorporate physical knowledge].
In future work, we plan to [1–2 条方向，如 explore domain-adaptive pretraining strategies and
integrate physics-informed modeling to improve interpretability].
```

---

## 执行步骤

1. **读取** `method.tex`：提取模型名称、各 subsection 对应的模块名和功能描述
2. **读取** `experiments.tex`：提取数据集数量/类型、baseline 数量/类别、主要结果（最优指标）
3. **起草第一段**：按上方逻辑，把提取的信息代入示例句式框架，检查是否 ≤ 7 句
4. **起草第二段**：选 1–2 条最主要局限，配 1–2 条强关联的未来工作方向，不超过 4 句
5. **输出** `conclusion.tex`，加 `\section{...}` 和 `\label{...}`
6. 提示用户在主文档中添加 `\input{conclusion.tex}`
