# paper-skills

个人科研 / 论文写作全流程 Skills 集合，按阶段拆分为独立的 Cursor Agent Skill，方便在不同项目中复用，并同步到 GitHub（`git@github.com:datashare768/paper-skills.git`）。

## 目录结构

每个阶段是一个独立目录，包含 `SKILL.md`（必需）以及可选的 `scripts/`、`reference.md`：

```
paper-skills/
├── README.md
├── idea-and-method-writing/   # 阶段：idea 构思 + 方法部分写作
│   ├── SKILL.md
│   └── scripts/
├── experiments-writing/       # 阶段：实验部分写作
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
| `conclusion-writing/` | 生成独立的 conclusion.tex，两段式（主结论 + 简短局限展望），严格参考顶会写法，不冗余 |
| `related-work-writing/` | 从参考论文提取被引文献 → CrossRef 查 BibTeX → 整理 40-50 条 references.bib → 写 3-subsection 的 related_work.tex |
| `introduction-writing/` | 分析参考论文 Introduction 写法 → 按 7 段结构写 intro.tex（背景→挑战→综述→动机→方法→4条贡献→结构段） |
| `abstract-writing/` | 读 method.tex + experiments.tex → 单段摘要 abstract.tex（背景→不足→提出→技术→实验，250–350词） |

## 使用方式

在 Cursor 中，将某个阶段目录整体复制到 `~/.cursor/skills/`（个人）或项目的 `.cursor/skills/`（项目级），即可被 Agent 识别和调用。

## 同步到 GitHub

```bash
git add .
git commit -m "更新 xxx 阶段 skill"
git push -u origin main
```
