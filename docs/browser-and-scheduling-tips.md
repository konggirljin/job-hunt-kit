# Browser control + weekly scheduled job search

Two optional power-ups: driving the browser with your agent (Codex-native
Chrome control), and running the job-search sweep automatically every week
via Windows Task Scheduler.

---

## 1. Chrome control (Codex)

Codex agents can drive Chrome natively — open pages, follow listings, read
postings. Nothing to install; the skill-side rules matter more than the
mechanism. Tips that make it actually good:

- **Dedup first, search second.** Before browsing, read the `title` +
  `company` of every existing `jobs/*.md` so the sweep doesn't re-find old
  jobs. The job-search skill mandates this.
- **Capture the JD verbatim.** A saved job's value is the FULL, unedited
  posting text (skills ask for it because paraphrase loses keywords). Select
  the whole description and paste it into `jobs/<id>-<slug>.md`.
- **Recency check before shortlisting.** Find the posted date on the page
  before a role earns a shortlist slot. No visible date → `date: unknown`,
  bottom of the list.
- **Login walls: don't fight them.** Some boards (LinkedIn especially) gate
  search results. Either browse while logged in, or fall back to
  paste-the-text: you copy the posting, the agent files it. Fighting a wall
  wastes tokens.
- **The agent browses, you decide.** Even with full browser control, the
  present-before-persist rule stands: the agent shortlists; you pick what's
  saved. Never let an automated run write files directly.
- **Respect robots/ToS.** Keep browsing human-paced (a handful of pages per
  sweep), no bulk scraping.

---

## 2. Weekly scheduled sweep (Windows)

### What you get

A Windows Task Scheduler job that runs your agent CLI headless once a week.
The agent re-reads your profile + search contract, sweeps the boards, and
appends a **shortlist** to `weekly-search.log` — it never saves files or
edits your workspace by itself. You open the log (or just ask your agent
"show last sweep"), reply with numbers, and the confirmed jobs get saved in
an interactive session.

### Quickstart

From the kit repo root (PowerShell):

```powershell
# register: every Monday 09:30 (defaults)
powershell -ExecutionPolicy Bypass -File scripts\register-weekly-search.ps1

# or customize
powershell -ExecutionPolicy Bypass -File scripts\register-weekly-search.ps1 `
    -TaskName MySweep -DayOfWeek Saturday -Time 10:00
```

### Which agent CLI runs it

By default the runner calls **opencode** headless (verified syntax):

```
opencode run "Weekly job-search sweep. Follow the job-search skill and
profile/search-contract.md. Present a shortlist table ONLY - do NOT save
any files. I will pick numbers later."
```

On a machine with **Codex** instead, set the command once:

```powershell
$env:KIT_AGENT_CMD = 'codex exec "Run the weekly job-search sweep per skills/job-search/SKILL.md. Shortlist only, save nothing."'
# persist it: [Environment]::SetEnvironmentVariable('KIT_AGENT_CMD', $env:KIT_AGENT_CMD, 'User')
```

(`codex exec` is the Codex headless mode — verify the exact flag on your
Codex install with `codex exec --help`.)

### Manage the task

```powershell
Get-ScheduledTask -TaskName WeeklyJobSearch        # does it exist / state
Start-ScheduledTask -TaskName WeeklyJobSearch      # run it now (test)
Get-Content weekly-search.log -Tail 50             # read the last sweep
Unregister-ScheduledTask -TaskName WeeklyJobSearch -Confirm:$false   # remove
```

- `-StartWhenAvailable` is set: if the PC was off at the scheduled time, the
  sweep runs when you next power on.
- Log lives at the repo root (`weekly-search.log`, gitignored).

### Privacy notes

- The sweep runs **locally** with your profile (CV mirrors, context) — the
  agent reads what it would read in an interactive session. Nothing new
  leaves your machine beyond what the agent CLI already sends to your model
  provider.
- The scheduled prompt forbids saving — shortlist only. Your `jobs/` folder
  only changes when YOU confirm picks.
- Results accumulate in `weekly-search.log`; it is gitignored. Delete it
  whenever you like.
