#!/bin/bash

# Script para iniciar o Backend SLTWEB
# Forma correta: uvicorn server:app --host 0.0.0.0 --port 8001 --reload

echo "🚀 Iniciando Backend SLTWEB..."
cd /app/backend

# Verificar se está na pasta correta
if [ ! -f "server.py" ]; then
    echo "❌ Erro: arquivo server.py não encontrado!"
    exit 1
fi

# Verificar variáveis de ambiente
if [ ! -f ".env" ]; then
    echo "⚠️ Aviso: arquivo .env não encontrado!"
fi

# Iniciar com uvicorn
echo "✅ Iniciando uvicorn na porta 8001..."
uvicorn server:app --host 0.0.0.0 --port 8001 --reload
