# job-hunt-kit

An **agentic job-hunt workspace**: match analysis, contract-driven job
search, one-page CV tailoring, ATS checks, and an application tracker —
packaged as a kit of AI-agent skills + scripts. Clone it, fill in your
profile, and your coding agent (opencode / Claude Code / Codex) becomes a
disciplined job-hunt assistant.

Built while running a real, ongoing job hunt — every lesson in here was paid
for in a missed page-count or a wrongly-declared "skill gap".

## What's inside

| Piece | What it does |
|---|---|
| `skills/job-description-analyzer` | Match score vs any JD, gap analysis, red flags, apply/skip strategy |
| `skills/resume-tailor` | The full loop: config-driven docx build → one-page fit → ATS keyword check → change log |
| `skills/job-search` | Contract-driven weekly sweeps; **present-before-persist** (agent shortlists, YOU decide what's saved) |
| `skills/one-page-cv` | Shrink an overflowing CV onto exactly one page, verified with Word |
| `profile/` | Your private layer (gitignored): CVs, context, truthfulness calibration, search contract |
| `scripts/tailor.py` | Config-driven CV builder — preserves run formatting, no font bugs |
| `scripts/verify_one_page.py/.ps1` | Word doc-level page/line verification (the only stats that don't lie) |
| `scripts/extract_master.py` | docx → markdown capability-inventory sync |
| `scripts/register-weekly-search.ps1` | Windows Task Scheduler: weekly automated job-search sweep |
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

## Design principles

1. **Files are the source of truth.** Every job, application, and edit lives
   as a markdown/json file — a fresh agent session can pick up mid-hunt.
2. **The agent proposes, you dispose.** Present-before-persist everywhere:
   shortlists before saves, change logs before submissions, `[to fill]`
   before invented numbers.
3. **Truthfulness is calibrated, not absolute.** A 1-page CV is a
   condensation; the exhaustive inventory (`profile/cv-master.md`) is the
   real capability list. Gaps are judged against experience, and uncertain
   claims become a question, never a silent assumption
   (`profile/truthfulness.md`).
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
