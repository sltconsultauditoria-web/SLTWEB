Write-Host "======================================="
Write-Host "DIAGNOSTICO DE BUILD - FRONTEND REACT"
Write-Host "======================================="

Write-Host ""
Write-Host "1️⃣ Verificando Node e NPM"

node -v
npm -v

if (!$?) {
    Write-Host "❌ Node ou NPM não estão funcionando corretamente"
}

Write-Host ""
Write-Host "2️⃣ Verificando existência de arquivos críticos"

$files = @(
"package.json",
"craco.config.js",
"postcss.config.js",
"tailwind.config.js"
)

foreach ($file in $files) {
    if (Test-Path $file) {
        Write-Host "✅ $file encontrado"
    } else {
        Write-Host "❌ $file NÃO encontrado"
    }
}

Write-Host ""
Write-Host "3️⃣ Verificando dependências do package.json"

$pkg = Get-Content package.json | ConvertFrom-Json

$deps = $pkg.dependencies
$devDeps = $pkg.devDependencies

if ($deps."tailwindcss") {
    Write-Host "✅ Tailwind instalado:" $deps."tailwindcss"
} else {
    Write-Host "❌ Tailwind NÃO encontrado"
}

if ($devDeps."@tailwindcss/postcss") {
    Write-Host "✅ Plugin PostCSS do Tailwind encontrado"
} else {
    Write-Host "⚠️ Plugin @tailwindcss/postcss não encontrado"
}

if ($deps."@craco/craco") {
    Write-Host "✅ CRACO encontrado"
} else {
    Write-Host "❌ CRACO não encontrado"
}

Write-Host ""
Write-Host "4️⃣ Verificando PostCSS"

if (Test-Path "postcss.config.js") {

    $content = Get-Content postcss.config.js -Raw

    if ($content -match "@tailwindcss/postcss") {
        Write-Host "✅ PostCSS configurado corretamente para Tailwind v4"
    }
    elseif ($content -match "tailwindcss") {
        Write-Host "⚠️ PostCSS usando tailwindcss direto (pode causar erro)"
    }
    else {
        Write-Host "⚠️ Tailwind não encontrado no PostCSS"
    }

}

Write-Host ""
Write-Host "5️⃣ Verificando node_modules"

if (Test-Path "node_modules") {
    Write-Host "✅ node_modules existe"
} else {
    Write-Host "❌ node_modules não existe"
}

Write-Host ""
Write-Host "6️⃣ Verificando instalação quebrada"

npm ls --depth=0

Write-Host ""
Write-Host "7️⃣ Testando build"

npm run build

if ($LASTEXITCODE -eq 0) {
    Write-Host ""
    Write-Host "🎉 BUILD EXECUTADO COM SUCESSO"
}
else {
    Write-Host ""
    Write-Host "❌ BUILD FALHOU"
}

Write-Host ""
Write-Host "======================================="
Write-Host "FIM DO DIAGNOSTICO"
Write-Host "======================================="