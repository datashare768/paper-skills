# 论文写作通用规范（强制，所有 *-writing skill 写作/自检时必读）

本文件是所有 `paper-skills` 下写作类 skill（abstract-writing / introduction-writing /
related-work-writing / idea-and-method-writing / experiments-writing / conclusion-writing）
共享的强制写作规范。每个 skill 在**起草完成后**、以及用户要求"检查/润色/符合学术规范"时，
都必须逐条对照本文件自查，而不是只依赖 skill 自身模板。

---

## 1. 图表引用顺序

- 正文中每个 `\ref{fig:...}` / `\ref{tab:...}` 对应的图或表，都必须在文中先有引用句
  （如 "As shown in Table~\ref{tab:xxx}..." 或 "Table~\ref{tab:xxx} reports..."），
  再出现该图/表环境本身（`\begin{figure}`/`\begin{table}` 或 `\input{results/table_xxx}`）。
- 检查方法：在最终 `.tex` 源码顺序里，每个 `\label{fig:xxx}`/`\label{tab:xxx}` 所在环境之前，
  必须已经出现过对应的 `\ref{fig:xxx}`/`\ref{tab:xxx}`（可以是同一段落里紧邻的引导句）。
- 若某表/图目前是"表先出现、引用句在表后面才提到"，须在表格前补一句先行引用的过渡句，
  不能仅在表后补述。

## 2. 段落写作风格（除 Introduction 贡献点外，全文禁止分点）

- **只有 Introduction 中列出论文贡献（contributions）时可以使用 `itemize`/`enumerate`**。
  其余任何位置（Related Work、Method、Experiments 的 baseline 介绍/ablation 变体介绍/
  局限与展望等）都必须写成连续散文段落，不能用项目符号列表拆分。
- 段落内部禁止使用编号式弱连接词来组织逻辑，包括但不限于：
  `1) 2) 3)`、`(i) (ii) (iii)`、`First, Second, Third, Fourth, Finally,`、
  裸露的 `first/second/third` 作为段内顺序词。
  应改写为依靠语义连接词（`while`、`In parallel`、`Moreover`、`Building on this`、
  `Correspondingly` 等）组织的连贯散文，保持前后逻辑衔接。
- 禁止使用破折号（em dash，`--` 用作插入语/口语化停顿，如 `A -- B -- C`）来组织句子。
  应改写为逗号或重新组织句子结构（不要改用冒号顶替，见下一条冒号规则）。
  **例外**：数字范围（`2--6\%`）、章节范围（`Sections~\ref{a}--\ref{b}`）、复合名词连接
  （`accuracy-efficiency trade-off`）等 LaTeX 排版惯例中的连接符号不算"破折号"，可保留。
- **段落中的句子内部禁止使用冒号（`:`）来引出举例、列举或解释性从句**，例如
  `...costs: GWNet, a lightweight model; DSTAGNN, ...`（用冒号罗列同位语）或
  `...consistent with the intended role of the deviation score: when the input
  departs...`（用冒号引出解释性分句）。这类写法应改写为：
  - 用 `namely`、`including` 引出同位语列举：
    `three baselines with markedly different costs, namely GWNet, ...; DSTAGNN, ...`；
  - 用 `in that`、`where`、`such that` 引出解释性从句，融入同一个句子：
    `consistent with the intended role of the deviation score, in that when the
    input departs...`；
  - 或者直接拆成两句，用 `Specifically,`/`In particular,` 开头承接：
    `...close to the strongest baseline. Specifically, DAPGN improves on ...`。
  **例外（结构性冒号，允许保留）**：引出后面的 `\begin{equation}`/`\begin{itemize}`
  等独立展示环境的引导句（如 `Their formal definitions are as follows:` 后接公式，
  或 Introduction 贡献列表前 `the main contributions of this paper are as follows:`
  后接 `itemize`），因为这是把公式/列表当作句子的直接延续，而不是在同一段散文句子
  内部用冒号组织举例或从句；此外数字比例记号（如训练集划分 `6:2:2`）也不算句内冒号，
  可以保留。写完后用正则 `[a-zA-Z]: ` 全文检索，命中的位置逐条确认是否为上述例外，
  非例外一律按本条改写。

## 3. 前后一致性自检（逐段检查全文后再收尾）

写作/润色收尾前，必须逐段过一遍全文，重点排查三类不一致：

