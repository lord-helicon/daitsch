# Installiert den Skill daitsch. Verwendung:
#   .\install.ps1
#   .\install.ps1 -Ziel C:\pfad\zum\skillordner

param([string]$Ziel = "")

$ErrorActionPreference = "Stop"
$Name = "daitsch"
$Quelle = Split-Path -Parent $MyInvocation.MyCommand.Path

if ([string]::IsNullOrEmpty($Ziel)) {
    $AgentsDir = Join-Path $env:USERPROFILE ".agents\skills"
    if (Test-Path $AgentsDir) {
        $Ziel = Join-Path $AgentsDir $Name
    } else {
        $Ziel = Join-Path $env:USERPROFILE ".claude\skills\$Name"
    }
}

New-Item -ItemType Directory -Force -Path $Ziel | Out-Null

$QuellSkill = Join-Path $Quelle "skills\$Name"
Copy-Item (Join-Path $QuellSkill "SKILL.md") (Join-Path $Ziel "SKILL.md") -Force

# Jeden Unterordner des Skills mitnehmen. Eine feste Liste vergisst den naechsten.
Get-ChildItem -Path $QuellSkill -Directory | ForEach-Object {
    $pfad = Join-Path $Ziel $_.Name
    if (Test-Path $pfad) { Remove-Item -Recurse -Force $pfad }
    Copy-Item $_.FullName $Ziel -Recurse -Force
}
Write-Host "Installiert nach $Ziel"

$python = Get-Command python -ErrorAction SilentlyContinue
if ($null -eq $python) { $python = Get-Command python3 -ErrorAction SilentlyContinue }
if ($null -ne $python) {
    Write-Host ""
    & $python.Source (Join-Path $Ziel "scripts\klartext.py") --selbsttest
} else {
    Write-Host ""
    Write-Host "Python nicht gefunden. Der Skill funktioniert auch ohne, dann ohne Pruefskript."
}

Write-Host ""
Write-Host "Fuer andere Agenten liegen fertige Dateien in adapters\:"
Write-Host "  adapters\AGENTS.md                     ins Projektwurzelverzeichnis als AGENTS.md"
Write-Host "  adapters\CLAUDE.md                     als CLAUDE.md"
Write-Host "  adapters\GEMINI.md                     als GEMINI.md"
Write-Host "  adapters\cursor\daitsch.mdc            nach .cursor\rules\"
Write-Host "  adapters\copilot-instructions.md       nach .github\copilot-instructions.md"
Write-Host "  adapters\system-prompt.txt             in den Systemprompt beliebiger Agenten"
