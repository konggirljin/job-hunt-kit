# job-hunt-kit

**[English](README.md) · [繁體中文](README.zh-Hant.md) · [简体中文](README.zh-Hans.md)**

> 一套**整合式的 AI 求職機器**。它幫你找工作、評分你的勝算、把你的履歷寫成與改造成**真正的單頁 Word 文件**、跑 ATS 關鍵字檢查、追蹤每一份申請——甚至透過 Chrome 控制，把繁瑣步驟**一路做到底**，只在最後「送出」那一刻停下來等你。

在真正的求職實戰中打造。這裡的每一條教訓，都是用一次頁數算錯或一次誤判「技能缺口」換來的。

---

## 為什麼是這套

大多數「AI 履歷工具」只吐出一大段文字，你得自己手動排回履歷格式。這套不同：它直接操作**招募者會打開的那份 Word 文件**。

- **單頁 `.docx`，經過驗證。** 不是「大約一頁」。它編輯真正的 Word 檔，再用 Word 自己的頁數／行數統計去量，讓你**確定**它是一頁。沒有字型出錯、沒有漂移。
- **自動找工作。** 指向你的目標市場，它每週（或隨需）掃各大平台、去重、給你一份入圍名單。
- **自動算匹配。** 每份 JD 都有匹配分數、缺口分析與警示檢查——讓你把力氣只花在值得的職缺上。
- **自動寫履歷 + 改造。** 依每個職缺的設定檔，生成客製的 `.docx`、重排你最有料的經歷、並做 ATS 關鍵字優化——同時保持內容誠實（不編造數字）。
- **省時的 Chrome 控制。** 配合可操作瀏覽器的 agent（Codex），它能開職缺頁、讀 JD、甚至自己填申請表——只在最後審核時交回給你。你的時間花在「判斷」，不是「複製貼上」。
- **一條龍流程，一地完成。** 搜尋 → 分析 → 改造 → 驗證 → 追蹤。一切都以檔案存在，任何全新的 agent 會話都能中途接手。

## 內含什麼

| 項目 | 功能 |
|---|---|
| `skills/job-description-analyzer` | 對每份 JD 算匹配分數、缺口分析、警示、投／不投策略 |
| `skills/resume-tailor` | 完整流程：設定檔驅動的 docx 產生 → 單頁校對 → ATS 關鍵字檢查 → 變更記錄 |
| `skills/job-search` | 依契約的每週掃描；**先呈報再寫入**（agent 給入圍名單，由你決定存什麼） |
| `skills/one-page-cv` | 把爆頁的履歷壓到剛好一頁，並用 Word 驗證 |
| `profile/` | 你的私人層（gitignore）：履歷、背景、誠實校準、搜尋契約 |
| `scripts/tailor.py` | 設定檔驅動的履歷產生器——產出真正的 `.docx`，保留格式 |
| `scripts/verify_one_page.py/.ps1` | Word 文件的頁／行驗證（唯一不會騙人的統計） |
| `scripts/extract_master.py` | docx → markdown 能力清單同步 |
| `scripts/register-weekly-search.ps1` | Windows 排程器：每週自動求職掃描 |
| `docs/browser-and-scheduling-tips.md` | Chrome 控制技巧 + 如何讓 AI 做到只剩最後一擊 |
| `AGENTS.md` | 你的 agent 讀的工作區規範 |

## 工作流程

```
job-search ──▶ jobs/<id>.md（逐字 JD）
     │                 │
     │                 ▼
     │        job-description-analyzer（匹配分數、缺口）
     │                 │
     ▼                 ▼
每週掃描      resume-tailor ──▶ tailored/<姓名>_<公司> <職位>.docx
（入圍名單）         │                    │
     │              │            verify_one_page（頁數=1）
     │              │                    │
     ▼              ▼                    ▼
  你來選    變更記錄 + ATS 報告 ─▶ tracker.md
```

## 快速開始（5 分鐘）

```powershell
git clone <你的 repo 網址>/job-hunt-kit.git my-job-hunt
cd my-job-hunt
```

1. **填 `profile/`**——照 `profile/README.md`：
   把履歷丟進 `profile/cv/`，把每個 `*.template.md` 複製成正式檔名並填好
   （context、truthfulness、search contract），`tailor.json.example` →
   `tailor.json` 並指向你的履歷。
