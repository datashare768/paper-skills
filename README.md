# paper-skills

个人科研 / 论文写作全流程 Skills 集合，按阶段拆分为独立的 Cursor Agent Skill，方便在不同项目中复用，并同步到 GitHub（`git@github.com:datashare768/paper-skills.git`）。

## 目录结构

每个阶段是一个独立目录，包含 `SKILL.md`（必需）以及可选的 `scripts/`、`reference.md`：

```
paper-skills/
├── README.md
├── WRITING_STANDARDS.md       # 所有写作 skill 共享的强制写作规范（图表引用顺序/禁止分点
│                               # 与破折号/一致性自检/中式英语与夸大断言/LaTeX符号/加粗规范）
├── idea-and-method-writing/   # 阶段：idea 构思 + 方法部分写作
│   ├── SKILL.md
│   └── scripts/
├── experiments-writing/       # 阶段：实验部分写作
│   ├── SKILL.md
│   └── scripts/
├── experiments-enrichment/    # 阶段：基于参考文献自动筛选并补充实验
│   ├── SKILL.md
│   └── scripts/
├── conclusion-writing/        # 阶段：结论部分写作
│   └── SKILL.md
├── related-work-writing/      # 阶段：相关工作写作 + BibTeX 生成
│   ├── SKILL.md
│   └── scripts/
├── introduction-writing/      # 阶段：引言写作（5-7段 + 4条贡献 + 论文结构段）
│   └── SKILL.md
├── abstract-writing/          # 阶段：摘要写作（单段 250-350词，5句式结构）
│   └── SKILL.md
└── ...                        # 后续阶段陆续添加
```

## 已有阶段

| 目录 | 说明 |
|------|------|
| `idea-and-method-writing/` | 根据参考文献 PDF 或研究方向，检索/解析顶会论文，组合创新生成 idea，并完成方法部分写作 |
| `experiments-writing/` | 调研参考论文的数据集/baseline/指标，确定实验方案，撰写 Experiments 部分（Academic/Demo 双模式） |
| `experiments-enrichment/` | 在已有 experiments.tex 基础上，扫描参考文献做过的实验类型/表格/图，按与本文核心创新点的相关度打分，自动（不问用户）选出 3-5 个新增项并补写 |
| `conclusion-writing/` | 生成独立的 conclusion.tex，两段式（主结论 + 简短局限展望），严格参考顶会写法，不冗余 |
| `related-work-writing/` | 从参考论文提取被引文献 → CrossRef 查 BibTeX → 整理 40-50 条 references.bib → 写 3-subsection 的 related_work.tex |
| `introduction-writing/` | 分析参考论文 Introduction 写法 → 按 7 段结构写 intro.tex（背景→挑战→综述→动机→方法→4条贡献→结构段） |
| `abstract-writing/` | 读 method.tex + experiments.tex → 单段摘要 abstract.tex（背景→不足→提出→技术→实验，250–350词） |

## 写作规范（重要）

所有写作类 skill（`abstract-writing`/`introduction-writing`/`related-work-writing`/
`idea-and-method-writing`/`experiments-writing`/`conclusion-writing`）在起草完成后，
都必须对照根目录的 `WRITING_STANDARDS.md` 逐条自查，涵盖：图表"先引用后出现"的顺序、
除 Introduction 贡献点外全文禁止分点/破折号、数值与术语与逻辑的前后一致性、
中式英语套语与无依据夸大断言、LaTeX 数学符号复用冲突、`\textbf{}` 加粗使用边界。
各 skill 的 SKILL.md 中已插入指向该文件的提示，但该文件本身是唯一权威来源，
更新写作规范时只需改 `WRITING_STANDARDS.md`，无需逐个 skill 重复维护细节。

## 使用方式

在 Cursor 中，将某个阶段目录整体复制到 `~/.cursor/skills/`（个人）或项目的 `.cursor/skills/`（项目级），即可被 Agent 识别和调用。

## 工作目录规范（重要）

**`paper-skills` 仓库本身只存放 skill 定义（`SKILL.md` + `scripts/`），不存放任何具体论文项目的产出文件。**

调用某个 skill 完成实际写作任务时，所有中间产物和最终文件（下载的参考论文、`text.md`、图片、
`method.tex`、`experiments.tex`、`intro.tex`、`abstract.tex`、`conclusion.tex`、
`related_work.tex`、`references.bib` 等）都应创建在**当前论文项目自己的目录下**，例如：

```
<你的论文项目>/                 # 例如 D:\PHD\Traffic_flow
├── reference_paper/            # 参考文献 PDF（已有）
├── papers/                     # skill 提取/下载的参考论文（text.md + figures/）
│   ├── <paper-slug-1>/
│   └── <paper-slug-2>/
└── paper/                      # 本文写作产出（各章节独立 tex 文件）
    ├── main.tex                # 主文档，用 \input{} 引入各章节
    ├── abstract.tex
    ├── intro.tex
    ├── related_work.tex
    ├── references.bib
    ├── method.tex
    ├── experiments.tex
    └── conclusion.tex
```

SKILL.md 中出现的 `workspace/`、`papers/` 等相对路径，均指**当前论文项目目录下**新建的文件夹，
不要在 `paper-skills` 仓库内创建这些文件夹（`paper-skills/.gitignore` 里的 `workspace/`、
`workspace_*/` 规则只是兜底防误提交，正确用法是压根不在这个仓库里生成）。

## 项目上下文记录（跨对话迁移用）

每个使用这些 skill 的论文项目目录下，建议维护一个 `PROJECT_STATUS.md`（放在项目根目录，例如
`<你的论文项目>/PROJECT_STATUS.md`，不要放进 `paper-skills` 仓库），记录：项目主题/模型名、
各 section 完成状态、已确定的关键规范/坑（如模板限制、表格合并方式、Demo Mode 约定）、遗留
待办。新开对话时先读这个文件即可快速接续上下文，避免每次重新解释背景或重复踩坑。写作时保持
简洁（一页以内），只记结论和规范，不重复贴大段正文。

## 同步到 GitHub

```bash
git add .
git commit -m "更新 xxx 阶段 skill"
git push -u origin main
```
