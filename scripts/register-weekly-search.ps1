# Registers (or replaces) a weekly Windows Task Scheduler job that runs
# scripts/weekly-search.ps1 - the headless agent job-search sweep.
#
# Usage (from the kit repo root, PowerShell):
#   powershell -ExecutionPolicy Bypass -File scripts\register-weekly-search.ps1
#   optional: -TaskName MySweep -DayOfWeek Saturday -Time 10:00
#
# Remove it again with:
#   Unregister-ScheduledTask -TaskName WeeklyJobSearch -Confirm:$false
param(
    [string]$TaskName = "WeeklyJobSearch",
    [ValidateSet("Sunday","Monday","Tuesday","Wednesday","Thursday","Friday","Saturday")]
    [string]$DayOfWeek = "Monday",
    [string]$Time = "09:30",
    [string]$Workspace = (Split-Path -Parent $PSScriptRoot)
)
$runner = Join-Path $Workspace "scripts\weekly-search.ps1"
if (-not (Test-Path $runner)) { Write-Error "runner not found: $runner"; exit 1 }

$action   = New-ScheduledTaskAction -Execute "powershell.exe" `
              -Argument "-NoProfile -ExecutionPolicy Bypass -WindowStyle Hidden -File `"$runner`"" `
              -WorkingDirectory $Workspace
$trigger  = New-ScheduledTaskTrigger -Weekly -DaysOfWeek $DayOfWeek -At $Time
$settings = New-ScheduledTaskSettingsSet -StartWhenAvailable -DontStopIfGoingOnBatteries -AllowStartIfOnBatteries

Register-ScheduledTask -TaskName $TaskName -Action $action -Trigger $trigger `
    -Settings $settings `
    -Description "job-hunt-kit weekly agent job-search sweep (shortlist only, never auto-saves)" `
    -Force | Out-Null
Write-Output "Registered scheduled task '$TaskName': weekly $DayOfWeek at $Time"
Write-Output "Runner: $runner"
Write-Output "Log will appear at: $(Join-Path $Workspace 'weekly-search.log')"
Write-Output "Remove with: Unregister-ScheduledTask -TaskName $TaskName -Confirm:`$false"
