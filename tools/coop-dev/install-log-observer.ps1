param([string]$Install = 'D:\Games\Bloodborne\Bloodborne Game Launcher', [switch]$Disable)
$ErrorActionPreference = 'Stop'
$repoDir = [IO.Path]::GetFullPath((Join-Path $PSScriptRoot '..\..'))
$installDir = (Resolve-Path -LiteralPath $Install).Path
$configPath = Join-Path $installDir 'tools\log-observer.json'
if ($Disable) {
    if (Test-Path -LiteralPath $configPath) {
        $value = Get-Content -LiteralPath $configPath -Raw | ConvertFrom-Json
        $value.enabled = $false
        [IO.File]::WriteAllText($configPath, ($value | ConvertTo-Json), [Text.UTF8Encoding]::new($false))
    }
    Write-Output 'Observer autostart disabled. Existing collector drains when profiles close.'
    exit 0
}
$running = @(Get-Process -Name Bloodborne,bb-probe,bb-play,bbsc-launch -ErrorAction SilentlyContinue)
if ($running.Count) { throw 'Close the games and launcher before installing the observer hook. No process was stopped.' }
$pythonwPath = Join-Path $repoDir 'out\qt-venv\Scripts\pythonw.exe'
if (!(Test-Path -LiteralPath $pythonwPath)) { throw 'Development pythonw.exe is missing.' }
if (!(Test-Path -LiteralPath (Join-Path $installDir 'Bloodborne.exe'))) { throw 'Bloodborne.exe is missing.' }
$backupDir = Join-Path $repoDir ('out\log-observer\install-backup-' + (Get-Date -Format 'yyyyMMdd-HHmmss'))
New-Item -ItemType Directory -Path $backupDir -Force | Out-Null
foreach ($relative in @('scripts\local_party.py', 'scripts\start_log_observer.py', 'tools\log-observer.json')) {
    $target = Join-Path $installDir $relative
    if (Test-Path -LiteralPath $target) {
        $backup = Join-Path $backupDir $relative
        New-Item -ItemType Directory -Path (Split-Path $backup -Parent) -Force | Out-Null
        Copy-Item -LiteralPath $target -Destination $backup
    }
}
foreach ($relative in @('scripts\local_party.py', 'scripts\start_log_observer.py')) {
    Copy-Item -LiteralPath (Join-Path $repoDir $relative) -Destination (Join-Path $installDir $relative)
}
New-Item -ItemType Directory -Path (Split-Path $configPath -Parent) -Force | Out-Null
$configuration = @{enabled=$true; pythonw=$pythonwPath; script=(Join-Path $PSScriptRoot 'log_observer.py'); projectId='b25db2d0-df72-4c85-acba-249ef647359a'}
[IO.File]::WriteAllText($configPath, ($configuration | ConvertTo-Json), [Text.UTF8Encoding]::new($false))
Write-Output "Installed observer hook. Backup: $backupDir"
