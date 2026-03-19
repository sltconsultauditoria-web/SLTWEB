#!/bin/bash

# Script para iniciar o Frontend SLTWEB
# Forma correta: npm start (ou yarn start)

echo "🎨 Iniciando Frontend SLTWEB..."
cd /app/frontend

# Verificar se está na pasta correta
if [ ! -f "package.json" ]; then
    echo "❌ Erro: arquivo package.json não encontrado!"
    exit 1
fi

# Verificar se node_modules existe
if [ ! -d "node_modules" ]; then
    echo "📦 node_modules não encontrado. Instalando dependências..."
    yarn install
fi

# Verificar variáveis de ambiente
if [ ! -f ".env" ]; then
    echo "⚠️ Aviso: arquivo .env não encontrado!"
fi

# Iniciar com npm start
echo "✅ Iniciando React na porta 3000..."
npm start
