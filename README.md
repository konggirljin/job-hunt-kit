# job-hunt-kit

**[English](README.md) · [繁體中文](README.zh-Hant.md) · [简体中文](README.zh-Hans.md)**

> An **all-in-one, AI-driven job-hunt machine**, built during a real job hunt.
> It finds jobs for you, scores your fit, writes and tailors your CV as a
> **real one-page Word document**, ATS-checks it, tracks every application —
> and, via Chrome control (e.g. Codex), runs the whole grunt work end-to-end,
> stopping only at the final "submit" click.

Built while running a real, ongoing job hunt. Every lesson in here was paid
for in a missed page-count or a wrongly-declared "skill gap".

---

## Why this one

Most "AI CV tools" output a wall of text you must hand-format back into a
resume. This kit is different because it operates on the **actual Word
document** your recruiter will open:

- **One-page `.docx`, verified.** Not "fits roughly one page." The kit edits
  the real Word file and measures it with Word's own page/line statistics so
  you *know* it's one page. No font bugs, no drift.
- **Auto job search.** Point it at your target market and it sweeps the
  boards weekly (or any cadence you set), dedupes, and brings you a
  shortlist.
- **Auto fit-score.** Every JD gets a match score, gap analysis, and red-flag
  check — so you spend effort only on roles worth it.- **Auto CV writing + tailoring.** From a per-job config, it generates the
  tailored `.docx`, reorders your strongest experiences, and ATS-optimizes
  keywords — all while keeping claims truthful (no invented numbers).
- **Chrome control that saves your time.** With a browser-controlling agent
  (Codex), it can open listings, read JDs, even fill in application forms by
  itself — and hand off to you only for the final approval. You spent your
  time judging, not copy-pasting.
- **Full pipeline, one place.** Search → analyze → tailor → verify → track.
  Everything lives as files, so any fresh agent session picks up mid-hunt.

## What's inside

