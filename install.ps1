# Universal PowerShell Installer for day-trader-india (Windows)
# Supports: Google Antigravity, Claude Code, Cursor, and Codex.

param(
    [string]$Target = "auto"
)

$ScriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path

Write-Host "============================================================" -ForegroundColor Cyan
Write-Host "  Day Trader India (day-trader-india) Windows Installer     " -ForegroundColor Cyan
Write-Host "============================================================" -ForegroundColor Cyan

$Skills = @(
    "trader-scanner",
    "trader-fii-dii",
    "trader-oi",
    "trader-news",
    "trader-entry",
    "trader-exit",
    "trader-timemachine",
    "trader-budget",
    "trader-risk",
    "trader-broker",
    "trader-alerts",
    "trader-analyst"
)

function Install-To([string]$Path, [string]$Name) {
    Write-Host "-> Installing to $Name ($Path)..." -ForegroundColor Yellow
    if (!(Test-Path $Path)) { New-Item -ItemType Directory -Path $Path -Force | Out-Null }
    foreach ($s in $Skills) {
        $source = Join-Path $ScriptDir $s
        if (Test-Path $source) {
            $dest = Join-Path $Path $s
            if (Test-Path $dest) { Remove-Item -Recurse -Force $dest }
            Copy-Item -Recurse -Path $source -Destination $dest
            Write-Host "   ✓ Installed $s" -ForegroundColor Green
        }
    }
}

$HomeDir = [Environment]::GetFolderPath("UserProfile")

if ($Target -eq "antigravity" -or $Target -eq "all" -or ($Target -eq "auto" -and (Test-Path "$HomeDir\.agents"))) {
    Install-To "$HomeDir\.agents\skills" "Google Antigravity"
}

if ($Target -eq "claude" -or $Target -eq "all" -or ($Target -eq "auto" -and (Test-Path "$HomeDir\.claude"))) {
    Install-To "$HomeDir\.claude\skills" "Claude Code"
}

if ($Target -eq "codex" -or $Target -eq "all" -or ($Target -eq "auto" -and (Test-Path "$HomeDir\.codex"))) {
    Install-To "$HomeDir\.codex\skills" "Codex"
}

Write-Host "============================================================" -ForegroundColor Cyan
Write-Host "  Success! 12 Indian Day Trading skills installed.          " -ForegroundColor Green
Write-Host "============================================================" -ForegroundColor Cyan
