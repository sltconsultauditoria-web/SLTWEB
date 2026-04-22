Write-Host "============================="
Write-Host "ANALISE DE INGRESS / KONG"
Write-Host "============================="

Write-Host "`nProcurando referencias a Kong..."

$results = Select-String -Path .\* -Pattern "kong" -Recurse -ErrorAction SilentlyContinue

if ($results) {
    Write-Host "Kong encontrado nos arquivos:"
    $results | Select Path, LineNumber, Line
} else {
    Write-Host "Nenhuma referencia a Kong encontrada"
}

Write-Host "`nProcurando arquivos de ingress..."

Get-ChildItem -Recurse -Include "*ingress*.yml","*ingress*.yaml" | ForEach-Object {
    Write-Host "Arquivo encontrado:" $_.FullName
}

Write-Host "`nProcurando docker containers Kong..."

Get-ChildItem -Recurse -Include "docker-compose.yml" | ForEach-Object {

    $content = Get-Content $_.FullName

    if ($content -match "kong") {
        Write-Host "Kong encontrado em:" $_.FullName
    }

}

Write-Host "`nAnalise concluida."