1. **数值一致性**：同一数值/百分比在摘要、引言、方法、实验、结论中反复出现时，
   必须与表格中的原始数据严格对应。任何"提升 X%--Y%"之类的区间描述，都要用表格
   真实数值重新算一遍再写，不能凭感觉估计范围。若某数据集上本方法并非全面领先
   （如被单个 baseline 打平或反超），措辞要如实反映，不能笼统写"consistently
   outperforms"。
2. **术语一致性**：同一模块/机制/变量在不同小节中的命名必须完全一致（例如
   "deviation-modulated pivotal graph convolution" 不要在别处写成
   "deviation-aware graph convolution" 这种看似同义但字面不同的说法，除非刻意用
   `\emph{}` 强调是同一概念的复现）。
3. **逻辑一致性**：某个结论（如"在 A、B 数据集上提升最明显"）在多处重复提及时，
   支撑该结论的数据集组合、原因解释必须前后一致，不能一处说"A、B 最明显"，
   另一处又说"A、C 最明显"却没有解释差异。

## 4. 语法与学术用词检查

逐段检查，重点排查：

- **中式英语套语**（必须删除或改写）：如 `it is worth noting that`、
  `plays a vital/crucial/important role`、堆砌的 `In this paper, we...` 开头、
  滥用的 `In recent years,`、`With the rapid development of...` 等空洞套语。
- **夸大与无依据断言**：`significantly`、`greatly`、`remarkably` 等程度副词若无
  数据支撑必须删除或替换为可验证的表述；`consistently outperforms all baselines`
  类断言必须与表格数据核对，改为"achieves the best or second-best result on the
  majority of..." 等可验证措辞。
- **语义错误**：主谓不一致、指代不清（it/this 指向模糊）、比较对象缺失
  （"higher than" 没写清楚与谁比较）。
- **领域用词精度**：领域术语要用该子领域公认的标准名词（如 traffic *flow* vs.
  traffic *speed* 不能混用；"anomaly" vs. "deviation" 若论文明确区分了两者的含义，
  不能在不同章节混用造成读者误解）。
- **禁止 `(e.g., ...)` 括号举例写法**：正文中不允许出现 `(e.g., ...)` 这种把例子
  塞进括号里的写法（例如 `recurring periodic patterns (e.g., daily commute peaks)`），
  这类写法读起来像是临时补充的注解，破坏了论文正文应有的连贯叙述感。必须将例子改写
  为融入主句的从句或短语，常见改法：
  - 用 `such as ...`（不加括号）直接续写在主句后：
    `recurring periodic patterns, such as daily commute peaks,`；
  - 用 `including ...`：
    `several of our reference baselines, including STPGNN~\citep{...},`；
  - 用 `comprising ...` / `covering ...` 等动名词短语引出例子。
  注意 `(i.e., ...)`（同义改写/精确定义，而非举例）不受此规则限制，可以保留。
  写完后用正则 `e\.g\.` 全文检索确认清零。
- **避免用 "real" 刻意强调"真实性"**：小节标题、图表标题（`\caption` 首句）、
  以及正文中都不应出现 `real`/`Real` 这个词去强调数据、地图、依赖关系等"是真的"
  （例如 `Spatial View of Pivotal Nodes and Real Dependency Strength`、
  `computed from the real PEMS08 traffic tensor`、`a real OpenStreetMap basemap`）。
  数据是否来自公开数据集应该在 Demo Disclaimer 或方法描述中一次性说明清楚，
  不需要在每处重复强调"real"来对比合成/占位数据。常见改法：
  - 直接删除 `real` 这个修饰词（如果上下文已经清楚这是观测数据）：
    `the real PEMS08 traffic tensor` → `the PEMS08 traffic tensor`；
  - 需要强调"来自公开数据集"而非模型/合成时，改用 `public`、`observed`、
    `data-derived`、`actual`、`genuine`、`true`（`true GPS coordinates` 这种
    习惯搭配可保留）等更精确的词，而不是泛化的 `real`；
  - 标题中如果原本用 `Real X` 修饰名词，直接删掉 `Real`，让标题回到中性的
    名词短语（如 `Spatial View of Pivotal Nodes and Dependency Strength`）。
  写完后用正则 `\breal\b` （忽略大小写）全文检索确认清零（脚本生成的图片标题
  本身一般不含该词，无需修改）。
