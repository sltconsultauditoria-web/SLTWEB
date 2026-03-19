Write-Host "====================================="
Write-Host "SRE ARCHITECTURE SCANNER"
Write-Host "====================================="

Write-Host "`n1️⃣ Detectando tecnologias..."

Get-ChildItem -Recurse -Include package.json,requirements.txt,Dockerfile,docker-compose.yml | ForEach-Object {
    Write-Host "Arquivo encontrado:" $_.FullName
}

Write-Host "`n2️⃣ Detectando API Routes..."

$routes = Select-String -Path backend\*.py -Pattern "@app.route","@router","@app.get","@app.post" -ErrorAction SilentlyContinue

if ($routes) {
    $routes | Select Path,LineNumber,Line
} else {
    Write-Host "Nenhuma rota encontrada automaticamente"
}

Write-Host "`n3️⃣ Detectando Banco de Dados..."

$db = Select-String -Path backend\*.py -Pattern "mongodb","postgres","mysql","sqlite","redis" -ErrorAction SilentlyContinue

if ($db) {
    $db | Select Path,LineNumber,Line
} else {
    Write-Host "Banco nao detectado automaticamente"
}

Write-Host "`n4️⃣ Detectando Kong / Gateway..."

Select-String -Path docker-compose.yml -Pattern "kong","nginx","traefik" -ErrorAction SilentlyContinue

Write-Host "`n5️⃣ Detectando dependencias quebradas..."

Get-ChildItem -Recurse -Include requirements.txt | ForEach-Object {

    Write-Host "Arquivo:" $_.FullName

    Get-Content $_.FullName | ForEach-Object {

        $pkg = $_

        pip show $pkg 2>$null

        if (!$?) {
            Write-Host "Dependencia possivelmente quebrada:" $pkg
        }

    }

}

Write-Host "`n6️⃣ Detectando variaveis de ambiente..."

Get-ChildItem -Recurse -Include ".env","*.env" | ForEach-Object {
    Write-Host "Arquivo ENV encontrado:" $_.FullName
}

Write-Host "`n7️⃣ Detectando serviços Docker..."

Get-Content docker-compose.yml

Write-Host "`nScan finalizado."