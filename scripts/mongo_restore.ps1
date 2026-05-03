param(
    [Parameter(Mandatory = $true)]
    [string]$BackupPath,
    [string]$MongoUrl = $env:MONGO_URL,
    [string]$Database = $env:DB_NAME
)

if (-not $MongoUrl) {
    $MongoUrl = "mongodb://localhost:27017/consultslt_db"
}

if (-not $Database) {
    $Database = "consultslt_db"
}

$source = Join-Path $BackupPath $Database
if (-not (Test-Path $source)) {
    throw "Diretorio de backup nao encontrado: $source"
}

mongorestore --uri $MongoUrl --db $Database --drop $source
if ($LASTEXITCODE -ne 0) {
    throw "mongorestore falhou com codigo $LASTEXITCODE"
}

Write-Output "Restore MongoDB concluido para $Database"