- **段落正文中非必要不要使用斜体（`\emph{}`）**：`\emph{}` 只在下列"必要"情形下
  使用，其余情况一律写成普通正文：
  - **术语的首次正式定义**：一个贯穿全文反复使用的核心概念/原理名称，在其被
    正式定义的那一处（通常紧跟公式或紧跟"we define ... as follows"式的定义句）
    可以用 `\emph{}` 标出一次，例如 `are used to define the \emph{deviation
    score} for each node`、`enforcing the principle of \emph{relative distance
    consistency}`。**同一术语在全文其余位置（包括摘要、引言的预告性提及、结果
    讨论）一律不再加斜体**，直接用正常字体书写。
  - **方法架构中被正式命名的模块/组件**，在总览段落第一次引出每个模块名称时
    可以用 `\emph{}` 标出（如 `A \emph{Spatio-Temporal Embedding} module
    encodes...`），帮助读者对照架构图识别模块边界；模块名称在其余章节
    （如详细方法小节标题、结果讨论）不需要再重复斜体。
  - **禁止**用 `\emph{}` 做纯修辞强调，包括但不限于：强调疑问式短语
    （`\emph{how much}`、`\emph{how far}`）、强调副词/形容词
    （`\emph{adaptively}`、`\emph{statically}`、`\emph{pivotal}`）、强调
    对比名词（`\emph{flow}` vs. `\emph{speed}`、`\emph{prediction}`）、
    强调消融/对比实验的变体名称（`\emph{w/o Decomposition}`、`\emph{None}`、
    `\emph{STL}`——这些变体名称在结果表格里本身就是纯文本，正文提到时也应保持
    纯文本，不要额外加斜体）、以及**整句话斜体**（用斜体整句标注免责声明或
    强调性说明，如 `\emph{Under Demo Mode, no actual training was
    performed...}`，应直接去掉 `\emph{}` 变成普通正文句）。
  写完后用正则 `\\emph\{` 全文检索，逐条确认是否属于上面两类"必要"情形，
  不属于的一律去掉 `\emph{}` 只保留花括号内的文字；新写句子需要强调时应优先
  依靠句子结构本身（如改写措辞、调整语序）来传达强调，而不是加斜体，从一开始
  就避免非必要斜体，不要写完再回头改。
- **避免"Motivated by the lack of X"式的绕弯子开场**：提出方法/模块的句子不要
  先用 `Motivated by the lack of ...`、`Despite the absence of ...`、
  `Given the lack of ...` 这类间接重述局限的方式起头（尤其是该局限已经在
  Introduction/Related Work 中充分论证过，此处再复述等于炒冷饭），应直接陈述
  "提出了什么方法，具备什么机制"，把方法名称和核心机制一次性交代清楚。例如把
  `Motivated by the lack, in existing methods, of an explicit deviation
  signal that couples decomposition and graph construction, we propose
  DAPGN, a unified framework that couples ...` 改写为
  `We propose the Deviation-Aware Pivotal Graph Network (DAPGN), a unified
  framework that couples adaptive sequence decomposition with dynamic
  pivotal-node-centered graph learning through an explicit, self-supervised
  deviation signal.`，直接从 `We propose ...`/`This paper proposes ...`
  开始。只有当该局限此前从未被提及（不属于回顾性重复）时，才允许用一句简短的
  因果句引出，但仍要避免 `Motivated by the lack of` 这个具体套语，改用更直接的
  因果连词（如 `To address this, ...`、`To this end, ...`）。

## 5. LaTeX 符号/下标/上标语法检查

检查全文所有数学表达式：

- 同一符号（如 `D`、`\delta`、`K`）不能在不同小节里表示两个不同的量。若确实需要
  复用字母，必须显式重新定义或换用不同符号（如区分嵌入维度 `D` 与距离 `\rho`）。
- 每个新引入的公式变量都要在首次出现处给出定义（"where ... denotes ..."）。
- 关键公式建议加 `\label{eq:xxx}`，正文引用统一用 `\eqref{eq:xxx}`，
  不要手写硬编码的公式编号（如 `Eq.~(17)`），否则后续增删公式会导致编号错位。
- 检查上下标是否使用了正确的 LaTeX 语法（`_{...}`/`^{...}` 多字符必须加花括号，
  不能写成 `x_i,t` 这种只作用于第一个字符的错误写法）。

## 6. 加粗（`\textbf{}`）使用规范

正文段落中**非必要不加粗**。仅以下情形允许使用 `\textbf{}`：

