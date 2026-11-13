param(
 [Parameter(Mandatory=$true)][string]$Destination,
 [Parameter(Mandatory=$true)][DateTimeOffset]$SinceUtc,
 [string[]]$ProfileRoots=@(),
 [string[]]$GameDirs=@(),
 [string]$Install=''
)
$ErrorActionPreference='Stop'
$ProgressPreference='SilentlyContinue'
$Destination=[IO.Path]::GetFullPath($Destination)
if(Test-Path -LiteralPath $Destination){throw 'DESTINATION_EXISTS: choose a new run directory'}
New-Item -ItemType Directory -Path $Destination | Out-Null
$start=[DateTimeOffset]::UtcNow
$records=New-Object System.Collections.Generic.List[object]
$warnings=New-Object System.Collections.Generic.List[string]
$gameSources=New-Object System.Collections.Generic.List[string]
foreach($g in $GameDirs){if($g){$gameSources.Add($g)}}
if(!$ProfileRoots.Count){
 $ProfileRoots=@(Get-ChildItem -LiteralPath $env:LOCALAPPDATA -Directory |
  Where-Object {$_.Name -eq 'Bloodborne Game Launcher' -or $_.Name -like 'Bloodborne Game Launcher *'} |
  ForEach-Object FullName)
}
function CopyLog([IO.FileInfo]$File,[string]$Group,[string]$Base){
 if($File.LastWriteTimeUtc -lt $SinceUtc.UtcDateTime){return}
 $beforeSize=$File.Length;$beforeTime=$File.LastWriteTimeUtc
 $relative=$File.FullName.Substring($Base.TrimEnd('\','/').Length).TrimStart('\','/')
 $dest=Join-Path (Join-Path $Destination $Group) $relative
 New-Item -ItemType Directory -Path (Split-Path $dest -Parent) -Force | Out-Null
 try {
  Copy-Item -LiteralPath $File.FullName -Destination $dest
  $after=Get-Item -LiteralPath $File.FullName
  $records.Add([PSCustomObject]@{Source=$File.FullName;Copy=$dest.Substring($Destination.Length+1);
   LastWriteUtc=$beforeTime.ToString('o');Length=$beforeSize;
   ChangedDuringCopy=($after.Length -ne $beforeSize -or $after.LastWriteTimeUtc -ne $beforeTime)})
 } catch {$warnings.Add("Copy failed: $($File.FullName): $($_.Exception.Message)")}
}
$index=0
foreach($profile in $ProfileRoots){
 $profile=[IO.Path]::GetFullPath($profile).TrimEnd('\','/');$index++
 $settings=Join-Path $profile 'settings.json'
 if(Test-Path -LiteralPath $settings){
  try {$dir=(Get-Content -LiteralPath $settings -Raw -Encoding UTF8 | ConvertFrom-Json).user_dir
   if($dir -and [IO.Path]::IsPathRooted($dir)){$gameSources.Add($dir)}
  } catch {$warnings.Add("Cannot read user_dir from $settings")}
 }
 $bbsc=Join-Path $profile 'coop/bbsc'
 $logs=Join-Path $bbsc 'logs'
 if(Test-Path -LiteralPath $logs){
  $recent=@(Get-ChildItem -LiteralPath $logs -File -Recurse |
   Where-Object {$_.LastWriteTimeUtc -ge $SinceUtc.UtcDateTime})
  foreach($f in $recent){
   CopyLog $f "profile-$index/mod-logs" $logs
   if($f.Extension -eq '.log'){
    foreach($line in (Select-String -LiteralPath $f.FullName -Pattern 'BB_USER_DIR ')){
     if($line.Line -match 'BB_USER_DIR (.+)\)'){$gameSources.Add($Matches[1])}
    }
   }
  }
 }
 $captures=Join-Path $bbsc 'captures'
 if(Test-Path -LiteralPath $captures){Get-ChildItem -LiteralPath $captures -File -Recurse |
  ForEach-Object {CopyLog $_ "profile-$index/captures" $captures}}
 # Immediate child directories cover a profile-local user_dir even if the
 # current settings point elsewhere or the mod did not log a slot this run.
 if(Test-Path -LiteralPath $profile){
  $gameSources.Add($profile)
  Get-ChildItem -LiteralPath $profile -Directory | ForEach-Object {$gameSources.Add($_.FullName)}
 }
}
$index=0
foreach($dir in ($gameSources | Sort-Object -Unique)){
 if(!(Test-Path -LiteralPath $dir -PathType Container)){continue}
 $index++;$dir=[IO.Path]::GetFullPath($dir).TrimEnd('\','/')
 Get-ChildItem -LiteralPath $dir -File | Where-Object { $_.Name -like 'run_*.log' -or $_.Name -like 'last_run*.log' } |
  ForEach-Object {CopyLog $_ "game-$index" $dir}
 $logDir=Join-Path $dir 'log'
 if(Test-Path -LiteralPath $logDir){Get-ChildItem -LiteralPath $logDir -File -Recurse |
  ForEach-Object {CopyLog $_ "game-$index/log" $logDir}}
}
$hashes=@{}
if($Install){foreach($rel in @('Bloodborne.exe','bin/bb-probe.exe','coop/client/bbsc/bbsc.dll')){
 $p=Join-Path $Install $rel
 if(Test-Path -LiteralPath $p){$hashes[$rel]=(Get-FileHash -LiteralPath $p -Algorithm SHA256).Hash}
}}
if(!$records.Count){$warnings.Add('No logs found in the requested interval; verify sources and SinceUtc')}
$report=[PSCustomObject]@{Machine=$env:COMPUTERNAME;SinceUtc=$SinceUtc.ToUniversalTime().ToString('o');
 StartedUtc=$start.ToString('o');FinishedUtc=[DateTimeOffset]::UtcNow.ToString('o');
 Profiles=$ProfileRoots;InstalledHashes=$hashes;Files=@($records.ToArray());Warnings=@($warnings.ToArray())}
[IO.File]::WriteAllText((Join-Path $Destination 'collection.json'),($report | ConvertTo-Json -Depth 6),[Text.UTF8Encoding]::new($false))
"collected=$Destination files=$($records.Count) warnings=$($warnings.Count)"
