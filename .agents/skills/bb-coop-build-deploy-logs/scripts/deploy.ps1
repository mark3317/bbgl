param([Parameter(Mandatory=$true)][string]$Source,[Parameter(Mandatory=$true)][string]$Install,[Parameter(Mandatory=$true)][string]$Root,[ValidatePattern('^[a-zA-Z0-9_-]+$')][string]$Label='build',[switch]$CheckOnly,[Alias('Files')][string[]]$IncludeFiles)
$ErrorActionPreference='Stop'
$ProgressPreference='SilentlyContinue'
$Source=[IO.Path]::GetFullPath($Source).TrimEnd('\','/')
$Install=[IO.Path]::GetFullPath($Install).TrimEnd('\','/')
$Root=[IO.Path]::GetFullPath($Root).TrimEnd('\','/')
$stamp=Get-Date -Format yyyyMMdd-HHmmss
function AssertStopped {
 if(Get-Process -Name 'bb-probe','bb-play','bbsc-launch','Bloodborne','Play Bloodborne' -ErrorAction SilentlyContinue){throw 'GAME_OR_LAUNCHER_RUNNING'}
}
AssertStopped
if($Source -eq $Install){throw 'SOURCE_IS_INSTALL'}
if(!(Test-Path -LiteralPath $Install -PathType Container)){throw 'INSTALL_MISSING'}
if($Source.EndsWith('.zip')) {
 $unpack=Join-Path $Root "coop-dev\stage-$Label-$stamp"
 Expand-Archive -LiteralPath $Source -DestinationPath $unpack
 $Source=Join-Path $unpack 'Bloodborne Game Launcher'
}
if(!$IncludeFiles -and !(Test-Path -LiteralPath (Join-Path $Source 'Bloodborne.exe'))){throw 'SOURCE_MISSING'}
$meta=Get-Content -LiteralPath (Join-Path $Source 'coop\SOURCE.json') -Raw -Encoding UTF8 | ConvertFrom-Json
"source_commit=$($meta.bbsc_commit)"
$backup=Join-Path $Root "coop-dev\backups\$Label-$stamp"
$skip=@('game','user','out','mods','bbport.ini','input.ini','mods.json','patches.json','last_run.log','coop-server.json','settings.json')
# Explicit delta avoids even enumerating the complete package. Otherwise use size/mtime.
$candidates=if($IncludeFiles){foreach($rel in $IncludeFiles){
 $candidate=[IO.Path]::GetFullPath((Join-Path $Source $rel))
 if(!$candidate.StartsWith($Source+'\', [StringComparison]::OrdinalIgnoreCase)){throw 'DELTA_PATH_OUTSIDE_SOURCE'}
 Get-Item -LiteralPath $candidate
}}else{Get-ChildItem -LiteralPath $Source -Recurse -File}
$files=@($candidates | ForEach-Object {
 $rel=$_.FullName.Substring($Source.Length+1)
 if(($rel -split '[\\/]')[0] -notin $skip){[PSCustomObject]@{Rel=$rel;Path=$_.FullName;Size=$_.Length;Time=$_.LastWriteTimeUtc}}
})
$changes=if($IncludeFiles){$files}else{@($files | Where-Object {
 $dst=Get-Item -LiteralPath (Join-Path $Install $_.Rel) -ErrorAction SilentlyContinue
 !$dst -or $dst.Length -ne $_.Size -or [Math]::Abs(($dst.LastWriteTimeUtc-$_.Time).TotalSeconds) -gt 2
})}
if($CheckOnly){"CHECK_ONLY selected=$($changes.Count)";return}
# Back up all replaced files before the first mutation of the installation.
foreach($f in $changes){
 $dst=Join-Path $Install $f.Rel
 if(Test-Path -LiteralPath $dst){$bak=Join-Path $backup $f.Rel; New-Item -ItemType Directory -Path (Split-Path $bak -Parent) -Force | Out-Null; Copy-Item -LiteralPath $dst -Destination $bak}
}
AssertStopped
foreach($f in $changes){$dst=Join-Path $Install $f.Rel;New-Item -ItemType Directory -Path (Split-Path $dst -Parent) -Force | Out-Null;Copy-Item -LiteralPath $f.Path -Destination $dst -Force}
# An old explicit override, if present, must not mask the new client DLL.
$override=Join-Path $Install 'coop\bbsc'
if(Test-Path -LiteralPath (Join-Path $override 'bbsc.dll')){
 foreach($name in 'bbsc.dll','bbsc-launch.exe','mod.json'){
  $dst=Join-Path $override $name;$src=Join-Path $Source "coop\client\bbsc\$name"
  if(Test-Path -LiteralPath $dst){$bak=Join-Path $backup "override\$name";New-Item -ItemType Directory -Path (Split-Path $bak -Parent) -Force | Out-Null;Copy-Item -LiteralPath $dst -Destination $bak}
  Copy-Item -LiteralPath $src -Destination $dst -Force
 }
}
"backup=$backup"
"copied=$(@($changes).Count) file_verification=disabled"
