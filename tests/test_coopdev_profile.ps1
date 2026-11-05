# Isolated path-resolution checks; no real launcher data is accessed.
$ErrorActionPreference = 'Stop'
$tokens = $null; $errors = $null
$ast = [Management.Automation.Language.Parser]::ParseFile((Join-Path $PSScriptRoot '../tools/coop-dev/coopdev.ps1'), [ref]$tokens, [ref]$errors)
if ($errors.Count) { throw $errors[0] }
$names = 'ProfileDir', 'SettingsFile', 'Settings', 'UserDir', 'DataPkg', 'ClientPkg', 'ActiveSave', 'LatestGameLog'
$ast.FindAll({param($node) $node -is [Management.Automation.Language.FunctionDefinitionAst]}, $true) |
    Where-Object { $_.Name -in $names } | ForEach-Object { Invoke-Expression $_.Extent.Text }
$originalLocal = $env:LOCALAPPDATA; $originalRoaming = $env:APPDATA
$fixture = Join-Path ([IO.Path]::GetTempPath()) ('bbgl-profile-test-' + [guid]::NewGuid())
function AssertEqual($actual, $expected) {
    if ($actual -ne $expected) { throw "Expected $expected, got $actual" }
}
try {
    $env:LOCALAPPDATA = Join-Path $fixture 'Local'
    $env:APPDATA = Join-Path $fixture 'Roaming'
    $Install = Join-Path $fixture 'install'
    $current = Join-Path $env:LOCALAPPDATA 'Bloodborne Game Launcher'
    $legacy = Join-Path $env:LOCALAPPDATA 'bbgl'
    AssertEqual (UserDir) (Join-Path $current 'user')
    New-Item -ItemType Directory -Force $legacy | Out-Null
    @{user_dir=(Join-Path $fixture 'old-save')} | ConvertTo-Json | Set-Content (Join-Path $legacy 'settings.json')
    AssertEqual (SettingsFile) (Join-Path $legacy 'settings.json')
    AssertEqual (DataPkg) (Join-Path $legacy 'coop')
    New-Item -ItemType Directory -Force $current | Out-Null
    AssertEqual (SettingsFile) $null
    AssertEqual (UserDir) (Join-Path $current 'user')
    AssertEqual (DataPkg) (Join-Path $current 'coop')
    $selected = Join-Path $fixture 'selected save'
    @{user_dir=$selected} | ConvertTo-Json | Set-Content (Join-Path $current 'settings.json')
    $save = Join-Path $selected 'savedata/1/CUSA00207/SPRJ0005'
    New-Item -ItemType Directory -Force $save | Out-Null
    AssertEqual (UserDir) $selected
    AssertEqual ((ActiveSave).FullName) ([IO.Path]::GetFullPath($save))
    AssertEqual (SettingsFile) (Join-Path $current 'settings.json')
    AssertEqual (DataPkg) (Join-Path $current 'coop')
    Set-Content (Join-Path $selected 'last_run.log') 'legacy'
    $newLog=Join-Path $selected 'run_20261104_204500.log'
    Set-Content $newLog 'new'
    (Get-Item (Join-Path $selected 'last_run.log')).LastWriteTimeUtc=[DateTime]::UtcNow.AddMinutes(-1)
    AssertEqual ((LatestGameLog).FullName) ([IO.Path]::GetFullPath($newLog))
    'PASS: profile paths, save discovery and latest timestamped run log'
} finally {
    $env:LOCALAPPDATA = $originalLocal; $env:APPDATA = $originalRoaming
}
