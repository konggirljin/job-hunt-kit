---
name: resume-tailor
description: Tailor a CV for a specific job — config-driven docx build, one-page fit, ATS keyword check, change log. The full tailoring loop in one skill.
---

# Resume Tailor (tailoring + ATS in one loop)

## When to Use This Skill

Use when the user wants to:
- Customize their CV for a specific job posting
- Create a targeted version of their CV
- Check if their CV will pass ATS / why applications get no responses
- Mentions: "tailor CV", "customize resume", "match job description",
  "ATS", "keyword optimization", "not getting interviews"

Run `job-description-analyzer` FIRST to know what to emphasize and whether
the effort is worth it.

## Mandatory Pre-Reads (before judging any gap or keyword)

1. `profile/cv-master.md` — exhaustive inventory of real experience. A
   keyword absent from the 1-page CV is NOT a gap if it is here.
2. `profile/context.md` — constraints and extra requirements.
3. `profile/truthfulness.md` — canonical 3-tier truthfulness framework.
   Never re-derive tiers here. Never transplant example claims; reword only
   what is TRUE; missing metrics → `[to fill]`.

## The Full Loop (5 stages)

### Stage 1 — ANALYZE

Run `job-description-analyzer`: match score, gaps, strengths, red flags. If
the match is poor, say so — don't burn an hour tailoring a 40% job.

### Stage 2 — BUILD

Write `tailoring-configs/<jobid>.json` (see
`template/tailoring-configs/job-example.json`), then:

```
python scripts/tailor.py <jobid>
```

Config keys (all optional except `company` + `position`):

| Key | Purpose |
|---|---|
| `company` / `position` | REQUIRED — output is named `{name}_{Company} {Position}.docx` |
| `summary` | One-line professional summary inserted after the contact line |
| `skills` | Skills line inserted right after the summary |
| `project_order` | `[{find, title}]` — reorder project blocks, retitling each |
| `reword` | `[{find, text}]` — rewrite any paragraph by prefix |
| `first_bullet` | `[{title, text}]` — replace a project's lead bullet |
| `insert_after` | `[{find, text}]` — new plain paragraph after a match |
| `insert_bullet_after` | `[{find, text}]` — new bulleted line after a match |
| `insert_block_before` | `[{find, title, bullets}]` — new titled block |
| `insert_job_before` | `[{find, title, date, bullets}]` — new job entry (header table + bullets) |
| `remove_paras` | `[{find}]` — delete paragraphs by prefix |
| `remove_personal_blocks` | `[table title]` — drop a whole personal-project block |

The script preserves run formatting (the "font bug" — see playbook). Errors
like "paragraph not found" mean an anchor in `profile/tailor.json` doesn't
match your docx text.

### Stage 3 — FIT ONE PAGE

```
python scripts/verify_one_page.py tailored/<output>.docx --budget <line_budget>
```

- Target: `pages=1`, `lines <= line_budget` (exit 0).
- Only trust DOC-level statistics (per-paragraph stats skip table lines).
- Over budget? Reclaim lines: trim 3-line bullets to 2, shorten the summary
  to one line, cut skills items, drop a low-value block. Adding sections
  ALWAYS costs lines elsewhere — there is no free space.
- Keep reworded bullets at or under the original character length, or the
  wrap grows a line (~95 chars/line at 11pt is typical).
- You MAY deliberately drop the summary/skills to fit more experience bullets
  — but tell the user you did, and why.

### Stage 4 — ATS CHECK

- Extract JD keywords: hard skills, soft skills, industry terms.
- Match: exact phrase in CV? synonyms? frequency? location (summary/skills/bullets)?
- Score = matched / required keywords; target 80%+.
- Placement priority: 1) summary (5–8 critical keywords), 2) skills section
  (exact JD phrasing), 3) bullets (naturally woven).
- Critical keywords 2–4× each; never keyword-stuff.
- Formatting rules: single column, standard section headers ("Work
  Experience", "Skills", "Education"), no tables/text boxes/graphics in the
  data path, standard fonts, contact info in body (not header/footer),
  consistent MM/YYYY dates, standard bullets.
- Recommended changes must NEVER fabricate claims to hit a keyword. Reword
  what is TRUE; use `[to fill]` for missing metrics.

### Stage 5 — LOG

Write two artifacts next to the output:
1. `<jobid>-change-log.md` — truthful before/after for every edit
   (summary, skills, reorders, rewords, blocks added/removed).
2. `<jobid>-ats-report.md` — keyword table (found/missing/counts), match
   score before/after, formatting check results.

Both feed interview prep later — keep them honest.

## One-Page Playbook (condensed)

Full version: `docs/one-page-cv-playbook.md`. The essentials:

- **The font bug:** any NEW paragraph must copy `w:rPr` from a real body run.
  New runs without it inherit the doc default (often Calibri 12pt) instead of
  the CV font (often Times New Roman 11pt) — taller lines, same paragraph
  count renders as 2 pages. `scripts/tailor.py` handles this; don't bypass it.
- **The budget is exact:** measure YOUR CV once with the verify script; the
  number is your `line_budget` in `profile/tailor.json`. Zero slack.
- **Bullet templates must carry `numPr`:** new bulleted lines cloned from a
  non-bullet paragraph lose the glyph. tailor.py picks a real bullet as the
  template.
- **Verify page count the reliable way:** doc-level `ComputeStatistics(2)` /
  `ComputeStatistics(1)` only (Word COM via the verify scripts).

## Quick Checklist

Before submitting any tailored CV:

1. ✅ Summary mentions the exact job title/function
2. ✅ Top 5 skills match the JD's top 5 requirements
3. ✅ Most relevant experience is positioned first
4. ✅ Each project's lead bullet addresses the JD's key requirement
5. ✅ JD keywords appear naturally throughout (2–4× for critical ones)
6. ✅ Company/industry terminology used correctly
7. ✅ All claims truthful per `profile/truthfulness.md` — no invented metrics
8. ✅ File named `{name}_{Company} {Position}.docx`
9. ✅ ATS formatting maintained (Stage 4 rules)
10. ✅ Change log + ATS report written and saved

## Version Management

- Keep ONE master CV per variant as the source of truth; tailored CVs are
  derived copies — never edit a master for a single job.
- Multiple CV variants? Record which is the tailoring base in
  `profile/tailor.json` (`source_cv`).
- Keep the change log per job for interview prep reference.
