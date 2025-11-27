<#
One-click local test runner for Windows (PowerShell).

This mirrors scripts/test-local.sh behavior for Windows: it will
- tear down any existing compose stack
- clean Python caches
- build images
- bring up services
- execute tests inside the backend container

Run from project root with PowerShell (Developer PowerShell recommended):

.
./scripts/test-local.ps1
#>

[CmdletBinding()]
param(
    [Parameter(Position = 0)]
    [string[]]
    $ExtraArgs
)

function Try-Run($cmd) {
    Write-Host "\n> $cmd" -ForegroundColor Yellow
    $proc = Start-Process -FilePath pwsh -ArgumentList "-NoProfile","-Command",$cmd -Wait -RedirectStandardOutput -NoNewWindow -PassThru -ErrorAction SilentlyContinue
    if ($proc -and $proc.ExitCode -ne 0) {
        throw "Command failed with exit code $($proc.ExitCode): $cmd"
    }
    return $proc
}

Write-Host "=== One-click test run (Windows) ===" -ForegroundColor Green

# Ensure we run from repository root where this script lives
$scriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
Push-Location $scriptDir\..\

try {
    Write-Host "Stopping and removing previous compose stack (if any)..." -ForegroundColor Cyan
    docker-compose down -v --remove-orphans

    Write-Host "Cleaning __pycache__ directories (if any)..." -ForegroundColor Cyan
    # Remove __pycache__ recursively (silently ignore if not present)
    Get-ChildItem -Path . -Filter '__pycache__' -Recurse -Directory -ErrorAction SilentlyContinue | ForEach-Object { Remove-Item $_.FullName -Recurse -Force -ErrorAction SilentlyContinue }

    Write-Host "Building images..." -ForegroundColor Cyan
    docker-compose build

    Write-Host "Starting compose services..." -ForegroundColor Cyan
    docker-compose up -d

    Write-Host "Running backend tests inside backend container..." -ForegroundColor Cyan
    # Execute the same test harness as scripts/test-local.sh: run tests-start.sh inside backend
    docker-compose exec -T backend bash scripts/tests-start.sh $ExtraArgs

    Write-Host "\nAll tests finished. If running in CI, check container logs above." -ForegroundColor Green
}
catch {
    Write-Host "Error: $_" -ForegroundColor Red
    exit 1
}
finally {
    Pop-Location
}