- ✓ 表格列标题（表头行，包括方法名列）
- ✓ 表格中标记最优结果的数值（且必须真的是该列/行的最优值，不能因为是"本文方法"
  就整行加粗——若本文方法在某个指标上不是最优，应改用 `\underline{}` 标记次优或不加标记）
- ✓ 图注中的子图标签 `(a)(b)(c)...`
- ✓ 算法/定理中的关键词标签（部分期刊约定）

以下情形**禁止**加粗：

- ✗ 正文中首次提出模型全称/缩写（如 `\textbf{Deviation-Aware Pivotal Graph Network
  (DAPGN)}`）——首次提出模型名不需要加粗，直接用正常字体即可。
- ✗ 正文中提及消融变体名称（如 `\textbf{w/o Decomposition}`）——应改用 `\emph{}` 斜体。
- ✗ 用加粗代替其他强调手段（应优先用句子结构本身传达重点，而非加粗）。

## 7. 章节交叉引用（Section~\ref）的使用限制

- **除 Introduction 结尾的"路线图"段落**（即 "The remainder of this paper is
  organized as follows. Section~\ref{...} reviews... Section~\ref{...}
  presents..." 这一段，用于概述全文结构）**外，正文任何其他位置一律禁止使用
  `Section~\ref{...}`/`Sec.~\ref{...}` 这类章节交叉引用**，包括但不限于：
  - Method 正文、Algorithm 环境中的 `\Comment{}` 注释（不能写
    `\Comment{Section~\ref{sec:xxx}}`，应改写为该步骤本身的简短功能描述，如
    `\Comment{pivotal node identification}`）；
  - Experiments 正文中"如 Section~\ref{sec:pivotal} 所述"这类回指表述；
  - 图/表的 `\caption{}` 内部。
- **替代写法**：需要指代"前文/后文某处已定义的概念"时，使用不依赖章节编号的
  过渡语，例如 "as detailed below" / "as detailed above" / "introduced
  earlier" / "the adaptive decomposition module described above" /
  "the aggregation/distribution score used for pivotal node identification"，
  直接用该模块/概念的名称重新表述，而不是给出一个可能因增删章节而错位的编号
  引用。
- **原因**：章节编号在多轮增删小节（如新增 Robustness、Case Study 等
  subsection）后很容易发生偏移或指代错误，且部分期刊排版会重新编号章节，
  裸露的 `Section~\ref` 在这种场景下比直接的语义重述更脆弱、更难自查正确性。
- 检查方法：对定稿的 `.tex` 全文搜索 `Section~\ref`/`Sec\.~\ref`，命中的位置
  除了 Introduction 路线图段落外，一律需要改写为不含章节编号引用的表述。

## 8. 图/表 caption 内禁止交叉引用其他图/表

- `\caption{}` 内部只能描述**当前这个图/表自身**的内容（各面板含义、数据来源、
  归一化方式、Demo 声明等），**禁止**在 caption 里出现指向其他图/表的
  `Fig.~\ref{fig:yyy}`/`Table~\ref{tab:yyy}`（`yyy` 不是当前 float 的
  label）。常见误用场景包括："锚定到 Table~\ref{tab:main_results} 中的对应
  数值"、"目标节点与 Fig.~\ref{fig:pivotal_network} 中相同"等。
- **替代写法**：把跨图表的关联关系改写成不依赖具体 `\ref` 的描述性语言，例如
  "anchored to the corresponding overall main-results value"、"the same
  highlighted pivotal node identified earlier"，把交叉引用挪到正文段落中
  （正文段落里引用其他图表是允许且推荐的，只是不能出现在 caption 内部）。
- 检查方法：对每个新增/修改的 `\caption{...}` 内容，搜索其中是否出现
  `\ref{fig:`/`\ref{tab:` 且该 label 不等于本 float 自身的 `\label{}`；命中
  则需要改写为描述性语言并将真正的交叉引用移到正文中。

## 9. 表格内禁止出现引用

- 表格（`tabular`/`table` 环境）的任意单元格内，**禁止**出现 `\citep{}`/`\cite{}`/
  `\citet{}` 等引用命令，包括方法名列、行标签列（如 baseline/变体名称）。
  原因：引用命令在表格窄列中容易破坏对齐、在双栏/紧凑排版下导致换行错位或溢出，
  且审稿人/编辑习惯上不接受表格单元格内夹带引用。
- 若某一行（如某个 baseline、某种经典策略）确实需要标注出处，**必须把引用移到
  `\caption{}` 里**，用一句话说明该行对应的方法/策略来自哪篇文献，例如：
  `\caption{... STL follows the classical Seasonal-Trend decomposition
  procedure~\citep{cleveland1990stl}. ...}`。
