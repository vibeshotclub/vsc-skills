param(
  [Parameter(Mandatory = $true)]
  [string[]]$ClipPaths,

  [string]$MusicPath = "",

  [Parameter(Mandatory = $true)]
  [string]$OutputPath,

  [string]$WorkDir = ""
)

$ErrorActionPreference = "Stop"

if (-not (Get-Command ffmpeg -ErrorAction SilentlyContinue)) {
  throw "FFmpeg was not found. Install FFmpeg or assemble manually in a video editor."
}

foreach ($clip in $ClipPaths) {
  if (-not (Test-Path -LiteralPath $clip)) {
    throw "Clip not found: $clip"
  }
}

if ($MusicPath -and -not (Test-Path -LiteralPath $MusicPath)) {
  throw "Music file not found: $MusicPath"
}

$outputDirectory = Split-Path -Parent $OutputPath
if ($outputDirectory -and -not (Test-Path -LiteralPath $outputDirectory)) {
  New-Item -ItemType Directory -Path $outputDirectory | Out-Null
}

if (Test-Path -LiteralPath $OutputPath) {
  $stamp = Get-Date -Format "yyyyMMdd-HHmmss"
  $base = [System.IO.Path]::GetFileNameWithoutExtension($OutputPath)
  $ext = [System.IO.Path]::GetExtension($OutputPath)
  $OutputPath = Join-Path $outputDirectory ("{0}_{1}{2}" -f $base, $stamp, $ext)
}

function Invoke-Ffmpeg {
  param([string[]]$Arguments)
  & ffmpeg @Arguments
  return $LASTEXITCODE
}

if (-not $WorkDir) {
  $WorkDir = $outputDirectory
}
if (-not (Test-Path -LiteralPath $WorkDir)) {
  New-Item -ItemType Directory -Path $WorkDir | Out-Null
}

$stamp = Get-Date -Format "yyyyMMdd-HHmmss"
$concatList = Join-Path $WorkDir ("concat_list_{0}.txt" -f $stamp)
$joinedVideo = Join-Path $WorkDir ("joined_silent_{0}.mp4" -f $stamp)

$lines = foreach ($clip in $ClipPaths) {
  $full = (Resolve-Path -LiteralPath $clip).Path.Replace("'", "''")
  "file '$full'"
}
$utf8NoBom = [System.Text.UTF8Encoding]::new($false)
[System.IO.File]::WriteAllLines($concatList, $lines, $utf8NoBom)

$copyArgs = @("-hide_banner", "-n", "-f", "concat", "-safe", "0", "-i", $concatList, "-c", "copy", $joinedVideo)
$copyExit = Invoke-Ffmpeg $copyArgs
if ($copyExit -ne 0 -or -not (Test-Path -LiteralPath $joinedVideo)) {
  $encodeArgs = @("-hide_banner", "-n", "-f", "concat", "-safe", "0", "-i", $concatList, "-c:v", "libx264", "-pix_fmt", "yuv420p", "-c:a", "aac", "-movflags", "+faststart", $joinedVideo)
  $encodeExit = Invoke-Ffmpeg $encodeArgs
  if ($encodeExit -ne 0) {
    throw "FFmpeg could not concatenate the clips."
  }
}

if ($MusicPath) {
  $musicArgs = @("-hide_banner", "-n", "-i", $joinedVideo, "-i", $MusicPath, "-map", "0:v:0", "-map", "1:a:0", "-c:v", "copy", "-c:a", "aac", "-shortest", "-movflags", "+faststart", $OutputPath)
  $musicExit = Invoke-Ffmpeg $musicArgs
  if ($musicExit -ne 0) {
    throw "FFmpeg could not add the music track."
  }
} else {
  $finalArgs = @("-hide_banner", "-n", "-i", $joinedVideo, "-c", "copy", $OutputPath)
  $finalExit = Invoke-Ffmpeg $finalArgs
  if ($finalExit -ne 0) {
    throw "FFmpeg could not write the final video."
  }
}

Write-Output $OutputPath
