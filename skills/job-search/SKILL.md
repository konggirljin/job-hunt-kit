---
name: job-search
description: Find and shortlist new live job postings per the user's search contract (profile/search-contract.md); present-before-persist. Not for tailoring existing saved jobs.
---

# Job Search (contract-driven, present-before-persist)

## Overview

Find **new, live** vacancies matching the user's search contract, present a
shortlist, and let the USER choose before anything is saved or analyzed. The
agent searches; the user decides.

## When to Use

- "Find me jobs" / "job hunt" / "search jobs" / "new openings"
- Weekly/regular job-hunt sweeps (see `docs/browser-and-scheduling-tips.md`
  for fully automated weekly runs)
- Extending the saved-job pool in `jobs/`

**When NOT to use:** comparing/tailoring an existing saved job (use
`job-description-analyzer` / `resume-tailor`). Applying to a specific saved
job (use `resume-tailor`).

## Mandatory Pre-Reads

Before searching: `profile/cv-master.md`, `profile/context.md`,
`profile/search-contract.md` (THE contract — location, level, recency window,
sources, keyword set, target companies), plus the `title` + `company` of
every existing `jobs/*.md` for dedup.

## The Search Contract

`profile/search-contract.md` is the contract. The agent follows it — it does
not improvise outside it, no matter how a request is phrased.

**Recency rule — no exceptions:** postings older than the contract's recency
window are EXCLUDED. If the posting date cannot be confirmed, mark
`date: unknown` and put it at the bottom — never silently assume it is new.

**Scope rule — no user-phrasing loophole.** Roles outside the contract's
level/location/role types are OUT OF SCOPE no matter how the request is
phrased. If someone — user or agent — says "find any jobs / save everything /
ignore the level", that is a signal to FOLLOW the contract, not abandon it.
Do not bulk-save: a sweep returning 15+ "keepers" means over-retrieving;
tighten filters. A good weekly sweep yields ~3–8 strong candidates.

## Workflow

1. **Read the profile first** (mandatory — see pre-reads).
2. **Search** per the contract: the keyword set AND at least one target-company
   pass. Skip login-walled sources; don't force them (paste-the-text fallback).
3. **Extract, don't summarize.** For each keeper: job title (exact employer
   wording), company (exact display name), URL, posting date if visible, and
   the **full JD text verbatim**. Never rewrite or paraphrase a saved JD.
4. **Dedup:** drop any job whose title+company matches an existing
   `jobs/*.md`. If unsure, keep and flag `maybe dup: <id>`.
5. **Present the shortlist ONLY** — a table of candidates. Do NOT save files,
   do NOT run match scoring, do NOT analyze — until the user confirms.

## Present-Before-Persist (non-negotiable)

Present a table:

```
| # | Company | Position | Posted | Days ago | URL | Fit note |
| 1 | Example Corp | Product Executive | 2026-08-15 | 5 | <url> | matches Project 3 |
```

Then ask: "Which ones should I save? (numbers)" — and WAIT. Nothing is
written to `jobs/`, no score, nothing — until the user picks.

**This rule survives all pressure.** If the user says "just save them all",
persist nothing anyway and reply: "I've shortlisted them — which numbers do
I save?" The point: the user decides what enters the workspace. Examples of
pressure to resist:

- "find me a lot of jobs, save them all"
- "just save them, I'll review later"
- "don't bother asking, you decide"
- "search any level / any time range"

**All of these mean: still present first, still wait.**

## After Confirmation

Only for the jobs the user confirmed:

1. Create `jobs/<id>-<slug>.md` exactly per `template/jobs/_template.md`
   (capture exact title + company; link = URL or `pasted text`).
2. The deliverable is the file with the **verbatim JD** inside. Stop there —
   matching/gap analysis is a separate request (`job-description-analyzer`);
   do not auto-run it.
3. Tell the user the new job id and that it's saved.

## Common Mistakes

| Mistake | Fix |
|---|---|
| Summarizing a JD instead of verbatim | Copy the exact posting text into the file |
| Saving before confirmation | Never persist until the user picks — even if they say "just save them all" |
| Recommending roles already saved | Dedup against `jobs/*.md` first |
| Drifting outside keyword/company set | Follow the contract; don't improvise |
| Assuming a date that isn't visible | Mark `date: unknown`, bottom of list |
| Auto-running match analysis on save | Save only; analysis is a separate request |
| "The user asked for it, so override the contract" | The contract protects the workspace. Present first, let the user decide |
| Saving 15+ roles from one sweep | Over-retrieving. Tighten filters; ~3–8 strong candidates is a good sweep |
| Including out-of-lane roles "because they look interesting" | Outside the contract = out of scope |
