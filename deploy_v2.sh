#!/bin/bash

# Script de Implantação SLTWEB v2 no Servidor 192.168.5.162

echo "🚀 Iniciando implantação do SLTWEB v2..."

# 1. Subir Banco de Dados (Docker)
echo "🐘 Iniciando banco de dados PostgreSQL via Docker..."
docker-compose up -d

# Aguardar banco ficar pronto
echo "⏳ Aguardando banco de dados inicializar (15s)..."
sleep 15

# 2. Configurar Backend
echo "⚙️ Configurando Backend..."
cd backend
if [ ! -d "venv" ]; then
    python3 -m venv venv
fi
source venv/bin/activate
pip install -r requirements.txt

# 3. Inicializar Banco e Criar Usuários
echo "🌱 Inicializando banco e criando usuários padrão..."
python seed_users.py

# 4. Iniciar Backend (em background)
echo "🏃 Iniciando servidor Backend na porta 8000..."
pkill -f "uvicorn server:app" || true
nohup uvicorn server:app --host 0.0.0.0 --port 8000 > backend.log 2>&1 &

# 5. Configurar Frontend
echo "💻 Configurando Frontend..."
cd ../frontend
# Usar npm install se a pasta node_modules não existir
if [ ! -d "node_modules" ]; then
    npm install
fi

# 6. Iniciar Frontend (em background)
echo "🌐 Iniciando servidor Frontend na porta 3000..."
pkill -f "craco start" || true
nohup npm start > frontend.log 2>&1 &

echo "✅ Implantação concluída com sucesso!"
echo "🔗 Acesse a aplicação em: http://192.168.5.162:3000"
echo "🔑 Verifique o arquivo CREDENCIAIS.md para dados de acesso."
