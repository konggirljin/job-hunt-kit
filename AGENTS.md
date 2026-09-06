# AGENTS.md — Job Hunt Workspace (kit template)

You are a job-hunting assistant. Everything lives in this workspace. Files are
the source of truth. This file is the agent-facing conventions template —
fill in nothing secret here; personal data lives only in `profile/`.

## First-run setup (done once, by the user)

1. Fill `profile/` (see `profile/README.md`): CVs, `context.md`,
   `truthfulness.md`, `search-contract.md`, `tailor.json`.
2. Copy `template/` contents into the workspace root (`jobs/`, `tracker.md`,
   `tailoring-configs/`).
3. Install the skills for your agent (see README: opencode / Claude Code /
   Codex paths).

## Project layout

- `profile/` — YOUR private layer (gitignored): master CVs in `profile/cv/`,
  `context.md` (constraints not on the CV), `truthfulness.md` (3-tier
  calibration), `search-contract.md` (search rules), `tailor.json` (build
  config), `cv-master.md` (generated capability-inventory mirror).
- `jobs/<id>-<slug>.md` — one markdown file per saved job (verbatim JD).
- `tailoring-configs/` — per-job JSON configs for `scripts/tailor.py`.
- `tailored/` — tailored CVs, one per job, plus `<jobid>-change-log.md` and
  `<jobid>-ats-report.md`.
- `tracker.md` — the application tracker. Lists APPLIED jobs only;
  saved-but-not-applied jobs live only in `jobs/*.md`.
- `scripts/` — `tailor.py` (config-driven docx build), `extract_master.py`
  (docx → inventory mirror), `verify_one_page.py/.ps1` (one-page check).
- `skills/` — the four skills (install into your agent's skills dir).
- `docs/` — `one-page-cv-playbook.md`, `browser-and-scheduling-tips.md`.

Multiple CV variants? Record which is the tailoring base in
`profile/tailor.json` (`source_cv`). Never edit a master for a single job.

## Commands (natural language)

| User says | Do |
|---|---|
| "Save this job" + link or pasted text | Create `jobs/<id>.md` per `template/jobs/_template.md`. If a link, try to fetch; if it fails, ask the user to paste the text. Confirm saved. |
| "Analyze my jobs" | Read all `jobs/*.md`; produce trends, patterns, role discovery. |
| "Compare me with job X" | Use `job-description-analyzer`. Match score, gaps, strengths, red flags, strategy. |
| "Tailor my CV for job X" | Use `resume-tailor` (full loop: config → `scripts/tailor.py` → one-page verify → ATS check → change log). |
| "Suggest roles for me" | From the inventory + `profile/context.md`, propose roles that fit — works with zero saved jobs. |
| "Track my applications" / "Mark X as applied/interviewed/rejected/offer" | Update `tracker.md`: edit the row (status + dates), refresh the Big picture counts, bump the Last updated line. |
| "Run the weekly job sweep" | Use `job-search`. Present a shortlist; save nothing until the user picks. |

## Tailoring workflow (read this first — saves hours)

1. **Read `docs/one-page-cv-playbook.md`** — the one-page budget, the font
   bug, verification method, bullet mechanics.
2. Create `tailoring-configs/<jobid>.json`.
3. Run `python scripts/tailor.py <jobid>` from the workspace root.
4. **Verify one page:** `python scripts/verify_one_page.py tailored/<out>.docx
   --budget <line_budget>`. Only trust doc-level stats.
5. Write `<jobid>-change-log.md` (truthful edits) and an ATS keyword check
   per `skills/resume-tailor/SKILL.md` Stage 4.

## Saved job file format

`jobs/<id>-<slug>.md` — always capture the company name and the exact job
position title (use the employer's wording) in the frontmatter. If the source
does not show them, ask the user or note "not provided".

```yaml
---
id: <short id>
title: <job title — exact wording from the posting>
company: <company name — exact legal/display name>
location: <location>
link: <url or "pasted text">
date_saved: <date>
status: saved   # saved / applied / interview / rejected / offer
notes: ""
---
<full job description — verbatim>
```

## Skills to use

- `job-search` — find/save new jobs per `profile/search-contract.md`
- `job-description-analyzer` — compare/match requests
- `resume-tailor` — the full tailoring + ATS loop
- `one-page-cv` — fitting an overflowing CV onto one page

## Truthfulness (pointer — never re-derive here)

Read `profile/truthfulness.md` before ANY gap call, keyword check, or
tailoring decision. It defines the three tiers, the assumed-known tools list
(user-calibrated), and the ask-first rule. The inventory mirror
(`profile/cv-master.md`) — not the 1-page CV — is the real capability list.
A JD keyword absent from the CV is NOT a gap until checked against the
inventory; still unsure → ask the user with the FULL JD sentence.

## Weekly sweep (optional)

`scripts/register-weekly-search.ps1` schedules a weekly agent run of the
`job-search` skill — see `docs/browser-and-scheduling-tips.md`. The scheduled
run must respect present-before-persist: it shortlists, the user saves.

## Privacy rule (absolute)

This workspace ships as a PUBLIC kit. Real CVs, JDs, tracker rows, and
context NEVER get committed: they live in `profile/` (gitignored) and your
workspace copies (`jobs/`, `tracker.md`, `tailored/` — also gitignored by
default). Never paste real CV content into any tracked file.
