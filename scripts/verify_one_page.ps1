# Verify a docx fits one page, using Word doc-level statistics.
# Usage:  powershell -File scripts\verify_one_page.ps1 -Path <file.docx> [-Budget 52]
# Exit 0 = 1 page within budget; exit 1 = over. Windows + Word required (COM; no pip installs).
param(
    [Parameter(Mandatory = $true)][string]$Path,
    [int]$Budget = 52
)
if (-not (Test-Path -LiteralPath $Path)) { Write-Error "file not found: $Path"; exit 1 }
$word = New-Object -ComObject Word.Application
$word.Visible = $false
try {
    $doc = $word.Documents.Open((Resolve-Path -LiteralPath $Path).Path, $false, $true)
    # Doc-level stats are the only trustworthy ones: per-paragraph
    # ComputeStatistics skips table lines, doc-level includes them.
    $lines = $doc.Range().ComputeStatistics(1)   # wdStatisticLines
    $pages = $doc.ComputeStatistics(2)           # wdStatisticPages
    $doc.Close($false)
} finally {
    $word.Quit()
    [System.Runtime.InteropServices.Marshal]::ReleaseComObject($word) | Out-Null
}
Write-Output "pages=$pages lines=$lines budget=$Budget"
if ($pages -eq 1 -and $lines -le $Budget) { exit 0 } else { exit 1 }