2. **把工作區範本複製到根目錄：**

   ```powershell
   New-Item -ItemType Directory -Force jobs, tailored, tailoring-configs | Out-Null
   Copy-Item template\jobs\_template.md jobs\
   Copy-Item template\tracker.template.md tracker.md
   Copy-Item template\tailoring-configs\job-example.json tailoring-configs\
   ```

3. **為你的 agent 安裝技能**（見下）。
4. 同步能力清單：`python scripts/extract_master.py`
5. 跟你的 agent 說：*「存下這份工作」*、*「拿我跟職缺 X 比」*、
   *「為職缺 X 改造我的履歷」*——完整指令集見 `AGENTS.md`。

### 各平台安裝技能

把 `skills/` 裡每個資料夾複製（或符號連結）到你的 agent 技能目錄：

| Agent | 路徑 |
|---|---|
| opencode | `<工作區>\.agents\skills\`（或全域設定目錄） |
| Claude Code | `~/.claude/skills/`（或工作區內的 `.claude/skills/`） |
| Codex | `<工作區>\.codex\skills\` |

Windows 符號連結需要管理員／開發者模式——直接用複製即可。

### 需求

- Python 3.10+，`pip install python-docx`（改造 + 萃取）
- Windows + Microsoft Word 做單頁驗證
  （`.py` 驗證器需 `pip install pywin32`；`.ps1` 版零依賴）
- agent CLI：opencode（已驗證）、Claude Code 或 Codex

## 每週自動掃描（選用，限 Windows）

```powershell
powershell -ExecutionPolicy Bypass -File scripts\register-weekly-search.ps1
```

每週以無頭模式跑一次你的 agent、對照你的搜尋契約，並記錄**入圍名單**——
在你挑選之前什麼都不會存。細節、Chrome 控制技巧（Codex）與排程管理：
`docs/browser-and-scheduling-tips.md`。

## Chrome 控制：讓 AI 做到只剩最後一擊

配合操作瀏覽器的 agent（Codex 的原生 Chrome 控制），整條流程可全自動：

1. AI 開平台、讀 JD、去重、產出入圍名單。
2. AI 起草每份申請與客製履歷。
3. AI 填表（姓名已在檔案中、地址、工作經歷、上傳檔）、貼上針對該 JD 的答覆。
4. **唯一的人工檢查點：** 你檢視一次填好的表單，然後按下送出。
   （或告訴 agent，只有在你核准後才送出。）

決定權在你，打字交給 AI。完整做法見
`docs/browser-and-scheduling-tips.md`。

## 設計原則

1. **檔案即真相。** 每份工作、申請、編輯都以 markdown/json 存在——全新的
   agent 會話也能中途接手。
2. **agent 提議、你拍板。** 全面「先呈報再寫入」：存檔前先給名單、提交前先給
   變更記錄、數字沒把握就 `[to fill]`。
3. **誠實是校準過的，不是絕對的。** 單頁履歷是濃縮；詳盡清單
   （`profile/cv-master.md`）才是真正的能力列表。缺口以實際經驗判斷，沒把握
   的主張變成一個問題，而不是沉默的假設（`profile/truthfulness.md`）。
4. **單頁，經過驗證。** 每次都用量 Word 文件層級的頁／行統計——逐段統計會跳過
   表格行，會騙人。
5. **工作區絕不把你的秘密放進 git。** 所有個資自第一筆 commit 起就 gitignore。

## 隱私承諾

**本 repo 不帶任何個人資料。** 你的履歷、背景、搜尋契約、JD 與追蹤表都放在被
gitignore 的路徑（`profile/`、`jobs/`、`tailored/`、`tracker.md`）。若你 fork
這套，請保持如此——絕不把真實履歷資料 commit 進來。

## 鳴謝

- [`resume-tailor`、`resume-ats-optimizer`、`job-description-analyzer`
  血統：Paramchoudhary/ResumeSkills](https://github.com/Paramchoudhary/ResumeSkills)
  （MIT）——大幅改寫並合併了原創流程（搜尋契約、先呈報再寫入、單頁 playbook、
  客製化產出工具）。
- 靈感來自技能生態：`anthropics/skills`、`obra/superpowers`。

## 授權

MIT——見 [LICENSE](LICENSE)。
