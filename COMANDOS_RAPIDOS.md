# 🚀 GUIA RÁPIDO - COMANDOS ESSENCIAIS SLTWEB

## ⚡ COMANDOS PRINCIPAIS

### Ver status de todos os serviços
```bash
sudo supervisorctl status
```

### Iniciar todos os serviços
```bash
sudo supervisorctl start all
```

### Parar todos os serviços
```bash
sudo supervisorctl stop all
```

### Reiniciar todos os serviços
```bash
sudo supervisorctl restart all
```

---

## 🔄 REINICIAR SERVIÇOS INDIVIDUAIS

```bash
# Backend (após alterar código Python)
sudo supervisorctl restart backend

# Frontend (após alterar código React)
sudo supervisorctl restart frontend

# MongoDB
sudo supervisorctl restart mongodb
```

---

## 📋 VER LOGS

```bash
# Backend - últimas 50 linhas
tail -n 50 /var/log/supervisor/backend.err.log

# Backend - acompanhar em tempo real
tail -f /var/log/supervisor/backend.err.log

# Frontend - últimas 50 linhas
tail -n 50 /var/log/supervisor/frontend.err.log

# Frontend - acompanhar em tempo real
tail -f /var/log/supervisor/frontend.err.log
```

---

## 🧪 TESTAR APIs

```bash
# Testar endpoint raiz
curl http://localhost:8001/api/

# Testar health check
curl http://localhost:8001/api/health

# Testar login
curl -X POST http://localhost:8001/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{"email":"admin@consultslt.com.br","password":"Admin@123"}'

# Listar usuários (precisa de token)
TOKEN="seu_token_aqui"
curl -H "Authorization: Bearer $TOKEN" \
  http://localhost:8001/api/usuarios
```

---

## 🗄️ MONGODB

```bash
# Conectar ao MongoDB
mongosh

# Listar databases
mongosh --eval "db.adminCommand('listDatabases')"

# Ver collections
mongosh consultslt --eval "db.getCollectionNames()"

# Contar usuários
mongosh consultslt --eval "db.users.countDocuments()"

# Ver usuários (sem senha)
mongosh consultslt --eval "db.users.find({}, {password: 0}).pretty()"
```

---

## 🔐 CREDENCIAIS

### Super Admin
```
Email: admin@consultslt.com.br
Senha: Admin@123
```

### Admin
```
Email: william.lucas@sltconsult.com.br
Senha: slt@2024
```

### Admin Padrão (trocar senha)
```
Email: admin@empresa.com
Senha: admin@2026
```

---

## 🌐 ACESSAR APLICAÇÃO

**URL:** https://fiscal-hub-13.preview.emergentagent.com

---

## 📊 HEALTH CHECK RÁPIDO

```bash
# Script completo
echo "🏥 Health Check:"
echo "Backend:" && curl -s http://localhost:8001/api/ | head -1
echo "Frontend:" && curl -s -I http://localhost:3000 | grep "HTTP"
echo "MongoDB:" && mongosh --quiet --eval "db.adminCommand('ping')"
sudo supervisorctl status
```

---

## 🛠️ TROUBLESHOOTING

### Backend não inicia
```bash
tail -n 100 /var/log/supervisor/backend.err.log
cd /app/backend && pip install -r requirements.txt
sudo supervisorctl restart backend
```

### Frontend não carrega
```bash
tail -n 100 /var/log/supervisor/frontend.err.log
cd /app/frontend && yarn install
sudo supervisorctl restart frontend
```

### MongoDB não conecta
```bash
sudo supervisorctl status mongodb
mongosh --eval "db.adminCommand('ping')"
```

---

## 📁 ESTRUTURA

```
/app/
├── backend/              # FastAPI (Python)
│   ├── api/             # Endpoints
│   ├── schemas/         # Validações
│   ├── middleware/      # Auth/RBAC
│   └── server.py        # Main
├── frontend/            # React
│   └── src/pages/       # Páginas
└── GUIA_INICIALIZACAO.md  # Este arquivo
```

---

## 🎯 SEQUÊNCIA DE INICIALIZAÇÃO

```bash
# 1. Parar tudo
sudo supervisorctl stop all

# 2. Iniciar na ordem
sudo supervisorctl start mongodb
sleep 3
sudo supervisorctl start backend
sleep 3
sudo supervisorctl start frontend
sleep 2
sudo supervisorctl start nginx-code-proxy

# 3. Verificar
sudo supervisorctl status
```

---

## ✅ TUDO OK!

Aplicação rodando em:
**https://fiscal-hub-13.preview.emergentagent.com**
