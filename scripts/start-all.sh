#!/bin/bash

# Script Master para iniciar SLTWEB completo
# Backend: uvicorn server:app --host 0.0.0.0 --port 8001 --reload
# Frontend: npm start

echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "🚀 SLTWEB - Iniciando aplicação completa"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""

# 1. Iniciar MongoDB
echo "🗄️ Passo 1: Iniciando MongoDB..."
sudo supervisorctl start mongodb
sleep 3
echo "✅ MongoDB iniciado!"
echo ""

# 2. Iniciar Backend em background
echo "⚙️ Passo 2: Iniciando Backend (uvicorn)..."
cd /app/backend
nohup uvicorn server:app --host 0.0.0.0 --port 8001 --reload > /var/log/backend.log 2>&1 &
BACKEND_PID=$!
echo "✅ Backend iniciado! PID: $BACKEND_PID"
echo "   Logs: tail -f /var/log/backend.log"
sleep 5
echo ""

# 3. Iniciar Frontend em background
echo "🎨 Passo 3: Iniciando Frontend (npm start)..."
cd /app/frontend
nohup npm start > /var/log/frontend.log 2>&1 &
FRONTEND_PID=$!
echo "✅ Frontend iniciado! PID: $FRONTEND_PID"
echo "   Logs: tail -f /var/log/frontend.log"
sleep 3
echo ""

# 4. Iniciar Nginx
echo "🌐 Passo 4: Iniciando Nginx..."
sudo supervisorctl start nginx-code-proxy
sleep 2
echo "✅ Nginx iniciado!"
echo ""

# 5. Verificar status
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "📊 Status dos Serviços:"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""
echo "MongoDB:"
sudo supervisorctl status mongodb
echo ""
echo "Backend (PID $BACKEND_PID):"
ps aux | grep "uvicorn server:app" | grep -v grep | head -1
echo ""
echo "Frontend (PID $FRONTEND_PID):"
ps aux | grep "npm start" | grep -v grep | head -1
echo ""
echo "Nginx:"
sudo supervisorctl status nginx-code-proxy
echo ""

# 6. Testar APIs
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "🧪 Testando conectividade..."
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""
echo "Backend API:"
sleep 2
curl -s http://localhost:8001/api/ || echo "⚠️ Backend ainda não respondeu"
echo ""
echo ""

echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "✅ SLTWEB iniciado com sucesso!"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""
echo "🌐 Acesse: https://fiscal-hub-13.preview.emergentagent.com"
echo "🔐 Login: [CREDENCIAIS DEVEM SER CRIADAS VIA INTERFACE SEGURA OU REPOSITORY VERSIONADO]"
echo ""
echo "📋 Para ver logs:"
echo "   Backend:  tail -f /var/log/backend.log"
echo "   Frontend: tail -f /var/log/frontend.log"
echo ""
echo "⏹️ Para parar tudo:"
echo "   pkill -f 'uvicorn server:app'"
echo "   pkill -f 'npm start'"
echo "   sudo supervisorctl stop all"
echo ""