| Piece | What it does |
|---|---|
| `skills/job-description-analyzer` | Match score vs any JD, gap analysis, red flags, apply/skip strategy |
| `skills/resume-tailor` | The full loop: config-driven docx build → one-page fit → ATS keyword check → change log |
| `skills/job-search` | Contract-driven weekly sweeps; **present-before-persist** (agent shortlists, YOU decide what's saved) |
| `skills/one-page-cv` | Shrink an overflowing CV onto exactly one page, verified with Word |
| `profile/` | Your personal files (gitignored — never pushed to GitHub): CVs, context, truthfulness calibration, search contract |
| `scripts/tailor.py` | Config-driven CV builder — produces a real `.docx`, preserves formatting |
| `scripts/verify_one_page.py/.ps1` | Word page/line verification |
| `scripts/extract_master.py` | docx → markdown capability-inventory sync |
| `scripts/register-weekly-search.ps1` | Windows Task Scheduler: weekly automated job-search sweep |
| `docs/browser-and-scheduling-tips.md` | Chrome-control tips for guiding AI through job boards |
| `AGENTS.md` | The workspace conventions your agent reads |

## The workflow

```
job-search ──▶ jobs/<id>.md (verbatim JD)
     │                │
     │                ▼
     │        job-description-analyzer (match score, gaps)
     │                │
     ▼                ▼
weekly sweep   resume-tailor ──▶ tailored/<name>_<Company> <Position>.docx
(shortlist)         │                    │
     │              │            verify_one_page (pages=1)
     │              │                    │
     ▼              ▼                    ▼
  you pick    change log + ATS report ─▶ tracker.md
```

## Brand new to git / GitHub / agents? Let your AI set it up

You don't need to know any of this. Copy-paste the prompt below into your AI
assistant (Claude, Codex, opencode, ChatGPT…) and it will walk you through
everything from zero — the only things you'll personally do are drop your CV
into a folder and answer questions. Your AI follows the same guide the kit's
own agents use: `docs/getting-started.md`.

<details>
<summary>Click to reveal the copy-paste prompt</summary>

```text
You are going to set up "job-hunt-kit" for me from scratch. I have ZERO
experience with GitHub, git, the command line, Python, or AI agents — so
please do everything for me, or explain each step in plain, non-technical
language.

This is the project: <paste the git clone URL or GitHub repo link here>

Here is what I want:
1. First, follow the guide in docs/getting-started.md in that repo — it tells
   YOU how to guide a total beginner like me.
2. Tell me exactly what files I need to prepare. I understand I need at least
   my CV as a .docx file. Explain how to produce a .docx if I only have a PDF.
3. Walk me through getting the kit onto my computer, one step at a time.
4. Help me fill the "profile" folder (my CV, my truthfulness notes, any extra
   context about me, my job-search preferences).
5. Set up my AI agent so it can use the kit's skills.
6. Then run the built-in test and show me it works, and demo one real task
   (like "tailor my CV" or "search jobs") so I know how to use it going
   forward.

Important: assume I know nothing — define every term, do the technical steps
for me where you can, and only make me type things when truly necessary.
Start by telling me what to prepare.
```

</details>

## Quickstart (5 minutes)

```powershell
git clone <your-repo-url>/job-hunt-kit.git my-job-hunt
cd my-job-hunt
```

1. **Fill `profile/`** — follow `profile/README.md`:
   drop your CV(s) into `profile/cv/`, copy each `*.template.md` to its real
   name and fill it (context, truthfulness, search contract), copy
   `tailor.json.example` → `tailor.json` and point it at your CV.
2. **Copy the workspace templates** into the root:

   ```powershell
   New-Item -ItemType Directory -Force jobs, tailored, tailoring-configs | Out-Null
   Copy-Item template\jobs\_template.md jobs\
   Copy-Item template\tracker.template.md tracker.md
   Copy-Item template\tailoring-configs\job-example.json tailoring-configs\
   ```

3. **Install the skills** for your agent (below).
4. Sync your capability inventory: `python scripts/extract_master.py`
5. Talk to your agent: *"save this job"*, *"compare me with job X"*,
   *"tailor my CV for job X"* — see `AGENTS.md` for the full command set.

### Install skills per platform

Copy (or symlink) each folder in `skills/` into your agent's skills
directory:

| Agent | Path |
|---|---|
| opencode | `<workspace>\.agents\skills\` (or global config dir) |
| Claude Code | `~/.claude/skills/` (or `.claude/skills/` in the workspace) |
| Codex | `<workspace>\.codex\skills\` |

Windows symlinks need admin/Dev Mode — plain copies are the default.

### Requirements

- Python 3.10+ with `pip install python-docx` (tailoring + extraction)
- Windows + Microsoft Word for one-page verification
  (`pip install pywin32` for the .py verifier; the `.ps1` one needs nothing)
- An agent CLI: opencode (verified), Claude Code, or Codex

## Weekly automated sweep (optional, Windows)

```powershell
powershell -ExecutionPolicy Bypass -File scripts\register-weekly-search.ps1
```

Runs your agent headless once a week against your search contract and logs a
**shortlist only** — nothing is saved until you pick. Details, Chrome-control
tips (Codex), and task management: `docs/browser-and-scheduling-tips.md`.

## Chrome control: let the AI do everything but the final click

With a browser-driving agent (Codex's native Chrome control), the full loop
handsfree:

1. AI opens boards, reads JDs, dedupes, shortlists.
2. AI drafts each application + tailored CV.
3. AI fills the form fields (name already on file, address, work history,
   the upload), pastes JD-specific answers.
4. **One human checkpoint:** you review the filled form once, then click
   submit. (Or tell the agent to submit only after you approve.)

You keep the decisions; the AI keeps the typing. Full recipe in
`docs/browser-and-scheduling-tips.md`.

## Design principles

1. **Files are the source of truth.** Every job, application, and edit lives
   as a markdown/json file — a fresh agent session can pick up mid-hunt.
2. **The agent proposes, you dispose.** Present-before-persist everywhere:
   shortlists before saves, change logs before submissions, `[to fill]`
   before invented numbers.
3. **Calibrated honesty — not naive literalism.** A one-page CV is a
   condensed highlight, not the full record. Judge whether a gap is real by
   your actual work experience, and treat basic skills (e.g. MS Office) as
   assumed — so the AI doesn't mistake over-literal reading for honesty and
   lose common sense. When something is genuinely uncertain, the AI stops
   and asks you (`profile/truthfulness.md`).
4. **One page, verified.** Page counts are measured with Word doc-level
   statistics every time — per-paragraph stats skip table lines and lie.
5. **The workspace never holds your secrets in git.** Everything personal is
   gitignored from commit #1.

## Privacy pledge

**This repo ships zero personal data.** Your CVs, context, search contract,
JDs, and tracker live in gitignored paths (`profile/`, `jobs/`, `tailored/`,
`tracker.md`). If you fork this kit, keep it that way — never commit real CV
data here.

## Credits

- [`resume-tailor`, `resume-ats-optimizer`, `job-description-analyzer`
  lineage: Paramchoudhary/ResumeSkills](https://github.com/Paramchoudhary/ResumeSkills)
  (MIT) — heavily modified and merged with original workflows (search
  contract, present-before-persist, one-page playbook, tailored-build
  tooling).
- Inspired by the skills ecosystem: `anthropics/skills`, `obra/superpowers`.

## License

MIT — see [LICENSE](LICENSE).
