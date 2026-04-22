Write-Host ""
Write-Host "==========================================="
Write-Host "ANALISE AVANCADA DE DEPENDENCIAS FRONTEND"
Write-Host "==========================================="
Write-Host ""

Write-Host "1️⃣ Versoes do ambiente"
node -v
npm -v

Write-Host ""
Write-Host "2️⃣ Verificando dependencias duplicadas"

npm ls tailwindcss
npm ls react
npm ls react-dom

Write-Host ""
Write-Host "3️⃣ Verificando dependencias quebradas"

npm ls --depth=0

Write-Host ""
Write-Host "4️⃣ Verificando inconsistencias"

if (Test-Path "package-lock.json") {
    Write-Host "package-lock.json encontrado"
} else {
    Write-Host "⚠ package-lock.json nao encontrado"
}

Write-Host ""
Write-Host "5️⃣ Verificando pacotes instalados manualmente"

$pkg = Get-Content package.json | ConvertFrom-Json

$dependencies = $pkg.dependencies
$devDependencies = $pkg.devDependencies

Write-Host ""
Write-Host "Dependencias principais:"
$dependencies.PSObject.Properties | ForEach-Object {
    Write-Host $_.Name ":" $_.Value
}

Write-Host ""
Write-Host "DevDependencias:"
$devDependencies.PSObject.Properties | ForEach-Object {
    Write-Host $_.Name ":" $_.Value
}

Write-Host ""
Write-Host "6️⃣ Detectando conflitos comuns"

$tailwind = npm ls tailwindcss | Out-String

if ($tailwind -match "deduped") {
    Write-Host "⚠ Possivel conflito de Tailwind detectado"
}

if ($tailwind -match "tailwindcss@4") {
    Write-Host "⚠ Tailwind v4 detectado (pode quebrar React Scripts)"
}

if ($tailwind -match "tailwindcss@3") {
    Write-Host "Tailwind v3 detectado"
}

Write-Host ""
Write-Host "7️⃣ Verificando arquivos de configuracao"

$files = @(
"craco.config.js",
"postcss.config.js",
"tailwind.config.js"
)

foreach ($file in $files) {

    if (Test-Path $file) {
        Write-Host "OK:" $file
    }
    else {
        Write-Host "ERRO:" $file "nao encontrado"
    }

}

Write-Host ""
Write-Host "8️⃣ Verificando node_modules"

if (Test-Path "node_modules") {
    $size = (Get-ChildItem node_modules -Recurse | Measure-Object).Count
    Write-Host "node_modules presente"
    Write-Host "Arquivos instalados:" $size
}
else {
    Write-Host "node_modules nao existe"
}

Write-Host ""
Write-Host "9️⃣ Testando build"

npm run build

if ($LASTEXITCODE -eq 0) {
    Write-Host ""
    Write-Host "BUILD OK"
}
else {
    Write-Host ""
    Write-Host "BUILD FALHOU"
}

Write-Host ""
Write-Host "==========================================="
Write-Host "FIM DA ANALISE"
Write-Host "==========================================="
