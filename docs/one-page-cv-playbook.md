# One-Page CV Playbook — lessons for fast, correct tailoring

Read this BEFORE any "tailor my CV for job X" or "fit this onto one page"
task. It exists so a fresh session (new machine, no chat history) can tailor
the next CV quickly without repeating the slow/debuggy first pass.

## Output naming formula (mandatory)

Tailored CVs are named `<name>_<Company> <Position>.docx` (e.g.
`Alex Chan_Example Corp Business Analyst.docx`). `name` comes from
`profile/tailor.json`; `company`/`position` come from the per-job config;
`scripts/tailor.py` builds the filename automatically (sanitizing invalid
path characters). Do not use ad-hoc names.

## The variants concept

Keep separate master docx files in `profile/cv/`:

- **Tailoring base** (`profile/tailor.json` → `source_cv`): your default
  1-page CV used for most applications.
- **Special variants** (optional): e.g. a humbler/adjusted version for one
  specific employer, or a 3-page "everything master" content repository.
- The everything-master is NOT a tailoring base — pull relevant bullets into
  a per-job config only when a JD warrants it. Keep the default base for
  everything else.
- Never edit a master for a single job. Tailored CVs are derived copies.

## How to tailor (fast path)

1. Create `tailoring-configs/<jobid>.json` (see
   `template/tailoring-configs/job-example.json`): `summary`, `skills`,
   `project_order`, `reword`, `first_bullet`, inserts/removals — plus
   `company` + `position` so the output is named correctly.
2. Run `python scripts/tailor.py <jobid>` from the repo root.
3. **Verify one page** (see below) — the #1 time sink if skipped.
4. Write `<jobid>-change-log.md` (truthful, lists edits) and run the ATS
   keyword check (see `skills/resume-tailor/SKILL.md`, Stage 4).

## CRITICAL lessons (from a slow, debuggy first pass — do not regress)

### 1. The font bug (the big one)

New paragraphs created by the script MUST copy `w:rPr` from a real body run.
If a run has no rPr it inherits the document default (often **Calibri 12pt**,
not the CV's Times New Roman 11pt). Calibri 12pt is taller → the same line
count renders as **2 pages**. The fix is baked into `scripts/tailor.py`
(`make_para`/`set_text` always copy run formatting) — do not bypass it.

### 2. The one-page budget is EXACT

Measure YOUR CV once:

```
python scripts/verify_one_page.py profile\cv\<your-master>.docx
```

The number of lines it reports for a 1-page render is your real budget —
record it as `line_budget` in `profile/tailor.json`. There is essentially
zero slack. Rule: **total lines must stay within budget.**

- Adding PROFESSIONAL SUMMARY + SKILLS costs ~4–6 lines. To fit, you MUST
  reclaim lines elsewhere (trim 3-line bullets to 2, shorten the summary to
  one line, cut skills items). You cannot add sections without trimming.
- A bullet paragraph fits ~95 chars per line at 11pt. Keep reworded bullets
  at or under the original character length, else the wrap grows a line.
- [Optional] You may deliberately skip the summary+skills to keep more
  experience bullets. That is a legitimate judgement call — but tell the
  user you did it, and why.

### 3. Verify page count the reliable way

Per-paragraph `ComputeStatistics` and doc-level stats can DISAGREE
(paragraph stats skip table lines; doc-level includes them). Trust
**doc-level** only:

```
python scripts/verify_one_page.py <file.docx> --budget <line_budget>
# or, with zero pip installs:
powershell -File scripts\verify_one_page.ps1 -Path <file.docx> -Budget <line_budget>
```

If over budget, find what wraps wrong with per-paragraph
`ComputeStatistics(1)` (only paragraphs with >1 line matter) — in Word via
COM, or just eyeball the docx.

### 4. Where bullets live (in a typical CV)

- Personal-project bullets are plain paragraphs AFTER the header tables in
  the body — not inside the tables. Table headers are rows of the tables.
- Project titles often use an **en-dash (–)** (e.g. `Project 3 – Foo`).
  Search with the en-dash prefix; renamed titles typically use plain hyphens.
- Watch for **non-breaking spaces (`\xa0`)** in titles copied from other
  documents — prefix matching with normal spaces will FAIL. Match on a
  stable shorter prefix, or search for a distinctive word instead.

### 5. Inserted blocks lose bullet glyphs — the classic root-cause bug (FIXED)

- **Symptom:** any bullet line added via `insert_block_before` renders
  WITHOUT a bullet point (•). Cause: building bullet paragraphs from the
  *body* template (which has no `w:numPr`), so new lines lose their bullet.
- **Fix (in `scripts/tailor.py`):** `find_bullet_template(body)` finds the
  first paragraph carrying `numPr`; ALL bullet-creating functions build from
  it. `insert_job_before` clones the job-header **table** (title cell +
  right-aligned date cell) so a new entry renders as a standalone job, not
  as a project under another employer.
- **Config field choice:** use `insert_job_before` (not
  `insert_block_before`) when adding a separate job/role. Each item:
  `{find, title, date, bullets}`.
- **Lesson:** when adding ANY new bulleted line, always build from a real
  bullet paragraph (one with `numPr`), never from the body/text template.

### 6. Reorder mechanics (in tailor.py, already correct)

- `get_block` reads siblings from a project title until the next project
  title or the personal-projects header. Blocks are re-titled, removed from
  the body, and re-inserted before the personal-projects header in the
  desired order.
- `first_bullet` must STOP at the next project title — an early buggy
  version iterated all siblings and wrongly replaced the *next* project's
  first bullet.

## Truthfulness

Canonical rules live in `profile/truthfulness.md` (three tiers). The one-line
version: the 1-page CV is a condensation, not the full capability list —
read `profile/cv-master.md` + `profile/context.md` before judging any gap;
a missing CV keyword is NOT a gap; missing metrics → `[to fill]`, never
invent numbers; ask the user with the FULL JD sentence when unsure.

## Tooling / environment

- Python + `python-docx` (pip install python-docx).
- Windows + Word for verification (COM): `scripts/verify_one_page.py`
  (pywin32) or `scripts/verify_one_page.ps1` (no dependency).
- Keep the config files in the repo (`tailoring-configs/`) so another
  machine can `git clone` and re-run. (Real configs contain JD-derived text
  about YOUR applications — they are gitignored by default; commit them only
  in your PRIVATE copy of this workspace if you fork the kit.)
