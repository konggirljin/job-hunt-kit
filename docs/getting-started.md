# First-time setup guide (for the AI — how to guide a brand-new user)

You (the AI agent) are walking a user through their very first `job-hunt-kit`
setup. Assume the user has **zero** Git/GitHub/agent experience — no
`git clone`, no commands, nothing. You do the heavy lifting; the user only
prepares files and answers questions.

Read this BEFORE guiding anyone, then follow the steps in order. Every step
below that the *user* must do is phrased in plain, non-technical language you
can relay directly (or do for them where possible).

---

## 0. What the human needs to prepare first

Ask the user to gather these **before** you start. Only #1 is required; the
rest strongly improve results.

### 1. A Master CV — **REQUIRED**

A Word document (`.docx`) of their full CV. This is the single source of
truth the whole kit is built on.

- If they only have a PDF, ask them to export/re-save it as `.docx` (Word:
  File → Save As → Word Document). A `.docx` is required because the kit
  *edits* the file programmatically to produce one-page tailored CVs.
- If they have multiple variants (e.g. a detailed "everything" version vs a
  one-page version), take **both** — label the big one as the "everything
  master" and the one-pager as the "tailoring base".

### 2. Truthfulness calibration — *optional (recommended)*

A short list that tells the AI what the user honestly knows, so it doesn't
over- or under-claim. Explain it plainly:

> "List any basic tools you use daily and are comfortable claiming (e.g. MS
> Office, Google Workspace, basic dashboards/Excel) — the AI will assume you
> know these. Also list any specialized systems you do NOT know and don't
> want claimed (e.g. SAP, Salesforce)."

This becomes `profile/truthfulness.md`. If they skip it, tell them the kit
ships a template they can fill later.

### 3. Extra context not on the CV — *optional (recommended)*

Anything the CV doesn't say but the AI should know when writing/tailoring:

- Right-to-work / visa status, notice period, earliest start date
- Salary floor or target; location / WFH constraints
- Career direction (the 1–3 role types they actually want)
- Dealbreakers (industries/employers they refuse)
- Anything they never want claimed

This becomes `profile/context.md`.

### 4. Their search contract — *optional (defaults otherwise)*

Where and what to search: location (office-required?), seniority level,
how recent postings must be, target companies/keywords. If they skip it,
start with sensible defaults and confirm with them once.

---

## 1. Prerequisites the AI should check

Before guiding the clone, check the user's machine (do it *for* them where
possible):

- [ ] **Git** installed — run `git --version`. If missing, help install it
      (e.g. `winget install Git.Git` on Windows, or point them to git-scm.com).
- [ ] **Python 3.10+** — `python --version`. If missing, help install.
- [ ] `python-docx` — `pip install python-docx`.
- [ ] An **agent CLI** they'll use daily: opencode / Claude Code / Codex.
      Ask which one they use (or plan to), then install the skills there.
- [ ] **Windows + Microsoft Word** — required for one-page verification only.
      (macOS/Linux: the `.docx` build still works; one-page *verification*
      needs Word or manual eyeballing.)

## 2. Get the kit onto their machine

If the user is going to *you* through a workspace already containing this
repo, skip to §3. Otherwise walk them through **creating their own copy**:

**Option A — they have GitHub (recommended for portfolio users):**
1. On github.com, they click **Fork** on the kit repo (or "Use this
   template" → "Create repository", then clone THEIR fork). Explain: this
   gives them their own private copy they control.
2. Clone it locally, doing the command *for them* (or relaying):
   `git clone <their-fork-url> my-job-hunt`

**Option B — no GitHub, just want it locally:**
1. Download the repo as a ZIP (github.com green **Code** button → Download
   ZIP), unzip to a folder named e.g. `my-job-hunt`. That's it — no git needed
   for a purely local workout. (Note: they lose easy upgrade/tracking; mention
   this lightly, don't over-explain.)

## 3. Fill the profile (the only part with THEIR data)

The `profile/` folder is gitignored — its contents never leave their machine.
Guide them (or do it for them) to:

1. Put the Master CV `.docx` into `profile/cv/`.
2. Copy each `*.template.md` → its real name and fill it:
   - `context.template.md` → `context.md` (their extra context, §0.3)
   - `truthfulness.template.md` → `truthfulness.md` (their calibration, §0.2)
   - `search-contract.template.md` → `search-contract.md` (their contract, §0.4)
3. Copy `tailor.json.example` → `tailor.json` and edit:
   - `name` → their display name (used in generated CV filenames)
   - `source_cv` → path to their one-page base CV
   - `line_budget` → how many lines fit *their* one page (measure it, below)
   - `anchors` → literal text strings that exist in their CV (contact line,
     a section header, a body sentence). **This is the most common source of
     "paragraph not found" errors** — help them copy exact strings from their
     own docx.

## 4. Scaffold the workspace + install skills

Do these *for* them (relay the commands):

```powershell
# copy starter files into the workspace root
New-Item -ItemType Directory -Force jobs, tailored, tailoring-configs | Out-Null
Copy-Item template\jobs\_template.md jobs\
Copy-Item template\tracker.template.md tracker.md
Copy-Item template\tailoring-configs\job-example.json tailoring-configs\

# sync the capability-inventory mirror from their master CV
python scripts/extract_master.py
```

Then install `skills/*` into their agent's skills directory
(see README's install table: opencode / Claude Code / Codex).

## 5. Measure their one-page budget (do together, once)

```powershell
python scripts/verify_one_page.py profile\cv\<their-cv>.docx
```

If it says `pages=1 lines=<N>`, set `line_budget` in `profile/tailor.json`
to `<N>`. Explain what this number means: *"this is how many lines your one
page actually holds — the kit will never let a tailored CV exceed it."*

## 6. Verify the whole loop works (walk them through it)

Run the built-in smoke test so they SEE it work before trusting it:

```powershell
python scripts/tests/test_tailor.py
```

Expect `PASS: tailor.py end-to-end`. Then demo one real task so they learn
the vocabulary, e.g.:

> "Copy-paste a job ad and say: *save this job*." →
> "Now say: *compare me with job 1*." →
> "Then: *tailor my CV for job 1*."

Reinforce the mental model: **search → save → analyze → tailor → verify →
track**, and that the AI shortlists but *they* decide.

## 7. Optional extras (offer, don't force)

- **Weekly sweep:** `powershell -File scripts\register-weekly-search.ps1`
  (Windows scheduler) — see `docs/browser-and-scheduling-tips.md`.
- **Chrome control (Codex):** let the AI fill forms up to the final click —
  same doc.

---

## Troubleshooting the first run

| Symptom | Likely cause | Fix |
|---|---|---|
| `paragraph not found` | An `anchors` string doesn't match their docx | Copy the exact text from their docx into `profile/tailor.json` |
| Tailored CV comes out 2 pages | Font inherited wrong default, or over budget | Re-run `tailor.py` (it preserves formatting); trim bullets/reduce `line_budget` |
| `no bullet template found` | Their CV uses style-level (not paragraph-level) bullets | Rare; report — the kit needs a bulleted paragraph to clone |
| `pip install python-docx` fails | No Python / pip | Install Python first, then retry |
| Word COM error on verify | No Word installed / pywin32 missing | Use `verify_one_page.ps1` (no deps) or skip verification manually |

## Language / tone when guiding

- Never assume they know `git clone`, `cd`, `pip`, or shell. Spell each out.
- Prefer doing it *for* them (you have the tools) over asking them to type.
- Only TWO things truly need the *user*'s own hands: putting their CV file in
  the right folder, and answering questions about their experience/preferences.
