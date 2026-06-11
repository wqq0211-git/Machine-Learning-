# Machine Learning

本仓库使用 [OpenSpec](https://github.com/Fission-AI/OpenSpec) 做**规格驱动开发（Spec-Driven Development）**：先把「做什么、为什么、怎么做、分几步做」写清楚，再让 AI 按任务清单实现代码。

---

## 前置条件

1. 安装 OpenSpec CLI（当前项目使用 **1.4.0**）：

   ```bash
   npm install -g @fission-ai/openspec
   openspec --version
   ```

2. 在 AI 编辑器中使用本仓库已配置好的命令（Cursor / Claude Code / Codex 均可）：
   - 命令定义：`.cursor/commands/`、`.claude/commands/opsx/` 等
   - Skill 定义：`.cursor/skills/openspec-*/SKILL.md` 等

---

## 目录结构

```text
openspec/
├── config.yaml          # 工作流 schema、项目上下文、artifact 规则
├── specs/               # 主规格（长期维护的系统能力说明）
│   └── <capability>/
│       └── spec.md
└── changes/             # 进行中的变更
    ├── <change-name>/   # 单个 change 的 proposal / design / tasks / delta specs
    └── archive/         # 已归档的 change（YYYY-MM-DD-<name>）
```

当前项目默认 schema 为 **`spec-driven`**（见 `openspec/config.yaml`），artifact 生成顺序：

```text
proposal → specs → design → tasks → apply（实现）
```

---

## 五个核心命令

在 Cursor 聊天框输入以下斜杠命令即可触发对应工作流（Claude Code 中为 `/opsx:propose` 等形式，含义相同）。

| 命令 | 用途 | 典型场景 |
|------|------|----------|
| `/opsx-explore` | 探索模式：讨论想法、查代码、对比方案 | 需求还不清晰，先想清楚再动手 |
| `/opsx-propose` | 一键创建 change 并生成全部 artifact | 需求已明确，要正式立项 |
| `/opsx-apply` | 按 `tasks.md` 逐项实现代码 | artifact 就绪，开始写代码 |
| `/opsx-sync` | 把 change 里的 delta spec 合并到主 spec | 实现过程中规格有更新 |
| `/opsx-archive` | 归档已完成的 change | 任务全部做完，收尾 |

---

## 推荐使用流程

```text
┌─────────────┐     想法模糊      ┌─────────────┐
│   explore   │ ───────────────▶  │   propose   │
│  探索讨论    │                   │  创建变更    │
└─────────────┘                   └──────┬──────┘
       ▲                                 │
       │ 实现中遇到设计问题                  │ 生成 proposal / specs /
       │                                 │ design / tasks
       │                                 ▼
       │                          ┌─────────────┐
       └────────────────────────  │    apply    │
                                  │  按任务实现   │
                                  └──────┬──────┘
                                         │
                    规格变更              │ 全部完成
                    ┌─────────────┐       │
                    │    sync     │◀──────┤
                    │ 同步主规格   │       │
                    └─────────────┘       ▼
                                   ┌─────────────┐
                                   │   archive   │
                                   │  归档变更    │
                                   └─────────────┘
```

### 1. 探索（`/opsx-explore`）

- **只思考，不写业务代码**（可以读代码、画图、对比方案）
- 适合：需求模糊、架构选型、实现卡住时重新梳理
- 示例：

  ```text
  /opsx-explore 我想给训练 pipeline 加 checkpoint 恢复
  /opsx-explore add-data-loader   # 围绕某个 change 继续讨论
  ```

- 讨论出结论后，可以说「帮我创建 proposal」进入下一步

### 2. 提案（`/opsx-propose`）

- 创建一个 change（kebab-case 命名，如 `add-checkpoint-resume`）
- 自动生成 artifact：
  - `proposal.md` — 做什么、为什么做
  - `specs/` — 本次变更涉及的能力规格（delta spec）
  - `design.md` — 技术方案
  - `tasks.md` — 可勾选的实现任务清单
- 示例：

  ```text
  /opsx-propose add-checkpoint-resume
  /opsx-propose 给 PyTorch 训练脚本增加断点续训
  ```

- 完成后提示：运行 `/opsx-apply` 开始实现

### 3. 实现（`/opsx-apply`）

- 读取 proposal / specs / design / tasks 作为上下文
- 逐条完成 `tasks.md` 中的 `- [ ]` 任务，完成后改为 `- [x]`
- 示例：

  ```text
  /opsx-apply
  /opsx-apply add-checkpoint-resume
  ```

- 若任务不清晰或设计与实现冲突，AI 会暂停并建议更新 artifact
- 全部任务完成后，建议执行 `/opsx-archive`

### 4. 同步规格（`/opsx-sync`）

- 把 change 目录下的 **delta spec** 智能合并到 `openspec/specs/<capability>/spec.md`
- delta spec 常见段落：
  - `## ADDED Requirements`
  - `## MODIFIED Requirements`
  - `## REMOVED Requirements`
  - `## RENAMED Requirements`
- 适合：实现过程中发现规格变化，但还不想立刻归档
- 示例：

  ```text
  /opsx-sync add-checkpoint-resume
  ```

### 5. 归档（`/opsx-archive`）

- 检查 artifact 与 tasks 是否完成（未完成会警告并让你确认）
- 如有 delta spec，会询问是否先 sync 再归档
- 将 change 移动到 `openspec/changes/archive/YYYY-MM-DD-<name>/`
- 示例：

  ```text
  /opsx-archive add-checkpoint-resume
  ```

---

## 常用 CLI 命令

除斜杠命令外，也可以直接在终端使用 OpenSpec CLI：

```bash
# 查看进行中的 change
openspec list

# 查看主规格
openspec list --specs

# 查看某个 change 的 artifact 完成状态
openspec status --change "add-checkpoint-resume"

# 交互式浏览 specs 和 changes
openspec view

# 手动创建 change（通常交给 /opsx-propose 即可）
openspec new change "add-checkpoint-resume"

# 校验 change 或 spec
openspec validate add-checkpoint-resume
```

---

## 配置说明

编辑 `openspec/config.yaml` 可定制 AI 生成 artifact 时的约束：

```yaml
schema: spec-driven

# 可选：项目背景，会注入到 AI 的 artifact 生成上下文
context: |
  Tech stack: Python, PyTorch
  数据集放在 data/ 目录，不提交 git
  训练脚本统一放在 src/training/

# 可选：针对不同 artifact 的额外规则
rules:
  proposal:
    - 必须包含 Non-goals 章节
  tasks:
    - 每个任务控制在 2 小时以内
```

---

## 使用建议

1. **先 explore，再 propose** — 避免一上来就写大量文档却方向不对
2. **tasks 要可验收** — 每条任务对应明确的代码改动或验证方式
3. **实现中随时回改 artifact** — OpenSpec 不强制「先文档后代码」，发现设计问题就更新 `design.md` 或 `tasks.md`
4. **归档前 sync** — 确保 `openspec/specs/` 反映最新系统能力，方便后续 change 引用
5. **change 命名用 kebab-case** — 如 `add-lr-scheduler`，不要用空格或驼峰

---

## 快速上手示例

假设你要给项目加一个学习率调度器：

```text
# 1. 先讨论方案
/opsx-explore 训练脚本需要 cosine annealing 学习率调度

# 2. 方案确定后创建 change
/opsx-propose add-lr-scheduler

# 3. 按 tasks 实现
/opsx-apply add-lr-scheduler

# 4. 完成后归档（必要时先 sync）
/opsx-archive add-lr-scheduler
```

---

## 相关文件

| 路径 | 说明 |
|------|------|
| `openspec/config.yaml` | OpenSpec 项目配置 |
| `.cursor/commands/opsx-*.md` | Cursor 斜杠命令 |
| `.cursor/skills/openspec-*/SKILL.md` | Cursor Agent Skill 详细流程 |
| `.claude/commands/opsx/` | Claude Code 命令 |
| `.codex/skills/openspec-*/` | Codex Skill |

如需更新命令与 Skill 到最新版，可在项目根目录执行：

```bash
openspec update
```
