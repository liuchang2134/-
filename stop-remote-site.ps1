$ErrorActionPreference = "Stop"

$logDir = Join-Path (Join-Path $env:LOCALAPPDATA "CodexTools") "al-brooks-remote"
$stateFile = Join-Path $logDir "remote-site-state.json"

if (-not (Test-Path $stateFile)) {
  Write-Host "No remote site state file found."
  exit 0
}

$state = Get-Content -Raw -LiteralPath $stateFile | ConvertFrom-Json
$pids = @($state.serverPid, $state.tunnelPid) | Where-Object { $_ }

foreach ($pid in $pids) {
  $process = Get-Process -Id $pid -ErrorAction SilentlyContinue
  if ($process) {
    Stop-Process -Id $pid -Force
    Write-Host "Stopped process $pid ($($process.ProcessName))."
  }
}

Remove-Item -LiteralPath $stateFile -Force
Write-Host "Remote site stopped."
