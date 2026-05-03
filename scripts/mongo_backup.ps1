param(
    [string]$MongoUrl = $env:MONGO_URL,
    [string]$Database = $env:DB_NAME,
    [string]$OutputDir = "backups"
)

if (-not $MongoUrl) {
    $MongoUrl = "mongodb://localhost:27017/consultslt_db"
}

if (-not $Database) {
    $Database = "consultslt_db"
}

$timestamp = Get-Date -Format "yyyyMMdd_HHmmss"
$target = Join-Path $OutputDir "mongo_$Database`_$timestamp"
New-Item -ItemType Directory -Path $target -Force | Out-Null

mongodump --uri $MongoUrl --db $Database --out $target
if ($LASTEXITCODE -ne 0) {
    throw "mongodump falhou com codigo $LASTEXITCODE"
}

Write-Output "Backup MongoDB criado em $target"
