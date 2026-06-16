$ErrorActionPreference = "Stop"

$projectRoot = $PSScriptRoot
$toolDir = Join-Path $env:LOCALAPPDATA "CodexTools"
$logDir = Join-Path $toolDir "al-brooks-remote"
$cloudflared = Join-Path $toolDir "cloudflared.exe"
$stateFile = Join-Path $logDir "remote-site-state.json"

New-Item -ItemType Directory -Force -Path $toolDir | Out-Null
New-Item -ItemType Directory -Force -Path $logDir | Out-Null

if (-not (Test-Path $cloudflared)) {
  Write-Host "Downloading cloudflared..."
  Invoke-WebRequest `
    -Uri "https://github.com/cloudflare/cloudflared/releases/latest/download/cloudflared-windows-amd64.exe" `
    -OutFile $cloudflared `
    -UseBasicParsing `
    -TimeoutSec 180
}

$pythonCandidates = @(
  (Join-Path $env:USERPROFILE ".cache\codex-runtimes\codex-primary-runtime\dependencies\python\python.exe"),
  "python",
  "py"
)

$python = $null
foreach ($candidate in $pythonCandidates) {
  try {
    if ((Test-Path $candidate) -or (Get-Command $candidate -ErrorAction SilentlyContinue)) {
      $python = $candidate
      break
    }
  } catch {}
}

if (-not $python) {
  throw "Python was not found. Install Python or run this from Codex after the bundled runtime is available."
}

$port = 8777
while (Get-NetTCPConnection -LocalPort $port -ErrorAction SilentlyContinue) {
  $port++
}

$serverOut = Join-Path $logDir "server-$port.out.log"
$serverErr = Join-Path $logDir "server-$port.err.log"
$tunnelLog = Join-Path $logDir "cloudflared-$port.log"
if (Test-Path $tunnelLog) {
  Remove-Item -LiteralPath $tunnelLog -Force
}

$server = Start-Process `
  -FilePath $python `
  -ArgumentList @("-m", "http.server", "$port", "--bind", "127.0.0.1") `
  -WorkingDirectory $projectRoot `
  -WindowStyle Hidden `
  -RedirectStandardOutput $serverOut `
  -RedirectStandardError $serverErr `
  -PassThru

Start-Sleep -Seconds 2
Invoke-WebRequest -Uri "http://127.0.0.1:$port/" -UseBasicParsing -TimeoutSec 10 | Out-Null

$tunnel = Start-Process `
  -FilePath $cloudflared `
  -ArgumentList @("tunnel", "--no-autoupdate", "--url", "http://127.0.0.1:$port", "--logfile", $tunnelLog, "--loglevel", "info") `
  -WindowStyle Hidden `
  -PassThru

$publicUrl = $null
for ($i = 0; $i -lt 60; $i++) {
  Start-Sleep -Milliseconds 750
  if (Test-Path $tunnelLog) {
    $content = Get-Content -Raw -LiteralPath $tunnelLog -ErrorAction SilentlyContinue
    $match = [regex]::Match($content, "https://[-a-z0-9]+\.trycloudflare\.com")
    if ($match.Success) {
      $publicUrl = $match.Value
      break
    }
  }
  if ($tunnel.HasExited) {
    break
  }
}

if (-not $publicUrl) {
  throw "Cloudflare tunnel did not return a public URL. Check log: $tunnelLog"
}

[pscustomobject]@{
  publicUrl = $publicUrl
  localUrl = "http://127.0.0.1:$port/"
  port = $port
  serverPid = $server.Id
  tunnelPid = $tunnel.Id
  startedAt = (Get-Date).ToString("s")
  tunnelLog = $tunnelLog
} | ConvertTo-Json -Depth 5 | Set-Content -LiteralPath $stateFile -Encoding UTF8

Write-Host ""
Write-Host "Remote website is running:"
Write-Host $publicUrl
Write-Host ""
Write-Host "Local URL:"
Write-Host "http://127.0.0.1:$port/"
Write-Host ""
Write-Host "Keep this computer awake. Run stop-remote-site.ps1 to stop it."
