param(
  [Parameter(Mandatory = $true)]
  [string]$InputImage,

  [Parameter(Mandatory = $true)]
  [string]$OutputDir,

  [string]$Prefix = "memory_sheet"
)

$ErrorActionPreference = "Stop"

if (-not (Test-Path -LiteralPath $InputImage)) {
  throw "Input image not found: $InputImage"
}

if (-not (Test-Path -LiteralPath $OutputDir)) {
  New-Item -ItemType Directory -Path $OutputDir | Out-Null
}

Add-Type -AssemblyName System.Drawing

$resolvedInput = (Resolve-Path -LiteralPath $InputImage).Path
$source = [System.Drawing.Bitmap]::new($resolvedInput)
try {
  $cellWidth = [Math]::Floor($source.Width / 4)
  $cellHeight = [Math]::Floor($source.Height / 4)
  $sheetWidth = $cellWidth * 2
  $sheetHeight = $cellHeight * 2

  $index = 1
  foreach ($rowBlock in 0, 1) {
    foreach ($colBlock in 0, 1) {
      $left = $colBlock * $sheetWidth
      $top = $rowBlock * $sheetHeight
      $dest = [System.Drawing.Bitmap]::new($sheetWidth, $sheetHeight)
      try {
        $graphics = [System.Drawing.Graphics]::FromImage($dest)
        try {
          $graphics.InterpolationMode = [System.Drawing.Drawing2D.InterpolationMode]::HighQualityBicubic
          $graphics.PixelOffsetMode = [System.Drawing.Drawing2D.PixelOffsetMode]::HighQuality
          $graphics.DrawImage(
            $source,
            [System.Drawing.Rectangle]::new(0, 0, $sheetWidth, $sheetHeight),
            [System.Drawing.Rectangle]::new($left, $top, $sheetWidth, $sheetHeight),
            [System.Drawing.GraphicsUnit]::Pixel
          )
        } finally {
          $graphics.Dispose()
        }

        $outPath = Join-Path $OutputDir ("{0}_{1:00}.png" -f $Prefix, $index)
        if (Test-Path -LiteralPath $outPath) {
          $stamp = Get-Date -Format "yyyyMMdd-HHmmss"
          $outPath = Join-Path $OutputDir ("{0}_{1:00}_{2}.png" -f $Prefix, $index, $stamp)
        }
        $dest.Save($outPath, [System.Drawing.Imaging.ImageFormat]::Png)
        Write-Output $outPath
      } finally {
        $dest.Dispose()
      }
      $index++
    }
  }
} finally {
  $source.Dispose()
}
