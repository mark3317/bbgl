param([string]$Output = '', [string]$Compiler = 'C:\msys64\clang64\bin\clang.exe')
$ErrorActionPreference = 'Stop'
$repoPath = [IO.Path]::GetFullPath((Join-Path $PSScriptRoot '..\..'))
if (!$Output) { $Output = Join-Path $repoPath 'out\profile-launchers' }
New-Item -ItemType Directory -Path $Output -Force | Out-Null
foreach ($playerNumber in 1..3) {
    $targetExe = Join-Path $Output "Bloodborne Player $playerNumber.exe"
    & $Compiler -std=c11 -O2 -Wall -Wextra -Werror -static -municode -mwindows "-DPLAYER_INDEX=$playerNumber" (Join-Path $PSScriptRoot 'profile-launcher.c') -o $targetExe -lshell32 -luser32
    if ($LASTEXITCODE -ne 0) { throw "Player $playerNumber build failed: $LASTEXITCODE" }
    Write-Output "built=$targetExe"
}
