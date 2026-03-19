# 🚀 GUIA COMPLETO - COMO SUBIR A APLICAÇÃO SLTWEB

## 📦 **ARQUITETURA DA APLICAÇÃO**

```
SLTWEB Sistema de Gestão Fiscal
├── MongoDB (Banco de Dados) - Porta 27017
├── Backend (FastAPI) - Porta 8001
├── Frontend (React) - Porta 3000
└── Nginx (Proxy Reverso)
```

---

## **1️⃣ VERIFICAR STATUS DOS SERVIÇOS**

### Comando:
```bash
sudo supervisorctl status
```

### Resultado Esperado:
```
backend         RUNNING   pid 48, uptime 0:06:17
frontend        RUNNING   pid 49, uptime 0:06:17
mongodb         RUNNING   pid 50, uptime 0:06:17
nginx-code-proxy RUNNING  pid 47, uptime 0:06:17
```

✅ **Todos devem estar com status RUNNING**

---

## **2️⃣ INICIAR TODOS OS SERVIÇOS**

### Se algum serviço estiver parado:

```bash
# Iniciar todos os serviços de uma vez
sudo supervisorctl start all
```

### Ou iniciar individualmente:

```bash
# Iniciar MongoDB
sudo supervisorctl start mongodb

# Iniciar Backend
sudo supervisorctl start backend

# Iniciar Frontend
sudo supervisorctl start frontend

# Iniciar Nginx
sudo supervisorctl start nginx-code-proxy
```

---

## **3️⃣ REINICIAR TODOS OS SERVIÇOS**

### Quando fizer alterações no código:

```bash
# Reiniciar todos os serviços
sudo supervisorctl restart all
```

### Ou reiniciar individualmente:

```bash
# Reiniciar apenas Backend (após alterações em Python)
sudo supervisorctl restart backend

# Reiniciar apenas Frontend (após alterações em React)
sudo supervisorctl restart frontend
```

---

## **4️⃣ VERIFICAR LOGS DOS SERVIÇOS**

### Ver logs do Backend:
```bash
# Últimas 50 linhas
tail -n 50 /var/log/supervisor/backend.err.log

# Acompanhar logs em tempo real
tail -f /var/log/supervisor/backend.err.log
```

### Ver logs do Frontend:
```bash
# Últimas 50 linhas
tail -n 50 /var/log/supervisor/frontend.err.log

# Acompanhar logs em tempo real
tail -f /var/log/supervisor/frontend.err.log
```

### Ver logs do MongoDB:
```bash
tail -n 50 /var/log/supervisor/mongodb.err.log
```

---

## **5️⃣ VERIFICAR SE OS SERVIÇOS ESTÃO RESPONDENDO**

### Testar Backend (API):
```bash
# Endpoint raiz
curl http://localhost:8001/api/

# Health check
curl http://localhost:8001/api/health

# Listar empresas (sem autenticação pode dar erro 401, mas significa que está funcionando)
curl http://localhost:8001/api/empresas
```

### Resposta esperada do endpoint raiz:
```json
{"message":"SLTWEB API - Sistema de Gestão Fiscal Integrada"}
```

### Testar Frontend:
```bash
# Verificar se o React está servindo
curl -I http://localhost:3000
```

### Resposta esperada:
```
HTTP/1.1 200 OK
Content-Type: text/html
```

### Testar MongoDB:
```bash
# Conectar ao MongoDB e listar databases
mongosh --eval "db.adminCommand('listDatabases')"
```

---

## **6️⃣ ACESSAR A APLICAÇÃO**

### 🌐 **Frontend (Interface Web):**
```
URL: https://fiscal-hub-13.preview.emergentagent.com
ou
URL: http://localhost:3000 (se estiver rodando localmente)
```

### 🔐 **Fazer Login:**

**Super Administrador:**
- Email: `admin@consultslt.com.br`
- Senha: `Admin@123`

**Administrador:**
- Email: `william.lucas@sltconsult.com.br`
- Senha: `slt@2024`

**Admin Padrão (obrigatório trocar senha):**
- Email: `admin@empresa.com`
- Senha: `admin@2026`

---

## **7️⃣ PARAR OS SERVIÇOS**

### Parar todos:
```bash
sudo supervisorctl stop all
```

### Parar individualmente:
```bash
sudo supervisorctl stop backend
sudo supervisorctl stop frontend
sudo supervisorctl stop mongodb
```

---

## **8️⃣ COMANDOS ÚTEIS DO SUPERVISOR**

```bash
# Ver status detalhado
sudo supervisorctl status

# Recarregar configuração (após mudanças no supervisor)
sudo supervisorctl reread
sudo supervisorctl update

# Ver todos os comandos disponíveis
sudo supervisorctl help
```

---

## **9️⃣ ESTRUTURA DE DIRETÓRIOS**

```
/app/
├── backend/              # Código do Backend (FastAPI)
│   ├── api/             # Endpoints da API
│   ├── schemas/         # Schemas Pydantic
│   ├── middleware/      # Autenticação e Autorização
│   ├── services/        # Lógica de negócio
│   ├── server.py        # Arquivo principal
│   ├── requirements.txt # Dependências Python
│   └── .env            # Variáveis de ambiente
│
├── frontend/            # Código do Frontend (React)
│   ├── src/
│   │   ├── pages/      # Páginas da aplicação
│   │   ├── components/ # Componentes reutilizáveis
│   │   └── App.js      # App principal
│   ├── package.json    # Dependências Node
│   └── .env            # Variáveis de ambiente
│
└── data/
    └── uploads/        # Arquivos enviados
```

