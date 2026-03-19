# 🚀 Guia de Inicialização da Aplicação ConsultSLT no Visual Studio Code

## 📋 Pré-requisitos

Antes de começar, certifique-se de ter instalado em sua máquina:

- **Node.js** (versão 18 ou superior) - [Download](https://nodejs.org/)
- **Python** (versão 3.11 ou superior) - [Download](https://www.python.org/)
- **MongoDB** (versão 4.4 ou superior) - [Download](https://www.mongodb.com/try/download/community)
- **Visual Studio Code** - [Download](https://code.visualstudio.com/)
- **Yarn** (gerenciador de pacotes) - `npm install -g yarn`

---

## 📁 Estrutura do Projeto

```
/app/
├── backend/          # API FastAPI (Python)
│   ├── server.py     # Arquivo principal do servidor
│   ├── .env          # Variáveis de ambiente do backend
│   └── requirements.txt
├── frontend/         # Interface React
│   ├── src/          # Código fonte
│   ├── .env          # Variáveis de ambiente do frontend
│   └── package.json
└── GUIA_INICIALIZACAO_VSCODE.md (este arquivo)
```

---

## 🔧 Configuração Inicial (Primeira vez apenas)

### 1️⃣ Abrir o Projeto no VS Code

1. Abra o Visual Studio Code
2. Clique em **File** → **Open Folder**
3. Navegue até a pasta do projeto e selecione `/app`
4. Clique em **Abrir**

### 2️⃣ Instalar Extensões Recomendadas no VS Code

- **Python** (Microsoft)
- **Pylance** (Microsoft)
- **ESLint** (Microsoft)
- **Prettier** (Prettier)
- **MongoDB for VS Code** (MongoDB)

### 3️⃣ Configurar MongoDB

**Opção A: MongoDB já instalado e rodando**
- Verifique se o MongoDB está rodando: abra um terminal e digite:
  ```bash
  mongosh
  ```
- Se conectar com sucesso, o MongoDB está funcionando!

**Opção B: Iniciar MongoDB manualmente**
- **Windows:**
  ```bash
  "C:\Program Files\MongoDB\Server\7.0\bin\mongod.exe" --dbpath "C:\data\db"
  ```
- **Linux/Mac:**
  ```bash
  sudo systemctl start mongod
  # ou
  brew services start mongodb-community
  ```

### 4️⃣ Instalar Dependências

#### Backend (Python)
1. Abra um terminal no VS Code (**Terminal** → **New Terminal**)
2. Navegue até a pasta backend:
   ```bash
   cd backend
   ```
3. Crie um ambiente virtual Python (recomendado):
   ```bash
   python -m venv venv
   ```
4. Ative o ambiente virtual:
   - **Windows:**
     ```bash
     venv\Scripts\activate
     ```
   - **Linux/Mac:**
     ```bash
     source venv/bin/activate
     ```
5. Instale as dependências:
   ```bash
   pip install -r requirements.txt
   ```

#### Frontend (React)
1. Abra um **segundo terminal** no VS Code (**Terminal** → **New Terminal**)
2. Navegue até a pasta frontend:
   ```bash
   cd frontend
   ```
3. Instale as dependências:
   ```bash
   yarn install
   ```

---

## ▶️ Inicialização da Aplicação

### Método 1: Usando Dois Terminais no VS Code (Recomendado)

#### Terminal 1 - Backend
1. Abra o primeiro terminal
2. Navegue até `/app/backend`:
   ```bash
   cd /app/backend
   ```
3. Ative o ambiente virtual (se criou na configuração inicial):
   - **Windows:** `venv\Scripts\activate`
   - **Linux/Mac:** `source venv/bin/activate`
4. Inicie o servidor backend:
   ```bash
   uvicorn server:app --host 0.0.0.0 --port 8001 --reload
   ```
5. Aguarde até ver a mensagem:
   ```
   INFO:     Uvicorn running on http://0.0.0.0:8001 (Press CTRL+C to quit)
   INFO:     Application startup complete.
   ```

#### Terminal 2 - Frontend
1. Abra o segundo terminal (**Terminal** → **Split Terminal** ou **New Terminal**)
2. Navegue até `/app/frontend`:
   ```bash
   cd /app/frontend
   ```
3. Inicie o servidor de desenvolvimento:
   ```bash
   yarn start
   ```
4. Aguarde até ver a mensagem:
   ```
   Compiled successfully!
   You can now view frontend in the browser.
   Local:            http://localhost:3000
   ```

### Método 2: Usando Scripts do VS Code (Avançado)

Crie um arquivo `.vscode/tasks.json` na raiz do projeto:

```json
{
  "version": "2.0.0",
  "tasks": [
    {
      "label": "Start Backend",
      "type": "shell",
      "command": "cd backend && uvicorn server:app --host 0.0.0.0 --port 8001 --reload",
      "isBackground": true,
      "problemMatcher": []
    },
    {
      "label": "Start Frontend",
      "type": "shell",
      "command": "cd frontend && yarn start",
      "isBackground": true,
      "problemMatcher": []
    },
    {
      "label": "Start All",
      "dependsOn": ["Start Backend", "Start Frontend"],
      "problemMatcher": []
    }
  ]
}
```

Depois use **Terminal** → **Run Task** → **Start All**

---

## 🌐 Acessando a Aplicação

Após iniciar ambos os servidores:

1. **Frontend (Interface do usuário):**
   - URL: `http://localhost:3000`
   - Abra no navegador de sua preferência

2. **Backend (API):**
   - URL: `http://localhost:8001/api/`
   - Documentação interativa: `http://localhost:8001/docs`

---

## 🔑 Credenciais de Acesso

### Usuário Principal (Criado no MongoDB)
- **Email:** `admin@consultslt.com.br`
- **Senha:** `Admin@123`

### Usuários Padrão (Hardcoded no código)
- **Email:** `admin@empresa.com`
  - **Senha:** `admin123`

- **Email:** `william.lucas@sltconsult.com.br`
  - **Senha:** `slt@2024`

---

## 🔧 Arquivos de Configuração

### Backend: `/app/backend/.env`
```env
# Servidor
PORT=8001
HOST=0.0.0.0

# MongoDB
MONGO_URL=mongodb://127.0.0.1:27017
DB_NAME=consultslt

# Segurança
JWT_SECRET=sltdctfweb-secret-key-2024-secure-change-me

# CORS
CORS_ORIGINS=http://localhost:3000,http://192.168.5.162:3000
```

### Frontend: `/app/frontend/.env`
```env
REACT_APP_BACKEND_URL=http://192.168.5.162:8001
ENABLE_HEALTH_CHECK=false
NODE_ENV=production
```

⚠️ **IMPORTANTE:** 
- Se estiver rodando em `localhost`, altere `REACT_APP_BACKEND_URL` para `http://localhost:8001`
- Se estiver acessando de outra máquina, use o IP correto (ex: `http://192.168.5.162:8001`)

---

## 🛠️ Comandos Úteis

### Backend
```bash
# Verificar se backend está rodando
curl http://localhost:8001/api/

# Parar o servidor
# Pressione CTRL+C no terminal do backend

# Reinstalar dependências
cd backend
pip install -r requirements.txt --force-reinstall
```

### Frontend
```bash
# Limpar cache e reinstalar
cd frontend
rm -rf node_modules
yarn install

# Build de produção
yarn build

# Parar o servidor
# Pressione CTRL+C no terminal do frontend
```

### MongoDB
```bash
# Conectar ao MongoDB
mongosh

# Usar o banco de dados
use consultslt

# Listar usuários (sem mostrar senha)
db.users.find({}, {password: 0})

# Verificar coleções
db.getCollectionNames()
```

---

## 🐛 Troubleshooting (Resolução de Problemas)

### Problema: "Porta 8001 já está em uso"
**Solução:**
```bash
# Windows
netstat -ano | findstr :8001
taskkill /PID <PID_NUMBER> /F

# Linux/Mac
lsof -i :8001
kill -9 <PID>
```

### Problema: "Porta 3000 já está em uso"
**Solução:**
```bash
# Windows
netstat -ano | findstr :3000
taskkill /PID <PID_NUMBER> /F

# Linux/Mac
lsof -i :3000
kill -9 <PID>
```

### Problema: "Cannot connect to MongoDB"
**Solução:**
1. Verifique se o MongoDB está rodando:
   ```bash
   mongosh
   ```
2. Se não estiver, inicie-o:
   - Windows: `"C:\Program Files\MongoDB\Server\7.0\bin\mongod.exe" --dbpath "C:\data\db"`
   - Linux/Mac: `sudo systemctl start mongod`

### Problema: "Module not found" no Backend
**Solução:**
```bash
cd backend
pip install -r requirements.txt
```

### Problema: "Module not found" no Frontend
**Solução:**
```bash
cd frontend
rm -rf node_modules package-lock.json
yarn install
```

### Problema: Login não funciona / Erro 401
**Solução:**
1. Verifique se o backend está rodando
2. Verifique o URL no `/app/frontend/.env` (`REACT_APP_BACKEND_URL`)
3. Teste o backend diretamente:
   ```bash
   curl -X POST http://localhost:8001/api/auth/login \
     -H "Content-Type: application/json" \
     -d '{"email":"admin@consultslt.com.br","password":"Admin@123"}'
   ```

---

## 📊 Verificação de Logs

### Logs do Backend
Os logs aparecem diretamente no terminal onde o backend está rodando.

### Logs do Frontend
Os logs aparecem no terminal do frontend e no **Console do Navegador** (F12).

### Logs do MongoDB
```bash
# Ver logs do MongoDB
# Windows
type "C:\Program Files\MongoDB\Server\7.0\log\mongod.log"

# Linux/Mac
tail -f /var/log/mongodb/mongod.log
```

---

## 🎯 Checklist de Inicialização

Antes de reportar problemas, verifique:

- [ ] MongoDB está rodando (`mongosh` conecta com sucesso)
- [ ] Backend está rodando (`curl http://localhost:8001/api/` retorna mensagem)
- [ ] Frontend está rodando (navegador abre `http://localhost:3000`)
- [ ] Arquivo `.env` do backend existe e está correto
- [ ] Arquivo `.env` do frontend existe e está correto
- [ ] As portas 8001 e 3000 não estão sendo usadas por outros processos
- [ ] Todas as dependências foram instaladas (backend e frontend)

---

## 📞 Suporte

Para suporte adicional, consulte:
- Documentação do FastAPI: https://fastapi.tiangolo.com/
- Documentação do React: https://react.dev/
- Documentação do MongoDB: https://www.mongodb.com/docs/

---

## 🔄 Atualizações Futuras

### Adicionar Novo Usuário Admin via MongoDB
```bash
# Conectar ao MongoDB
mongosh consultslt

# Criar novo usuário (a senha será hashada pela API)
# Use a rota de registro da API:
curl -X POST http://localhost:8001/api/auth/register \
  -H "Content-Type: application/json" \
  -d '{"email":"novo@email.com","password":"senha123","name":"Nome Completo"}'
```

### Alterar Porta do Backend
1. Edite `/app/backend/.env`: `PORT=NOVA_PORTA`
2. Edite `/app/frontend/.env`: `REACT_APP_BACKEND_URL=http://localhost:NOVA_PORTA`
3. Reinicie ambos os servidores

### Alterar Porta do Frontend
1. Edite o comando de início:
   ```bash
   PORT=3001 yarn start
   ```
2. Acesse pelo novo endereço: `http://localhost:3001`

---

## ✅ Resumo Final

**Para iniciar a aplicação:**
1. Abra VS Code na pasta `/app`
2. Abra 2 terminais
3. Terminal 1: `cd backend && uvicorn server:app --host 0.0.0.0 --port 8001 --reload`
4. Terminal 2: `cd frontend && yarn start`
5. Acesse: `http://localhost:3000`
6. Login: `admin@consultslt.com.br` / `Admin@123`

**Pronto! Sua aplicação está rodando! 🎉**
