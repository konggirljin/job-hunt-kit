# job-hunt-kit

**[English](README.md) · [繁體中文](README.zh-Hant.md) · [简体中文](README.zh-Hans.md)**

> 在真实的求职实战中打造的一套**一体化的 AI 求职机器人**。它帮你找工作、给你的胜算评分、把你的简历写成与改造成**真正的一页 Word 文档**、跑 ATS 关键词检查、跟踪每一份申请—，通过 Chrome 控制，把繁琐步骤**一路做到尾**，只在最后「提交」那一刻停下来等你。

---

## 为什么是这套

大多数「AI 简历工具」只吐出一大段文字，你得自己手动排回简历格式。这套不一样：它直接操作**招聘者会打开的那份 Word 文档**。

- **一页 `.docx`，经过验证。** 不是「大约一页」。它编辑真正的 Word 文件，再用 Word 自己的页数／行数统计去量，让你**确定**它是一页。没有字体出错、没有漂移。
- **自动找工作。** 指向你的目标市场，它每周（或自定义）扫各大平台、去重、给你一份入围名单。
- **自动算匹配。** 每份 JD 都有匹配分数、缺口分析与预警检查—，让你把力气只花在值得的职位上。
- **自动写简历 + 改造。** 按每个职位的配置，生成定制的 `.docx`、重排你最有料的经历、并做 ATS 关键词优化，同时保持内容诚实（不编造数字）。
- **省时的 Chrome 控制。** 配合可操作浏览器的 agent（例如Codex），它能开职位页、读 JD、甚至自己填申请表，只在最后审核时交回给你。你的时间花在「判断」，不是「复制粘贴」。
- **一条龙流程，一地完成。** 搜索 → 分析 → 改造 → 验证 → 跟踪。一切都以文件存在，任何全新的 agent 会话都能中途接手。

## 含有什么

| 项目 | 功能 |
|---|---|
| `skills/job-description-analyzer` | 对每份 JD 算匹配分数、缺口分析、预警、投／不投策略 |
| `skills/resume-tailor` | 完整流程：配置驱动的 docx 生成 → 一页校对 → ATS 关键词检查 → 变更记录 |
| `skills/job-search` | 按契约的每周扫描；**先呈报再写入**（agent 给入围名单，由你决定存什么） |
| `skills/one-page-cv` | 把爆页的简历压到刚好一页，并用 Word 验证 |
| `profile/` | 你的个人文件（gitignore，不会被推送到github上）：简历、背景、诚实校准、搜索契约 |
| `scripts/tailor.py` | 配置驱动的简历生成器——产出真正的 `.docx`，保留格式 |
| `scripts/verify_one_page.py/.ps1` | Word 文档的页／行验证 |
| `scripts/extract_master.py` | docx → markdown 能力清单同步 |
| `scripts/register-weekly-search.ps1` | Windows 计划任务：每周自动求职扫描 |
| `docs/browser-and-scheduling-tips.md` | 指导AI Chrome 控制求职网页技巧 |
| `AGENTS.md` | 你的 agent 读的工作区规范 |

## 工作流程

```
job-search ──▶ jobs/<id>.md（逐字 JD）
     │                 │
     │                 ▼
     │        job-description-analyzer（匹配分数、缺口）
     │                 │
     ▼                 ▼
每周扫描      resume-tailor ──▶ tailored/<姓名>_<公司> <职位>.docx
（入围名单）         │                    │
     │              │            verify_one_page（页数=1）
     │              │                    │
     ▼              ▼                    ▼
  你来选    变更记录 + ATS 报告 ─▶ tracker.md
```

## 完全没碰过 git／GitHub／agent？让 AI 帮你装

你不必懂任何东西。把下面这段提示词复制贴到你的 AI 助手（Claude、Codex、
opencode、ChatGPT…），它会从零一步步带你走完——你唯一要亲手做的，就是
把你的简历放进一个文件夹、然后回答问题。你的 AI 会照这套 kit 自己的指南
走：`docs/getting-started.md`。

<details>
<summary>点击展开可复制的提示词</summary>

```text
你要从零帮我架设「job-hunt-kit」。我对 GitHub、git、命令行、Python、AI agent
完全没经验——所以请尽量帮我做，或每个步骤都用平易近人、非技术性的话说明。

项目在此：<贴上 git clone 网址或 GitHub repo 链接>

我想请你：
1. 先读该 repo 里的 docs/getting-started.md——它教你如何引导像我这样的
   完全新手。
2. 告诉我要准备哪些文件。我知道至少要准备 .docx 档的简历；请说明如果我只有
   PDF 该怎么转成 .docx。
3. 一步步带我把这套 kit 装到我的电脑上。
4. 帮我填好「profile」文件夹（我的简历、我的诚实笔记、其他不在简历上的背景、
   我的求职偏好）。
5. 设定好我的 AI agent，让它能用 kit 的技能。
6. 接着跑内建的测试让我看它运作正常，并示范一个真实任务（例如「改造我的简历」
   或「找工作」），让我以后知道怎么用。

重要：把我当成什么都不懂——每个名词都要解释，能帮我做的技术步骤就帮我做，
非必要别叫我打字。先从「告诉我要准备什么」开始。
```

