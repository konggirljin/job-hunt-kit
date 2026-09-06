---
name: one-page-cv
description: Fit an overflowing CV onto exactly one page — measure with Word doc-level stats, reclaim lines, rebuild via scripts/tailor.py, re-verify.
---

# One-Page CV

## When to Use This Skill

- "Does my CV fit one page?" / "make my CV 1 page" / "it's 2 pages, shrink it"
- After any tailoring that adds content (summary, skills, new blocks)
- Whenever `scripts/verify_one_page.py` reports `pages=2`

## The Method (measure → reclaim → rebuild → re-verify)

1. **Measure.** Never guess:

   ```
   python scripts/verify_one_page.py <file.docx> --budget <line_budget>
   ```

   Output: `pages=N lines=L budget=B`. Exit 0 only if `pages=1` and `L <= B`.
   Only DOC-level stats count (per-paragraph stats skip table lines — they
   lie). Get your true one-page line count once and store it as `line_budget`
   in `profile/tailor.json` (52 is an example, not a universal number).

2. **Reclaim lines.** Every addition costs lines elsewhere — there is no free
   space on a full page:

   - Trim 3-line bullets to 2 (keep the strongest evidence)
   - Shorten the professional summary to one line
   - Cut low-value skills items
   - Drop a whole low-relevance block (`remove_personal_blocks`)
   - Keep reworded text at or under the ORIGINAL character length
     (~95 chars/line at 11pt), or the wrap grows a line

3. **Rebuild via config, not by hand.** Put the edits in
   `tailoring-configs/<jobid>.json` and run `python scripts/tailor.py
   <jobid>` — it preserves run formatting (the "font bug": new runs without
   copied `rPr` inherit Calibri 12pt and silently double your page count).

4. **Re-verify** with the same command. Iterate 2–3 until `pages=1`.

## Judgement calls you may make (tell the user)

- Skipping PROFESSIONAL SUMMARY + SKILLS to fit more experience bullets is
  legitimate — say you did it and why.
- Which blocks to drop when everything seems important: lead with relevance
  to the target JD, recency second, uniqueness third.

## Common Failures

| Symptom | Cause | Fix |
|---|---|---|
| Same paragraph count, now 2 pages | Font bug — new runs lost `rPr` | Use tailor.py; don't hand-edit XML |
| Lines grew after a "small" reword | Wrap: text just over one line | Shorten the text below ~95 chars/line |
| Per-paragraph check says it fits, Word shows 2 pages | Table lines skipped by paragraph stats | Trust doc-level stats only |
| Bullet glyphs missing on new lines | Built from a non-bullet template | tailor.py uses `find_bullet_template()`; don't bypass |
| "paragraph not found" error | Anchor mismatch (en-dash/nbsp vs plain text) | Check `anchors` in `profile/tailor.json` against the real docx text |

Full lessons: `docs/one-page-cv-playbook.md`.
