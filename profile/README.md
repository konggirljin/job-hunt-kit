# profile/ — your private layer (gitignored)

This folder is the ONLY place your personal data lives, and it is gitignored —
nothing in it ever gets committed. The published kit ships templates only.

## Set up once (in order)

1. **Drop your CVs** into `profile/cv/`:
   - `master-external.docx` — your default 1-page tailoring base
   - (optional) other variants, e.g. an internal/steadier version for one
     employer, or a 3-page `*MASTER*` content repository of everything
2. **Copy each template to its real name** (drop `.template`):
   - `context.template.md` → `context.md`
   - `truthfulness.template.md` → `truthfulness.md` — then EDIT the TIER 2
     "assumed known" list to your own tools
   - `search-contract.template.md` → `search-contract.md` — then fill the table
3. **Copy `tailor.json.example` → `tailor.json`** and fill it:
   - `name` — the filename prefix for tailored CVs (`<name>_<Company> <Position>.docx`)
   - `source_cv` — which docx is the tailoring base
   - `line_budget` — how many Word lines fit your one page (measure YOUR CV
     with `scripts/verify_one_page.py` first; 52 is an example, not a rule)
   - `anchors` — literal text fragments that exist in YOUR CV (contact line,
     an education-section header, a body sentence, the personal-projects
     header, etc.). tailor.py uses them to find edit points. Wrong anchors →
     "paragraph not found" errors. Check spelling against your docx.
   - `extract_docx_glob` / `extract_out` — which docx mirrors into the
     capability-inventory markdown
4. **Sync the inventory mirror:** `python scripts/extract_master.py`
   (re-run whenever the source docx changes in Word)

## Verify your setup

```powershell
python scripts/verify_one_page.py profile\cv\<your-master>.docx --budget <your line_budget>
```

You should get `pages=1 lines=<n>`. If pages=2, your real budget is smaller
than you think — count again after any layout change.