</details>

## 快速开始（5 分钟）

```powershell
git clone <你的 repo 地址>/job-hunt-kit.git my-job-hunt
cd my-job-hunt
```

1. **填 `profile/`**——按 `profile/README.md`：
   把简历丢进 `profile/cv/`，把每个 `*.template.md` 复制成正式文件名并填好
   （context、truthfulness、search contract），`tailor.json.example` →
   `tailor.json` 并指向你的简历。
2. **把工作区模板复制到根目录：**

   ```powershell
   New-Item -ItemType Directory -Force jobs, tailored, tailoring-configs | Out-Null
   Copy-Item template\jobs\_template.md jobs\
   Copy-Item template\tracker.template.md tracker.md
   Copy-Item template\tailoring-configs\job-example.json tailoring-configs\
   ```

3. **为你的 agent 安装技能**（见下）。
4. 同步能力清单：`python scripts/extract_master.py`
5. 跟你的 agent 说：*「存下这份工作」*、*「拿我跟职位 X 比」*、
   *「为职位 X 改造我的简历」*——完整指令集见 `AGENTS.md`。

### 各平台安装技能

把 `skills/` 里每个文件夹复制（或符号链接）到你的 agent 技能目录：

| Agent | 路径 |
|---|---|
| opencode | `<工作区>\.agents\skills\`（或全局配置目录） |
| Claude Code | `~/.claude/skills/`（或工作区内的 `.claude/skills/`） |
| Codex | `<工作区>\.codex\skills\` |

Windows 符号链接需要管理员／开发者模式——直接用复制即可。

### 需求

- Python 3.10+，`pip install python-docx`（改造 + 提取）
- Windows + Microsoft Word 做一页验证
  （`.py` 验证器需 `pip install pywin32`；`.ps1` 版零依赖）
- agent CLI：opencode（已验证）、Claude Code 或 Codex

## 每周自动扫描（可选，限 Windows）

```powershell
powershell -ExecutionPolicy Bypass -File scripts\register-weekly-search.ps1
```

每周以无头模式跑一次你的 agent、对照你的搜索契约，并记录**入围名单**——
在你挑选之前什么都不会存。细节、Chrome 控制技巧（Codex）与计划任务管理：
`docs/browser-and-scheduling-tips.md`。

## Chrome 控制：让 AI 做到只剩最后一击

配合操作浏览器的 agent（Codex 的原生 Chrome 控制），整条流程可全自动：

1. AI 开平台、读 JD、去重、产出入围名单。
2. AI 起草每份申请与定制简历。
3. AI 填表（姓名已在文件中、地址、工作经历、上传件）、贴上针对该 JD 的答复。
4. **唯一的人工检查点：** 你浏览一次填好的表单，然后按下提交。
   （或告诉 agent，只有在你批准后才提交。）

决定权在你，打字交给 AI。完整做法见
`docs/browser-and-scheduling-tips.md`。

## 设计原则

1. **文件即真相。** 每份工作、申请、编辑都以 markdown/json 存在——全新的
   agent 会话也能中途接手。
2. **agent 提议、你拍板。** 全面「先呈报再写入」：存档前先给名单、提交前先给
   变更记录、数字没把握就 `[to fill]`。
3. **诚实** 一页简历是浓缩精华，以你的工作经验实际判断是否有缺口，基础技能如Window Office技巧默认你会，避免AI过分诚实缺乏常识。如遇到不确认，AI会停下问你（`profile/truthfulness.md`）。
4. **一页CV，经过验证。** 每次都用量 Word 文档层级的页／行统计——逐段统计会跳过
   表格行，会骗人。
5. **工作区绝不把你的秘密放进 git。** 所有个资自第一笔 commit 起就 gitignore。

## 隐私承诺

**本 repo 不带任何个人数据。** 你的简历、背景、搜索契约、JD 与跟踪表都放在被
gitignore 的路径（`profile/`、`jobs/`、`tailored/`、`tracker.md`）。若你 fork
这套，请保持如此——绝不把真实简历数据 commit 进来。

## 鸣谢

- [`resume-tailor`、`resume-ats-optimizer`、`job-description-analyzer`
  血统：Paramchoudhary/ResumeSkills](https://github.com/Paramchoudhary/ResumeSkills)
  （MIT）——大幅改写并合并了原创流程（搜索契约、先呈报再写入、一页 playbook、
  定制化产出工具）。

## 许可

MIT——见 [LICENSE](LICENSE)。
