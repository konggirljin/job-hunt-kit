# Runs the weekly job-search sweep via your agent CLI, headless.
# Invoked by the Windows Task Scheduler job created by register-weekly-search.ps1.
# The prompt enforces present-before-persist: the agent shortlists, it never saves.
param(
    [string]$AgentCommand = ""
)
$ErrorActionPreference = "Continue"
$root = Split-Path -Parent $PSScriptRoot   # repo root (scripts/ -> root)
if (-not $AgentCommand) {
    $AgentCommand = $env:KIT_AGENT_CMD
}
if (-not $AgentCommand) {
    $AgentCommand = 'opencode run "Weekly job-search sweep. Follow the job-search skill and profile/search-contract.md. Present a shortlist table ONLY - do NOT save any files, do NOT run analysis. I will pick numbers later."'
}
$log = Join-Path $root "weekly-search.log"
$stamp = Get-Date -Format "yyyy-MM-dd HH:mm"
Push-Location $root
try {
    "=== $stamp ===" | Add-Content -Path $log
    Invoke-Expression $AgentCommand 2>&1 | Out-String | Add-Content -Path $log
    "=== done ===" | Add-Content -Path $log
} finally {
    Pop-Location
}