---

## **🔟 VARIÁVEIS DE AMBIENTE IMPORTANTES**

### Backend (.env):
```bash
MONGO_URL="mongodb://localhost:27017"
DB_NAME="consultslt"
CORS_ORIGINS="*"
JWT_SECRET="sltdctfweb-secret-key-2024"
LOCAL_STORAGE_PATH="/data/uploads"
```

### Frontend (.env):
```bash
REACT_APP_BACKEND_URL=https://fiscal-hub-13.preview.emergentagent.com
WDS_SOCKET_PORT=443
ENABLE_HEALTH_CHECK=false
```

---

## **🐛 TROUBLESHOOTING - PROBLEMAS COMUNS**

### ❌ **Problema: Backend não inicia**

**Verificar logs:**
```bash
tail -n 100 /var/log/supervisor/backend.err.log
```

**Soluções comuns:**
- Verificar se MongoDB está rodando
- Verificar se porta 8001 está livre
- Reinstalar dependências: `cd /app/backend && pip install -r requirements.txt`

---

### ❌ **Problema: Frontend não carrega**

**Verificar logs:**
```bash
tail -n 100 /var/log/supervisor/frontend.err.log
```

**Soluções comuns:**
- Verificar se porta 3000 está livre
- Reinstalar dependências: `cd /app/frontend && yarn install`
- Limpar cache: `cd /app/frontend && rm -rf node_modules && yarn install`

---

### ❌ **Problema: MongoDB não conecta**

**Verificar status:**
```bash
sudo supervisorctl status mongodb
```

**Testar conexão:**
```bash
mongosh --eval "db.adminCommand('ping')"
```

---

### ❌ **Problema: Erro 401/403 nas requisições**

**Causa:** Token JWT inválido ou expirado

**Solução:**
1. Fazer logout
2. Fazer login novamente
3. Token será renovado automaticamente

---

## **🎯 SEQUÊNCIA COMPLETA DE INICIALIZAÇÃO**

### 📝 **Script Completo:**

```bash
#!/bin/bash

echo "🚀 Iniciando SLTWEB Sistema de Gestão Fiscal..."

# 1. Parar todos os serviços
echo "⏹️  Parando serviços..."
sudo supervisorctl stop all

# 2. Aguardar 2 segundos
sleep 2

# 3. Iniciar MongoDB primeiro
echo "🗄️  Iniciando MongoDB..."
sudo supervisorctl start mongodb
sleep 3

# 4. Iniciar Backend
echo "⚙️  Iniciando Backend (FastAPI)..."
sudo supervisorctl start backend
sleep 5

# 5. Iniciar Frontend
echo "🎨 Iniciando Frontend (React)..."
sudo supervisorctl start frontend
sleep 3

# 6. Iniciar Nginx
echo "🌐 Iniciando Nginx..."
sudo supervisorctl start nginx-code-proxy
sleep 2

# 7. Verificar status
echo "✅ Verificando status dos serviços..."
sudo supervisorctl status

# 8. Testar APIs
echo ""
echo "🧪 Testando APIs..."
echo "Backend:" 
curl -s http://localhost:8001/api/ | head -1

echo ""
echo "✅ SLTWEB iniciado com sucesso!"
echo ""
echo "📱 Acesse: https://fiscal-hub-13.preview.emergentagent.com"
echo "🔐 Login: admin@consultslt.com.br / Admin@123"
```

### Para executar:
```bash
bash /caminho/do/script.sh
```

---

## **🔐 CREDENCIAIS DE ACESSO**

### **Super Administrador (Acesso Total):**
```
Email: admin@consultslt.com.br
Senha: Admin@123
Perfil: SUPER_ADMIN
```

### **Administrador:**
```
Email: william.lucas@sltconsult.com.br
Senha: slt@2024
Perfil: ADMIN
```

### **Admin Padrão (Trocar senha no primeiro login):**
```
Email: admin@empresa.com
Senha: admin@2026
Perfil: ADMIN
⚠️ Obrigatório trocar senha
```

---

## **📊 VERIFICAÇÃO DE SAÚDE COMPLETA**

### Script de Health Check:

```bash
#!/bin/bash

echo "🏥 SLTWEB - Health Check Completo"
echo "=================================="
echo ""

# MongoDB
echo "🗄️  MongoDB:"
mongosh --quiet --eval "db.adminCommand('ping')" && echo "✅ OK" || echo "❌ ERRO"
echo ""

# Backend
echo "⚙️  Backend (FastAPI):"
curl -s http://localhost:8001/api/health | grep -q "healthy" && echo "✅ OK" || echo "❌ ERRO"
echo ""

# Frontend
echo "🎨 Frontend (React):"
curl -s -I http://localhost:3000 | grep -q "200 OK" && echo "✅ OK" || echo "❌ ERRO"
echo ""

# Supervisor
echo "📋 Supervisor Status:"
sudo supervisorctl status
echo ""

echo "=================================="
echo "Health Check Completo!"
```

---

## **🎉 PRONTO!**

Sua aplicação SLTWEB está rodando com:
- ✅ 14 APIs REST funcionando
- ✅ Sistema de Usuários e Permissões (RBAC)
- ✅ 3 administradores configurados
- ✅ Dashboard com KPIs em tempo real
- ✅ Gestão completa de Empresas, Guias, Alertas, Certidões, Débitos
- ✅ MongoDB como banco de dados
- ✅ Frontend React conectado ao Backend

**Acesse agora:** https://fiscal-hub-13.preview.emergentagent.com
