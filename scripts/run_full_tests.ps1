python -m pytest tests -q
if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }
Push-Location frontend
npm.cmd run build
$buildExitCode = $LASTEXITCODE
Pop-Location
exit $buildExitCode
