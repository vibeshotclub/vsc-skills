param(
  [string]$TopviewSkill = "",
  [switch]$ShowInstallHints
)

$ErrorActionPreference = "SilentlyContinue"

function Test-CommandName {
  param(
    [string]$Name,
    [bool]$Required = $false,
    [string]$InstallHint = ""
  )
  $cmd = Get-Command $Name -ErrorAction SilentlyContinue
  if ($cmd) {
    [PSCustomObject]@{ Tool = $Name; Required = $Required; Found = $true; Path = $cmd.Source; InstallHint = "" }
  } else {
    [PSCustomObject]@{ Tool = $Name; Required = $Required; Found = $false; Path = ""; InstallHint = $InstallHint }
  }
}

function Get-PythonCommand {
  $py = Get-Command "py" -ErrorAction SilentlyContinue
  if ($py) { return @("py", "-3") }
  $python = Get-Command "python" -ErrorAction SilentlyContinue
  if ($python) { return @("python") }
  return @()
}

function Test-PythonModule {
  param(
    [string]$ModuleName,
    [bool]$Required = $false,
    [string]$InstallHint = ""
  )
  $pythonCmd = Get-PythonCommand
  if ($pythonCmd.Count -eq 0) {
    return [PSCustomObject]@{ Tool = "python-module:$ModuleName"; Required = $Required; Found = $false; Path = ""; InstallHint = "Install Python first, then run: $InstallHint" }
  }
  $exe = $pythonCmd[0]
  $args = @()
  if ($pythonCmd.Count -gt 1) { $args += $pythonCmd[1..($pythonCmd.Count - 1)] }
  $args += @("-c", "import $ModuleName")
  & $exe @args | Out-Null
  $ok = $LASTEXITCODE -eq 0
  [PSCustomObject]@{
    Tool = "python-module:$ModuleName"
    Required = $Required
    Found = $ok
    Path = if ($ok) { $exe } else { "" }
    InstallHint = if ($ok) { "" } else { $InstallHint }
  }
}

$commonTopviewSkills = @(
  $TopviewSkill,
  "$env:USERPROFILE\.agents\skills\topview",
  "$env:USERPROFILE\.codex\skills\topview"
) | Where-Object { $_ }

$topviewPath = ""
foreach ($candidate in $commonTopviewSkills) {
  if (Test-Path -LiteralPath $candidate) {
    $topviewPath = $candidate
    break
  }
}

$results = @()
$results += Test-CommandName "python" $true "Install Python 3.10+ from python.org or Microsoft Store."
$results += Test-CommandName "py" $false "Install Python Launcher or use python directly."
$results += Test-PythonModule "PIL" $true "py -m pip install Pillow"
$results += Test-CommandName "ffmpeg" $true "winget install --id Gyan.FFmpeg -e"
$results += Test-CommandName "ffprobe" $true "winget install --id Gyan.FFmpeg -e"
$results += Test-CommandName "node" $true "Install Node.js LTS from nodejs.org or use winget install OpenJS.NodeJS.LTS."
$results += Test-CommandName "npm" $true "Install Node.js LTS from nodejs.org or use winget install OpenJS.NodeJS.LTS."
$results += Test-CommandName "npx" $true "Install Node.js LTS from nodejs.org or use winget install OpenJS.NodeJS.LTS."
$results += Test-CommandName "remotion" $false "Optional global CLI. If missing, use npx remotion inside a Remotion project."

$remotionSkillCandidates = @(
  "$env:USERPROFILE\.codex\plugins\cache\openai-curated\remotion",
  "$env:USERPROFILE\.codex\skills\remotion-best-practices",
  "$env:USERPROFILE\.agents\skills\remotion-best-practices"
)
$remotionSkillPath = ""
foreach ($candidate in $remotionSkillCandidates) {
  if (Test-Path -LiteralPath $candidate) {
    $remotionSkillPath = $candidate
    break
  }
}
$results += [PSCustomObject]@{
  Tool = "remotion-plugin"
  Required = $true
  Found = [bool]$remotionSkillPath
  Path = $remotionSkillPath
  InstallHint = "Install or enable the Remotion plugin/skill before using Remotion assembly."
}
$results += [PSCustomObject]@{
  Tool = "topview-skill"
  Required = $false
  Found = [bool]$topviewPath
  Path = $topviewPath
  InstallHint = "Optional. Install/connect Topview only if this user wants automated Topview generation."
}

$results | Format-Table -AutoSize

if ($ShowInstallHints) {
  $missingRequired = $results | Where-Object { $_.Required -and -not $_.Found }
  if ($missingRequired) {
    Write-Host ""
    Write-Host "Missing required dependencies. Ask the user before installing:"
    $missingRequired | ForEach-Object { Write-Host ("- {0}: {1}" -f $_.Tool, $_.InstallHint) }
  }
}
