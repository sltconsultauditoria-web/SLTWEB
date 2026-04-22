# 🚀 GUIA DEFINITIVO - COMO INICIAR SLTWEB

## ✅ **FORMA CORRETA DE SUBIR A APLICAÇÃO**

### **Opção 1: Script Automático (RECOMENDADO)**

```bash
bash /app/scripts/start-all.sh
```

Este script inicia tudo automaticamente:
- ✅ MongoDB via supervisor
- ✅ Backend com `uvicorn server:app --host 0.0.0.0 --port 8001 --reload`
- ✅ Frontend com `npm start`
- ✅ Nginx via supervisor

---

### **Opção 2: Manual (Passo a Passo)**

#### **1. Iniciar MongoDB**
```bash
sudo supervisorctl start mongodb
```

#### **2. Iniciar Backend**
```bash
cd /app/backend
uvicorn server:app --host 0.0.0.0 --port 8001 --reload
```
**OU em background:**
```bash
cd /app/backend
nohup uvicorn server:app --host 0.0.0.0 --port 8001 --reload > /var/log/backend.log 2>&1 &
```

#### **3. Iniciar Frontend (em outro terminal ou background)**
```bash
cd /app/frontend
npm start
```
**OU em background:**
```bash
cd /app/frontend
nohup npm start > /var/log/frontend.log 2>&1 &
```

#### **4. Iniciar Nginx**
```bash
sudo supervisorctl start nginx-code-proxy
```

---

## 📋 **VER LOGS EM TEMPO REAL**

### Backend:
```bash
tail -f /var/log/backend.log
```

### Frontend:
```bash
tail -f /var/log/frontend.log
```

### MongoDB:
```bash
tail -f /var/log/supervisor/mongodb.err.log
```

---

## ⏹️ **PARAR TODOS OS SERVIÇOS**

```bash
# Parar Backend e Frontend (processos manuais)
pkill -f 'uvicorn server:app'
pkill -f 'npm start'

# Parar MongoDB e Nginx (supervisor)
sudo supervisorctl stop all
```

---

## 🔄 **REINICIAR APENAS O BACKEND**

```bash
# Parar
pkill -f 'uvicorn server:app'

# Iniciar novamente
cd /app/backend
nohup uvicorn server:app --host 0.0.0.0 --port 8001 --reload > /var/log/backend.log 2>&1 &
```

---

## 🔄 **REINICIAR APENAS O FRONTEND**

```bash
# Parar
pkill -f 'npm start'

# Iniciar novamente
cd /app/frontend
nohup npm start > /var/log/frontend.log 2>&1 &
```

---

## 🧪 **TESTAR SE ESTÁ FUNCIONANDO**

### Backend:
```bash
curl http://localhost:8001/api/
```
**Resposta esperada:**
```json
{"message":"SLTWEB API - Sistema de Gestão Fiscal Integrada"}
```

### Frontend:
```bash
curl -I http://localhost:3000
```
**Resposta esperada:**
```
HTTP/1.1 200 OK
```

### Login:
```bash
curl -X POST http://localhost:8001/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{"email":"admin@consultslt.com.br","password":"Admin@123"}'
```

---

## 📊 **VER STATUS DOS PROCESSOS**

```bash
# Ver processos do Backend
ps aux | grep "uvicorn server:app" | grep -v grep

# Ver processos do Frontend
ps aux | grep "npm start" | grep -v grep

# Ver serviços do Supervisor
sudo supervisorctl status
```

---

## 🌐 **ACESSAR A APLICAÇÃO**

**URL:** https://fiscal-hub-13.preview.emergentagent.com

**Credenciais:**
- Email: `admin@consultslt.com.br`
- Senha: `Admin@123`

---

## 🛠️ **TROUBLESHOOTING**

### ❌ Erro: "Cannot find module 'react-router-dom'"

**Solução:**
```bash
cd /app/frontend
rm -rf node_modules
yarn install
```

### ❌ Backend não responde

**Verificar logs:**
```bash
tail -f /var/log/backend.log
```

**Reiniciar:**
```bash
pkill -f 'uvicorn server:app'
cd /app/backend
nohup uvicorn server:app --host 0.0.0.0 --port 8001 --reload > /var/log/backend.log 2>&1 &
```

### ❌ Frontend não compila

**Verificar logs:**
```bash
tail -f /var/log/frontend.log
```

**Reinstalar dependências:**
```bash
cd /app/frontend
rm -rf node_modules
yarn install
```

### ❌ Porta 8001 ou 3000 já em uso

**Matar processos:**
```bash
# Ver o que está usando a porta 8001
lsof -i :8001

# Matar processo específico
kill -9 <PID>

# Ou matar todos relacionados
pkill -f 'uvicorn server:app'
pkill -f 'npm start'
```

---

## 📁 **SCRIPTS DISPONÍVEIS**

```
/app/scripts/
├── start-all.sh        # Inicia tudo automaticamente
├── start-backend.sh    # Inicia apenas backend
└── start-frontend.sh   # Inicia apenas frontend
```

**Usar:**
```bash
bash /app/scripts/start-all.sh
bash /app/scripts/start-backend.sh
bash /app/scripts/start-frontend.sh
```

---

## ✅ **CHECKLIST DE INICIALIZAÇÃO**

- [ ] MongoDB rodando (`sudo supervisorctl start mongodb`)
- [ ] Backend rodando (`uvicorn server:app --host 0.0.0.0 --port 8001 --reload`)
- [ ] Frontend rodando (`npm start`)
- [ ] Nginx rodando (`sudo supervisorctl start nginx-code-proxy`)
- [ ] Backend responde em http://localhost:8001/api/
- [ ] Frontend responde em http://localhost:3000
- [ ] Login funciona em https://fiscal-hub-13.preview.emergentagent.com

---

## 🎉 **TUDO PRONTO!**

Aplicação SLTWEB rodando com:
- ✅ Backend FastAPI (uvicorn + reload)
- ✅ Frontend React (npm start + hot reload)
- ✅ MongoDB
- ✅ Sistema de Usuários (RBAC)
- ✅ 14 APIs REST
- ✅ 18 Páginas frontend

**Acesse agora:** https://fiscal-hub-13.preview.emergentagent.com 🚀
