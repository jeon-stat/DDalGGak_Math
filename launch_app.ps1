$ErrorActionPreference = "Stop"

$projectDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$port = 8501
$url = "http://127.0.0.1:$port"
$python = Join-Path $projectDir ".venv\Scripts\python.exe"

Set-Location $projectDir

$listener = Get-NetTCPConnection -LocalPort $port -State Listen -ErrorAction SilentlyContinue
if (-not $listener) {
    Start-Process -FilePath $python -ArgumentList @(
        "-m", "streamlit", "run", "app.py",
        "--server.port", "$port",
        "--server.headless", "true",
        "--browser.gatherUsageStats", "false"
    ) -WorkingDirectory $projectDir -WindowStyle Minimized
    Start-Sleep -Seconds 4
}

Start-Process $url