- 检查方法：对每个新增或修改的 `results/table_*.tex` 文件，搜索 `\cite`/`\citep`/
  `\citet` 是否出现在 `\begin{tabular}...\end{tabular}` 范围内；若命中，一律挪到
  `\caption{}` 中改写为叙述性说明句。

## 10. 用脚本（matplotlib 等）生成图片的绘图规范

本节适用于所有用 Python 脚本（如 `matplotlib`）生成、导出到 `figs/*.pdf`/`*.png`
再用 `\includegraphics` 插入论文的图（不适用于纯 LaTeX/TikZ 绘制的图）。

### 10.1 分辨率与字体（强制，写图脚本时必须设置）

- **DPI 统一为 600**：脚本中不要各图各写一个 `dpi=` 数值，应在文件顶部定义一次
  全局常量（如 `FIG_DPI = 600`），所有 `fig.savefig(..., dpi=FIG_DPI)` 调用统一引用它。
- **全局字体统一为 Times New Roman**（不要局部对某个 `ax`/`text` 单独设置字体，
  应在脚本顶部、任何 `plt.subplots` 之前设置一次全局 `rcParams`）：

  ```python
  matplotlib.rcParams["font.family"] = "serif"
  matplotlib.rcParams["font.serif"] = ["Times New Roman"]
  matplotlib.rcParams["mathtext.fontset"] = "stix"  # 让公式符号也接近 Times 风格
  ```

  生成前可用以下命令确认系统已安装该字体，避免静默回退到默认字体：

  ```python
  import matplotlib.font_manager as fm
  assert any(f.name == "Times New Roman" for f in fm.fontManager.ttflist)
  ```

- 图片背景统一为白色：`facecolor="white"`（`fig`/`ax` 都要设置），
  `fig.savefig(..., facecolor="white", bbox_inches="tight")`。

### 10.2 坐标轴刻度必须均匀分布

- 当横轴变量本身数值跨度不均匀（如超参数扫描 `d=8,16,32,64,128` 或
  `M=4,8,16,32,64`，相邻间隔并非等差）时，**禁止**直接把原始数值作为 x 坐标传给
  `ax.plot(x, y)`（这会导致刻度疏密不均、后半段点挤在一起）。
- 正确做法：使用等间距的索引位置作为实际绘图坐标（如
  `x_idx = np.arange(len(values))`），再用 `ax.set_xticklabels([...])` 把刻度标签
  换成真实数值/类别名称，保证视觉上刻度间距均匀，同时刻度文字仍显示真实取值。
- 折线图/柱状图的类别型横轴（如消融变体名称、数据集名称）同样默认使用等间距
  索引位置，不需要额外处理。

### 10.3 尽量在同一张图中展示多个数据集

- 参数敏感性分析、误差随预测步长变化等分析类图表，若涉及的方法/机制对多个
  数据集都适用，应尽量在同一张图（或同一组 subplot）中叠加展示至少 2-3 个
  代表性数据集的曲线，而不是只画单一数据集，以增强结论的普适性论证力度。
- 若不同数据集的绝对数值量纲差异很大（如 flow 类数据集 MAE 在 10+，speed 类
  数据集 MAE 在 1~2 之间），**优先展示绝对真实值而不是转换为相对百分比**：
  为跨量纲的数据集组分配**双 y 轴**（`ax.twinx()`），量纲相近的数据集共用左轴，
  量纲差异大的数据集使用右轴，所有曲线仍共享同一组横轴刻度位置；右轴的轴标签
  颜色应与该数据集的曲线颜色保持一致，便于读者对应。只有当双 y 轴仍不足以清晰
  呈现（如数据集数量过多、量纲跨度极端）时，才退而使用相对各自最优配置的百分比
  （`100 * value / best_value`）作为替代方案，并在图注中明确说明该归一化方式。
- 多数据集需要用一致的配色 + marker 方案加以区分，并在图内或图上方放置共享
  图例（`fig.legend(...)`），不要在每个子图内重复画各自图例造成冗余。

### 10.4 避免遮挡与视觉杂乱

- 涉及地理底图（`contextily`）或密集节点/边的网络图时：优先使用不带文字标签的
  底图样式（如 `CartoDB.PositronNoLabels`），并调小节点 marker 尺寸、边的透明度，
  避免节点、边、底图文字互相遮挡。
