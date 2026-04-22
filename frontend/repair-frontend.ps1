Write-Host ""
Write-Host "===================================="
Write-Host "REPARO AUTOMATICO FRONTEND REACT"
Write-Host "===================================="
Write-Host ""

# 1 - Limpar ambiente
Write-Host "1) Limpando ambiente..."

if (Test-Path "node_modules") {
    Remove-Item node_modules -Recurse -Force
}

if (Test-Path "package-lock.json") {
    Remove-Item package-lock.json -Force
}

npm cache clean --force

Write-Host "OK limpeza concluida"
Write-Host ""

# 2 - Instalar dependencias
Write-Host "2) Instalando dependencias..."
npm install

Write-Host ""
Write-Host "Dependencias instaladas"
Write-Host ""

# 3 - Detectar versão do Tailwind
Write-Host "3) Detectando Tailwind..."

$tailwind = npm ls tailwindcss | Out-String

if ($tailwind -match "tailwindcss@4") {

    Write-Host "Tailwind v4 detectado"

    npm install -D @tailwindcss/postcss

}
elseif ($tailwind -match "tailwindcss@3") {

    Write-Host "Tailwind v3 detectado"
    Write-Host "Configurando PostCSS padrão..."

    $postcss = @"
module.exports = {
  plugins: {
    tailwindcss: {},
    autoprefixer: {},
  },
};
"@

    Set-Content postcss.config.js $postcss

}

Write-Host ""
Write-Host "PostCSS configurado"
Write-Host ""

# 4 - Corrigir CRACO
Write-Host "4) Corrigindo CRACO..."

$craco = @"
module.exports = {
  style: {
    postcss: {
      plugins: [
        require('tailwindcss'),
        require('autoprefixer'),
      ],
    },
  },
};
"@

Set-Content craco.config.js $craco

Write-Host "CRACO corrigido"
Write-Host ""

# 5 - Verificar arquivos essenciais

$files = @(
"craco.config.js",
"postcss.config.js",
"tailwind.config.js"
)

Write-Host "5) Verificando arquivos..."

foreach ($file in $files) {

    if (Test-Path $file) {
        Write-Host "OK:" $file
    }
    else {
        Write-Host "ERRO:" $file "nao encontrado"
    }

}

Write-Host ""

# 6 - Testar build
Write-Host "6) Testando build..."

npm run build

if ($LASTEXITCODE -eq 0) {

    Write-Host ""
    Write-Host "===================================="
    Write-Host "BUILD CORRIGIDO COM SUCESSO"
    Write-Host "===================================="

}
else {

    Write-Host ""
    Write-Host "===================================="
    Write-Host "BUILD AINDA FALHOU"
    Write-Host "Verifique configuracoes manualmente"
    Write-Host "===================================="

}
