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
└── ...                        # 后续阶段陆续添加
```

## 已有阶段

| 目录 | 说明 |
|------|------|
| `idea-and-method-writing/` | 根据参考文献 PDF 或研究方向，检索/解析顶会论文，组合创新生成 idea，并完成方法部分写作 |

## 使用方式

在 Cursor 中，将某个阶段目录整体复制到 `~/.cursor/skills/`（个人）或项目的 `.cursor/skills/`（项目级），即可被 Agent 识别和调用。

## 同步到 GitHub

```bash
git add .
git commit -m "更新 xxx 阶段 skill"
git push -u origin main
```