- 不需要展示的自动生成水印/来源小字（如底图默认在角落打印的 attribution 文本）
  应显式关闭（如 `ctx.add_basemap(..., attribution="")`）。
- 多子图拼图时，所有子图必须保持一致的宽高比/坐标范围（如通过统一计算正方形
  bounding box），避免出现"某个子图明显比其他子图大/小"的观感问题。

### 10.5 面板标注与字号

- **面板字母必须是全图唯一、按顺序连续的扁平序列**：`(a) (b) (c) (d) (e) (f) ...`，
  **禁止**嵌套式编号（如 `(b1) (b2) (b3)`、`(a-1) (a-2)`）。即使某一行逻辑上是
  "对同一大面板的三个子情形分别展示"，也要把它们各自算作独立字母（例如三个节点
  各自的放大对比图应标为 `(b) (c) (d)`，而不是 `(b1) (b2) (b3)`），后续文字/图注
  引用时逐个点名 `(b)`/`(c)`/`(d)`，不要用 `(b1)--(b3)` 这种范围写法糊弄过去。
  字母顺序必须严格按面板在图中从左到右、从上到下的视觉顺序编号，不能跳号。
- 多子图图片的子图标签统一写在每个子图标题里（而不是图片外部单独排版），并保持
  全图子图标签样式统一（同一个字母风格、同一种加粗/字号）。
- 标题、坐标轴标签、图例、颜色条刻度的字号需要显式设置（不要用 matplotlib
  默认字号）。**默认字号必须明显大于普通文档正文**，因为多子图图会被压缩到论文
  单栏宽度显示，字号不够大会导致缩小后无法阅读；生成后务必按论文实际印刷宽度
  （单栏，约 8-9cm）预览一次，检查文字是否清晰。推荐起始范围（而非上限，如果
  面板数量少、单个面板更大，可以进一步调高）：
  - 子图标题：20-26pt
  - 坐标轴标签：16-18pt
  - 坐标轴刻度：15-16pt
  - 图例：12-17pt
  - 颜色条标签/刻度：与坐标轴标签/刻度同一档
  若某几个面板标题较长导致换行后与相邻面板重叠，优先精简标题文字（例如把
  "dependency strength to target node 183 (full network)" 精简为
  "PEMS-BAY: node 183 (full network)"），其次再考虑增大每个面板的宽度/间距
  （`figsize` 或 `wspace`），而不是反过来为了塞下长标题去调小字号。

### 10.6 图注（`\caption{}`）配套要求

- 图注中必须清楚说明每个面板 `(a)/(b)/...` 分别对应什么内容/数据集，
  以及图中数值是真实数据还是 Demo 模式下的模拟占位数据（遵循本文件第 4 章的
  Demo 声明要求）。
- 若某个面板使用了归一化/相对指标（如 10.3 中的相对 MAE），图注必须明确写出
  归一化定义。
- 图注内部仍需遵守第 7 章（禁止 `Section~\ref`）和第 8 章（禁止交叉引用其他
  图/表）的规则，只描述当前图/表自身，不回指编号。

## 11. 章节/小节标题（`\section`/`\subsection`/`\subsubsection`）命名规范

- 标题必须是**名词短语**（noun phrase），不能写成完整句子（不能出现主谓结构、
  不能是一个可以独立成句的陈述）。
  - 错误示例：`\subsection{Our Method Improves Accuracy on All Datasets}`、
    `\subsubsection{We Analyze How the Deviation Score Behaves}`（含主谓，是句子）。
  - 正确示例：`\subsection{Main Results}`、
    `\subsubsection{Adaptive Trend-Periodic Decomposition}`、
    `\subsubsection{Temporal View of the Response to a Real Multi-Day Disturbance}`
    （都是名词短语，没有主谓结构）。
- **避免用冒号拼接出"标签 + 解释性短句"的标题**（如
  `Case Study: Deviation-Aware Response to Traffic Disturbances`），这种写法读起来
  介于标题和图注之间，不够简洁。若确实需要限定性短语，优先用 `of`/`for`/`via` 等
  介词把两部分融合成一个连贯的名词短语（如改写为
  `Case Study on Deviation-Aware Response to Traffic Disturbances`），而不是用冒号
  断开成"标签: 描述"两截。
- 标题一律使用 Title Case（每个实词首字母大写，冠词/介词/连词等虚词小写，除非
  位于标题开头），与文件中已有标题的大小写风格保持一致。
