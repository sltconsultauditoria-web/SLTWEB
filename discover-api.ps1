Write-Host ""
Write-Host "API DISCOVERY"
Write-Host "====================="

$urls = @(
"http://localhost:8000",
"http://localhost:8000/docs",
"http://localhost:8000/api",
"http://localhost:8000/health",
"http://localhost:8001",
"http://localhost:8001/api",
"http://localhost:8001/docs"
)

foreach ($url in $urls) {

    try {

        $r = Invoke-WebRequest $url -UseBasicParsing -TimeoutSec 3

        Write-Host "[OK] $url -> $($r.StatusCode)"

    }
    catch {

        Write-Host "[FAIL] $url"

    }

}