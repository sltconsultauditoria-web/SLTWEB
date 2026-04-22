Clear-Host

Write-Host "======================================="
Write-Host "GERANDO PACOTE COMPLETO DA APLICAÇÃO"
Write-Host "======================================="

$package = "consultslt_fullstack_package"

if (Test-Path $package) {
    Remove-Item $package -Recurse -Force
}

New-Item -ItemType Directory -Path $package
New-Item -ItemType Directory -Path "$package/frontend"
New-Item -ItemType Directory -Path "$package/backend"
New-Item -ItemType Directory -Path "$package/database"
New-Item -ItemType Directory -Path "$package/docs"

Write-Host "Copiando frontend..."

if (Test-Path "docs") {
    Copy-Item docs "$package/frontend" -Recurse
}

Write-Host "Copiando backend..."

if (Test-Path "backend") {
    Copy-Item backend "$package/backend" -Recurse
}

Write-Host "Exportando MongoDB..."

mongodump --db consultslt_db --out "$package/database"

Write-Host "Gerando docker-compose..."

$compose = @"
version: '3'

services:

  mongodb:
    image: mongo
    container_name: consultslt_mongo
    ports:
      - "27017:27017"
    volumes:
      - ./database:/data/db

  backend:
    build: ./backend
    ports:
      - "8000:8000"
    depends_on:
      - mongodb

  gateway:
    image: node
    working_dir: /app
    volumes:
      - ./backend:/app
    command: node gateway.js
    ports:
      - "8001:8001"
"@

$compose | Out-File "$package/docker-compose.yml"

Write-Host "Criando README..."

$readme = @"
# CONSULT SLT - FULLSTACK PACKAGE

Arquitetura:

Frontend -> API Gateway -> Backend -> MongoDB

Portas:

Frontend : GitHub Pages
Gateway  : 8001
Backend  : 8000
MongoDB  : 27017

Para iniciar:

docker-compose up -d
"@

$readme | Out-File "$package/README.md"

Write-Host ""
Write-Host "PACOTE GERADO EM:"
Write-Host $package
Write-Host ""
Write-Host "FINALIZADO"