- 标题末尾不加句号，不使用破折号做插入语（第 2 章的破折号限制同样适用于标题）。
- **禁止"孤子小节"（一个 `\subsection` 下只有唯一一个 `\subsubsection`）**：分级标题
  的意义在于把内容拆成两个或以上的并列部分；如果一个 `\subsection` 底下只挂了
  一个 `\subsubsection`，说明这次拆分没有意义，必须去掉这个多余的 `\subsubsection`
  标题，把其内容直接并入上一级 `\subsection` 的连续正文（用一句衔接性的过渡句
  引出，如 `To further examine ..., the ... row in Table~\ref{...} establishes
  that ...`），而不是保留一个形式上"只有一半"的子结构。同理，`\section` 下也不能
  只有一个孤立的 `\subsection`。写完一整个大节后，应通篇检查一遍每一级标题下是否
  存在这种"只有一个孩子"的情况。
- 检查方法：写完或修改任意 `\section{}`/`\subsection{}`/`\subsubsection{}` 后，
  自问"这行文字去掉大括号还能不能当一句完整的话读出来（有主语+谓语动词）"，
  如果能，就必须改写为名词短语；同时检查同一父标题下是否只有它一个子标题，
  如果是，直接删掉该子标题、并入上级正文。

## 12. 每个 `\section` 开头需要一段引导段落，禁止直接进入第一个 `\subsection`

- 除非该 `\section` 本身只有连续正文、完全没有下级 `\subsection`（如 Abstract、
  Conclusion），否则 `\section{...}` 命令之后、第一个 `\subsection{...}` 之前，
  必须先有一段简短的引导段落（2-4 句），说明这一节要讲什么、按什么顺序展开，
  不能让 `\section{Methodology}`/`\section{Related Work}` 后面直接跟第一个
  `\subsection`。
- 引导段落的内容因章节而异：
  - **Methodology**：点名提出的方法全称/缩写，一句话概括其核心机制，再用一句
    话给出本节的组织顺序（先形式化问题，再给整体框架，再逐模块展开），例如
    `This section presents the proposed Deviation-Aware Pivotal Graph Network
    (DAPGN), a unified architecture that couples adaptive trend-periodic
    decomposition with dynamic, deviation-modulated pivotal graph learning
    for traffic flow forecasting. We first formalize the forecasting
    problem, then give an overview of the overall pipeline, and finally
    detail each of its five components together with the training
    objective.`
  - **Related Work**：概括这一节要综述哪几条技术路线（通常一一对应各
    `\subsection` 的主题），并说明会指出其局限、将本文方法与之对比，例如
    `This section reviews three lines of work that underpin the design of
    DAPGN: graph-based traffic flow forecasting, decomposition- and
    prototype-based sequence forecasting, and pivotal-node or
    importance-aware graph modeling. For each, we summarize representative
    methods, highlight their limitations, and position DAPGN relative to
    them.`
  - **Experiments**：若该节已有 Demo Disclaimer 段落（占位数据声明）紧跟在
    `\section{Experiments}` 之后，该段落本身即视为满足本条要求，不需要再单独
    加一段引导段落。
- 引导段落篇幅要精炼（不超过 4 句），**不要重复 Introduction 里已经详细论证过
  的背景/动机/局限分析**（那些属于 Introduction 的职责，此处重复即冗余），
  这里只需要"点名方法/内容范围 + 给出本节路线图"，具体论证留给后面的正文小节；
  同时遵守本文件第 4 章"避免 Motivated by the lack of X 式绕弯子开场"的规则，
  不要在引导段落里重新铺垫一遍局限再引出方法。
- 检查方法：对每个 `.tex` 文件搜索 `\section{`，确认其后（跳过 `\label{}`）
  紧跟的是一段散文文字而不是直接的 `\subsection{`；若发现直接是
  `\subsection{`（且该 `\section` 确实包含多个 `\subsection`），需要按上面的
  模板补一段引导段落。新写一个 `\section` 时应从一开始就先写这段引导段落，
  不要写完所有 `\subsection` 后才回头补。

---

## 使用方式

