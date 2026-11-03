param(
    [Parameter(Mandatory=$true)][string]$SourceInstall,
    [Parameter(Mandatory=$true)][string]$Install,
    [Parameter(Mandatory=$true)][string]$Profile,
    [Parameter(Mandatory=$true)][string]$Payload,
    [Parameter(Mandatory=$true)][string]$Invitation,
    [Parameter(Mandatory=$true)][string]$Member,
    [Parameter(Mandatory=$true)][string]$Game,
    [Parameter(Mandatory=$true)][string]$Snapshot
)
$ErrorActionPreference='Stop'
$target=[IO.Path]::GetFullPath($Install)
$source=[IO.Path]::GetFullPath($SourceInstall)
if ($target -eq $source -or (Test-Path -LiteralPath $target)) { throw 'Use a new, separate experimental installation.' }
if (Test-Path -LiteralPath $Profile) { throw 'Use a new experimental profile; existing data is preserved.' }
if (!(Test-Path -LiteralPath (Join-Path $Game 'eboot.bin'))) { throw 'Game path is not valid.' }
if (!(Test-Path -LiteralPath (Join-Path $Snapshot 'SPRJ0005'))) { throw 'Named test snapshot required.' }
New-Item -ItemType Directory -Path $target | Out-Null
& robocopy $source $target /E /XJ /XD game out user server /XF "Bloodborne Player *.exe" /NFL /NDL /NJH /NJS /NP | Out-Null
if ($LASTEXITCODE -ge 8) { throw "Clone failed: $LASTEXITCODE" }
# Only these copied client files are changed. Main installation and live profiles are untouched.
& robocopy $Payload $target /E /XJ /NFL /NDL /NJH /NJS /NP | Out-Null
if ($LASTEXITCODE -ge 8) { throw "Payload copy failed: $LASTEXITCODE" }
New-Item -ItemType Directory -Force -Path (Join-Path $Profile 'party'),(Join-Path $Profile 'user/savedata/1/CUSA00207'),(Join-Path $Profile 'seed') | Out-Null
Copy-Item -LiteralPath (Join-Path $Snapshot 'SPRJ0005') -Destination (Join-Path $Profile 'user/savedata/1/CUSA00207/SPRJ0005') -Recurse
Copy-Item -LiteralPath (Join-Path $Snapshot 'SPRJ0005') -Destination (Join-Path $Profile 'seed/SPRJ0005') -Recurse
if (Test-Path -LiteralPath (Join-Path $Snapshot 'SPRJ0005.sce_sys')) {
    Copy-Item -LiteralPath (Join-Path $Snapshot 'SPRJ0005.sce_sys') -Destination (Join-Path $Profile 'user/savedata/1/CUSA00207/SPRJ0005.sce_sys') -Recurse
}
Copy-Item -LiteralPath $Invitation -Destination (Join-Path $Profile 'party/invitation.json')
$cmdText="@echo off`r`nset `"BBGL_PROFILE_DIR=$Profile`"`r`nset `"BB_PARTY_CONFIG=$Profile\party\invitation.json`"`r`nset `"BB_PARTY_MEMBER=$Member`"`r`nset `"BB_PARTY_GAME=$Game`"`r`ncd /d `"%~dp0`"`r`n`"%~dp0Bloodborne.exe`" --script `"%~dp0coop\party\launch.py`"`r`n"
[IO.File]::WriteAllText((Join-Path $target 'Play Party.cmd'),$cmdText,[Text.Encoding]::ASCII)
$legacyText="@echo off`r`nset `"BBGL_PROFILE_DIR=$Profile`"`r`nset `"BB_PARTY_CONFIG=`"`r`nset `"BB_PARTY_MEMBER=`"`r`ncd /d `"%~dp0`"`r`n`"%~dp0Bloodborne.exe`"`r`n"
[IO.File]::WriteAllText((Join-Path $target 'Play Legacy.cmd'),$legacyText,[Text.Encoding]::ASCII)
$settings=@{game_dir=$Game;user_dir=(Join-Path $Profile 'user');player_name=$Member;mods_enabled=$true;play_mode='offline';auto_update=$false}
[IO.File]::WriteAllText((Join-Path $Profile 'settings.json'),($settings|ConvertTo-Json -Depth 4),[Text.UTF8Encoding]::new($false))
Write-Output "Experimental client prepared: $target; profile: $Profile; member: $Member"
exit 0
