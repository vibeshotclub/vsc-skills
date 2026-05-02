param(
  [string]$TopviewSkill = ""
)

$ErrorActionPreference = "SilentlyContinue"

function Test-EnvName {
  param([string[]]$Names)
  foreach ($name in $Names) {
    $value = [Environment]::GetEnvironmentVariable($name, "Process")
    if (-not $value) { $value = [Environment]::GetEnvironmentVariable($name, "User") }
    if (-not $value) { $value = [Environment]::GetEnvironmentVariable($name, "Machine") }
    if ($value) { return $name }
  }
  return ""
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

$providers = @(
  [PSCustomObject]@{
    Provider = "Topview"
    Connected = [bool]$topviewPath
    Evidence = if ($topviewPath) { $topviewPath } else { "" }
    Notes = "Use automated Omni Reference when the Topview skill is installed and authenticated."
  },
  [PSCustomObject]@{
    Provider = "Seedance API"
    Connected = [bool](Test-EnvName @("SEEDANCE_API_KEY", "ARK_API_KEY", "VOLCENGINE_ACCESS_KEY_ID"))
    Evidence = Test-EnvName @("SEEDANCE_API_KEY", "ARK_API_KEY", "VOLCENGINE_ACCESS_KEY_ID")
    Notes = "If connected, adapt the exported video prompt and pass the 2x2 sheet plus character cards as references."
  },
  [PSCustomObject]@{
    Provider = "Krea"
    Connected = [bool](Test-EnvName @("KREA_API_KEY"))
    Evidence = Test-EnvName @("KREA_API_KEY")
    Notes = "If not connected, use Krea manually with the exported references and prompt."
  },
  [PSCustomObject]@{
    Provider = "Lovart"
    Connected = [bool](Test-EnvName @("LOVART_API_KEY"))
    Evidence = Test-EnvName @("LOVART_API_KEY")
    Notes = "If not connected, use Lovart manually with the exported references and prompt."
  },
  [PSCustomObject]@{
    Provider = "LibTV"
    Connected = [bool](Test-EnvName @("LIBTV_API_KEY", "LIBTV_TOKEN"))
    Evidence = Test-EnvName @("LIBTV_API_KEY", "LIBTV_TOKEN")
    Notes = "If not connected, use LibTV manually with the exported references and prompt."
  }
)

$providers | Format-Table -AutoSize

if (-not ($providers | Where-Object { $_.Connected })) {
  Write-Host ""
  Write-Host "No connected video generation provider was detected. Ask the user which platform they want to use, then provide manual upload instructions using:"
  Write-Host "- images/memory_sheet_01.png ... memory_sheet_04.png"
  Write-Host "- images/character_male.png"
  Write-Host "- images/character_female.png"
  Write-Host "- prompts/video_clip_01.txt ... video_clip_04.txt"
}