- 各写作类 skill 完成初稿后，在"写作质量检查清单"环节追加一项：
  **"已按 `../WRITING_STANDARDS.md` 逐条自查图表引用顺序/分点/破折号/句内冒号/
  一致性/中式英语/`(e.g., ...)` 括号举例/`real` 强调真实性/非必要斜体
  （`\emph{}`）/`Motivated by the lack of` 绕弯子开场/LaTeX 符号/加粗规范/
  章节交叉引用限制/caption 内禁止交叉引用/表格内禁止引用/绘图规范
  （DPI·字体·刻度·多数据集·防遮挡）/章节标题必须是名词短语（第 11 章）/
  `\section` 开头需有引导段落（第 12 章）"**。
- 全文搜索 `\section{`/`\subsection{`/`\subsubsection{`，逐个检查花括号内文字是否
  含主谓结构（能否独立读成一句完整的话），命中则按第 11 章改写为名词短语；新写
  标题时应从一开始就按名词短语构造，不要先写成句子再回头改。同时按标题的出现顺序
  统计每一级标题下挂了几个下一级标题，若发现某个 `\subsection`/`\section` 下只有
  唯一一个子标题，按第 11 章把该子标题去掉、内容并入上级正文。
- 全文搜索 `Section~\ref`/`Sec\.~\ref`，除 Introduction 结尾的路线图段落外，
  命中的位置一律按第 7 章改写；同时检查所有 `\caption{}` 内部是否出现指向
  其他图/表的 `\ref`，命中则按第 8 章改写。
- 全文搜索 `e\.g\.`，命中的位置一律按第 4 章改写为 `such as`/`including` 等融入
  主句的写法（`i.e.,` 不受此限制）；写作过程中新增例子时应从一开始就按此规范
  措辞，不要写完再回头改。
- 全文搜索 `\breal\b`（忽略大小写，包含标题、caption、正文），命中的位置一律按
  第 4 章改写为删除该词或替换为 `public`/`observed`/`data-derived`/`actual`/
  `true` 等更精确的词，不要在标题或正文里用 `real` 去反复强调数据"是真的"；
  写新的图表标题或涉及公开数据集的描述时应从一开始就避免这个词，不要写完再回头改。
- 全文搜索 `[a-zA-Z]: `（正文段落，不含 `\label`/`\citep`/`\url`/`Section~\ref`
  等 LaTeX 命令内部的冒号），命中的位置逐条判断是否为引出公式/itemize 的结构性
  冒号（可保留）还是段内举例/列举/解释性从句的冒号（按第 2 章末尾的冒号规则改写
  为 `namely`/`in that`/`where`/独立成句等）；新写句子需要举例或解释时应从一开始
  就避免用冒号顶替，不要写完再回头改。
- 全文搜索 `\\emph\{`，命中的位置逐条判断是否属于第 4 章"非必要不要使用斜体"
  一条中列出的两类必要情形（术语首次正式定义、方法架构模块名称首次引出）；
  不属于的一律去掉 `\emph{}`，包括同一术语的后续重复提及、消融/对比实验变体
  名称、纯修辞强调词、以及整句话斜体。新写方法/实验描述时应默认不加斜体，只有
  确实是"这是一个第一次被正式定义、之后会反复引用的核心术语或模块名"时才考虑
  斜体一次，不要写完再回头改。
- 任何生成或修改 `scripts/generate_*.py`、`scripts/*figures*.py` 等绘图脚本的场景，
  必须先对照第 10 章「用脚本生成图片的绘图规范」检查 DPI、字体、坐标轴刻度、
  多数据集展示、防遮挡、面板标注这六项，而不是等用户逐条反馈后才补齐；面板字母
  一律用 10.5 节的扁平序列规则从一开始就编号，字号直接按 10.5 节给出的
  20-26/16-18/15-16/12-17pt 起始范围设置，不要先用小字号交差、等用户反馈"字太小"
  再返工放大。
- 全文搜索 `[Mm]otivated by the lack`，命中的位置按第 4 章改写为直接的
  `We propose ...`/`This paper proposes ...` 开场，不再绕弯子重述局限；新写
  方法提出句时应从一开始就直接陈述方法与机制，不要写完再回头改。
- 对每个含 `\section{` 且包含多个 `\subsection{` 的文件，检查 `\section{...}`
  之后是否紧跟一段引导段落而非直接进入第一个 `\subsection`；若缺失，按第 12
  章的模板（点名方法/内容范围 + 本节路线图）补一段，新写一个 `\section` 时
  应从一开始就先写这段引导段落。
- 用户提出"检查一致性/学术规范/润色语法"等类似请求时，优先读取本文件作为检查清单，
  逐段（而不是抽样）过一遍目标 `.tex` 文件。
