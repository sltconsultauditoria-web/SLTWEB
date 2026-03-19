# 🚀 GUIA PASSO A PASSO - INICIAR APLICAÇÃO NO VS CODE

## 📋 PRÉ-REQUISITOS

Antes de começar, certifique-se de ter instalado:

### ✅ Softwares Necessários

1. **Visual Studio Code**
   - Download: https://code.visualstudio.com/
   - Versão: Qualquer versão recente

2. **Node.js** (v18 ou superior)
   - Download: https://nodejs.org/
   - Verificar instalação:
     ```bash
     node --version
     npm --version
     ```

3. **Python** (v3.10 ou superior)
   - Download: https://www.python.org/
   - Verificar instalação:
     ```bash
     python --version
     # ou
     python3 --version
     ```

4. **MongoDB** (v4.4 ou superior)
   - Download: https://www.mongodb.com/try/download/community
   - Verificar instalação:
     ```bash
     mongosh --version
     ```

---

## 📂 PASSO 1: ESTRUTURA DO PROJETO

A estrutura da aplicação é:

```
/app/
├── backend/                 # 🐍 Backend Python/FastAPI
│   ├── server.py           # Arquivo principal
│   ├── requirements.txt    # Dependências Python
│   ├── .env               # Configurações do backend
│   ├── api/               # Rotas da API
│   ├── services/          # Lógica de negócio
│   ├── models/            # Modelos de dados
│   └── ...
│
├── frontend/               # ⚛️ Frontend React
│   ├── src/               # Código-fonte
│   ├── public/            # Assets estáticos
│   ├── package.json       # Dependências Node
│   └── .env              # Configurações do frontend
│
└── README.md
```

---

## 🎯 PASSO 2: ABRIR PROJETO NO VS CODE

### Opção A: Via Interface Gráfica

1. **Abra o Visual Studio Code**
2. Clique em **File → Open Folder** (ou pressione `Ctrl+K Ctrl+O`)
3. Navegue até a pasta `/app`
4. Selecione a pasta e clique em **Abrir**

### Opção B: Via Terminal

```bash
cd /app
code .
```

### ✅ Verificação
Você deve ver no explorer do VS Code (lado esquerdo):
- 📁 backend
- 📁 frontend
- 📄 README.md

---

## ⚙️ PASSO 3: CONFIGURAR ARQUIVOS .env

### 3.1 Backend (.env)

**Arquivo:** `/app/backend/.env`

**Conteúdo CORRETO:**
```env
# Servidor
PORT=8001
HOST=0.0.0.0

# MongoDB
MONGO_URL=mongodb://127.0.0.1:27017
DB_NAME=consultslt

# Segurança
JWT_SECRET=sltdctfweb-secret-key-2024-secure-change-me

# CORS (Importante para permitir requisições do frontend)
CORS_ORIGINS=http://localhost:3000,http://127.0.0.1:3000

# PostgreSQL (Opcional)
DATABASE_URL=

# Azure / SharePoint (Opcional)
AZURE_TENANT_ID=
AZURE_CLIENT_ID=
AZURE_CLIENT_SECRET=
SHAREPOINT_SITE_URL=
```

### 3.2 Frontend (.env)

**Arquivo:** `/app/frontend/.env`

**Conteúdo CORRETO:**
```env
# URL do Backend (localhost para desenvolvimento)
REACT_APP_BACKEND_URL=http://localhost:8001

# Health Check
ENABLE_HEALTH_CHECK=false

# Ambiente
NODE_ENV=development
```

### ⚠️ IMPORTANTE
- No Windows, use `http://localhost:8001`
- No Linux/Mac, também use `http://localhost:8001`
- NÃO use `127.0.0.1` no frontend .env

---

## 🗄️ PASSO 4: INICIAR MONGODB

### Windows:

**Opção A - Via Serviços:**
1. Pressione `Win + R`
2. Digite `services.msc`
3. Procure por "MongoDB Server"
4. Clique com botão direito → "Iniciar"

**Opção B - Via Linha de Comando:**
```bash
"C:\Program Files\MongoDB\Server\7.0\bin\mongod.exe"
```

### Linux:

```bash
sudo systemctl start mongod
# ou
sudo service mongod start
```

### Mac:

```bash
brew services start mongodb-community
```

### ✅ Verificar se MongoDB está rodando:

```bash
mongosh
# Se conectar, está funcionando!
# Digite 'exit' para sair
```

---

## 📦 PASSO 5: INSTALAR DEPENDÊNCIAS

### 5.1 Backend (Python)

**No VS Code:**
1. Abra um **Terminal Integrado** (Menu: Terminal → New Terminal)
2. Navegue até a pasta backend:
   ```bash
   cd backend
   ```

3. **Criar ambiente virtual (RECOMENDADO):**
   ```bash
   # Windows
   python -m venv venv
   
   # Linux/Mac
   python3 -m venv venv
   ```

4. **Ativar o ambiente virtual:**
   ```bash
   # Windows
   venv\Scripts\activate
   
   # Linux/Mac
   source venv/bin/activate
   ```
   
   Você verá `(venv)` no início da linha do terminal.

5. **Instalar dependências:**
   ```bash
   pip install -r requirements.txt
   ```
   
   Aguarde... Isso pode levar 2-3 minutos.

6. **✅ Verificar instalação:**
   ```bash
   pip list | grep fastapi
   # Deve mostrar: fastapi   0.110.1 (ou similar)
   ```

### 5.2 Frontend (Node)

**No VS Code:**
1. Abra um **SEGUNDO Terminal** (ícone + no canto superior direito do terminal)
2. Navegue até a pasta frontend:
   ```bash
   cd frontend
   ```

3. **Instalar dependências:**
   ```bash
   npm install
   # ou se preferir yarn:
   yarn install
   ```
   
   Aguarde... Isso pode levar 3-5 minutos.

4. **✅ Verificar instalação:**
   ```bash
   ls node_modules | wc -l
   # Deve mostrar mais de 900 pacotes
   ```

---

## ▶️ PASSO 6: INICIAR OS SERVIDORES

Agora você deve ter **2 terminais abertos no VS Code**:
- Terminal 1: Backend
- Terminal 2: Frontend

### 6.1 Iniciar Backend (Terminal 1)

**Certifique-se de estar na pasta backend:**
```bash
cd /app/backend
```

**Ativar ambiente virtual (se ainda não estiver ativo):**
```bash
# Windows
venv\Scripts\activate

# Linux/Mac
source venv/bin/activate
```

**Iniciar o servidor:**
```bash
uvicorn server:app --host 0.0.0.0 --port 8001 --reload
```

**✅ Mensagens de Sucesso:**
```
INFO:     Uvicorn running on http://0.0.0.0:8001
INFO:     Application startup complete.
============================================================
ConsultSLT - Sistema de Gestão Fiscal Integrada
============================================================
✓ MongoDB conectado: consultslt
✓ Todas as rotas da API carregadas com sucesso
============================================================
Servidor pronto para receber requisições!
============================================================
```

**⚠️ NÃO FECHE ESTE TERMINAL!** Deixe rodando.

### 6.2 Iniciar Frontend (Terminal 2)

**Certifique-se de estar na pasta frontend:**
```bash
cd /app/frontend
```

**Iniciar o servidor:**
```bash
npm start
# ou se usou yarn:
yarn start
```

**✅ Mensagens de Sucesso:**
```
Compiled successfully!

You can now view frontend in the browser.

  Local:            http://localhost:3000
  On Your Network:  http://192.168.x.x:3000
```

**⚠️ NÃO FECHE ESTE TERMINAL!** Deixe rodando.

---

## 🌐 PASSO 7: ACESSAR A APLICAÇÃO

### 7.1 Abrir no Navegador

Automaticamente, o navegador deve abrir em:
```
http://localhost:3000
```

Se não abrir automaticamente, copie e cole esta URL no seu navegador.

### 7.2 Tela de Login

Você deve ver:
- ✅ Título: **"SLTWEB"**
- ✅ Subtítulo: "Sistema de Gestão Fiscal Integrada"
- ✅ Formulário de login com campos Email e Senha
- ✅ Botão "Entrar"

---

## 🔑 PASSO 8: FAZER LOGIN

### Credenciais Padrão:

**Opção 1 (Recomendada):**
```
Email:    admin@empresa.com
Senha:    admin123
```

**Opção 2:**
```
Email:    william.lucas@sltconsult.com.br
Senha:    slt@2024
```

**Opção 3:**
```
Email:    admin@consultslt.com.br
Senha:    Admin@123
```

### Passos:
1. Digite o email (copie e cole para evitar erros)
2. Digite a senha (copie e cole para evitar erros)
3. Clique em **"Entrar"**

### ✅ Sucesso!
Você será redirecionado para o **Dashboard** da aplicação.

---

## 🎨 PASSO 9: EXPLORANDO A APLICAÇÃO

Após o login, você terá acesso aos módulos:

1. **📊 Dashboard** - Visão geral do sistema
2. **🏢 Empresas** - Gestão de empresas clientes
3. **📄 Documentos** - Upload e gestão de documentos fiscais
4. **📋 Obrigações** - Controle de obrigações tributárias
5. **💰 Guias** - Geração e controle de guias
6. **🔔 Alertas** - Sistema de notificações
7. **📈 Relatórios** - Relatórios gerenciais
8. **🤖 Robôs** - Automação de processos (RPA)
9. **🧾 Fiscal (IRIS)** - Módulo fiscal completo
10. **🔍 Auditoria (Kolossus)** - Auditoria fiscal
11. **📸 OCR** - Reconhecimento ótico de caracteres

---

## 🛑 PASSO 10: PARAR OS SERVIDORES

Quando quiser parar a aplicação:

### Parar Backend:
- No Terminal 1, pressione: `Ctrl + C`
- Confirme com `Y` se necessário

### Parar Frontend:
- No Terminal 2, pressione: `Ctrl + C`
- Confirme com `Y` se necessário

### Parar MongoDB:
**Windows:**
```bash
net stop MongoDB
```

**Linux:**
```bash
sudo systemctl stop mongod
```

**Mac:**
```bash
brew services stop mongodb-community
```

---

## 🔄 REINICIAR A APLICAÇÃO

Quando quiser iniciar novamente:

### 1. Iniciar MongoDB
```bash
# Windows
net start MongoDB

# Linux
sudo systemctl start mongod

# Mac
brew services start mongodb-community
```

### 2. Abrir VS Code na pasta do projeto
```bash
cd /app
code .
```

### 3. Abrir 2 terminais no VS Code

**Terminal 1 - Backend:**
```bash
cd backend
source venv/bin/activate  # Linux/Mac
# ou
venv\Scripts\activate     # Windows
uvicorn server:app --host 0.0.0.0 --port 8001 --reload
```

**Terminal 2 - Frontend:**
```bash
cd frontend
npm start
```

### 4. Acessar
```
http://localhost:3000
```

---

## 🐛 TROUBLESHOOTING

### Problema 1: "Porta 8001 já está em uso"

**Solução:**
```bash
# Windows
netstat -ano | findstr :8001
taskkill /PID <número_do_PID> /F

# Linux/Mac
lsof -i :8001
kill -9 <PID>
```

### Problema 2: "Porta 3000 já está em uso"

**Solução:**
```bash
# Windows
netstat -ano | findstr :3000
taskkill /PID <número_do_PID> /F

# Linux/Mac
lsof -i :3000
kill -9 <PID>
```

### Problema 3: "MongoDB não está rodando"

**Solução:**
```bash
# Verificar se está instalado
mongosh --version

# Iniciar MongoDB
# Windows
net start MongoDB

# Linux
sudo systemctl start mongod
```

### Problema 4: "ModuleNotFoundError" no Backend

**Solução:**
```bash
cd backend
source venv/bin/activate  # ou venv\Scripts\activate no Windows
pip install -r requirements.txt
```

### Problema 5: "Module not found" no Frontend

**Solução:**
```bash
cd frontend
rm -rf node_modules package-lock.json
npm install
```

### Problema 6: Página em Branco

**Solução:**
1. Verifique se o backend está rodando: `curl http://localhost:8001/api/`
2. Verifique o console do navegador (F12 → Console)
3. Limpe o cache do navegador (Ctrl + Shift + R)
4. Verifique se o arquivo `/app/frontend/.env` tem `REACT_APP_BACKEND_URL=http://localhost:8001`

### Problema 7: Erro de CORS

**Solução:**
Verifique se o arquivo `/app/backend/.env` tem:
```env
CORS_ORIGINS=http://localhost:3000,http://127.0.0.1:3000
```

### Problema 8: Login não funciona

**Solução:**
1. Verifique se o MongoDB está rodando: `mongosh`
2. Verifique se o backend está rodando: `curl http://localhost:8001/api/`
3. Use as credenciais exatas (copie e cole):
   - Email: `admin@empresa.com`
   - Senha: `admin123`

---

## 📊 VERIFICAÇÃO RÁPIDA

### Checklist de Verificação:

```bash
# 1. MongoDB rodando?
mongosh
# Deve conectar. Digite 'exit' para sair.

# 2. Backend rodando?
curl http://localhost:8001/api/
# Deve retornar: {"message":"ConsultSLT API..."}

# 3. Frontend rodando?
curl http://localhost:3000
# Deve retornar HTML

# 4. Ambiente virtual ativado? (Backend)
# Deve mostrar (venv) no início da linha do terminal
```

---

## 🎯 RESUMO DOS COMANDOS

### Sequência Completa (Copy-Paste Friendly):

```bash
# 1. Iniciar MongoDB
# Windows: net start MongoDB
# Linux: sudo systemctl start mongod
# Mac: brew services start mongodb-community

# 2. Backend (Terminal 1)
cd /app/backend
source venv/bin/activate  # ou venv\Scripts\activate (Windows)
uvicorn server:app --host 0.0.0.0 --port 8001 --reload

# 3. Frontend (Terminal 2 - novo terminal)
cd /app/frontend
npm start

# 4. Acessar
# http://localhost:3000
# Login: admin@empresa.com / admin123
```

---

## 📝 NOTAS IMPORTANTES

### Hot Reload Ativado

Ambos os servidores têm **hot reload** ativado:
- **Backend:** Mudanças em `.py` são detectadas automaticamente
- **Frontend:** Mudanças em `.jsx/.js/.css` são detectadas automaticamente

**EXCEÇÃO:** Mudanças em `.env` requerem **restart manual** do servidor.

### Variáveis de Ambiente

**Backend (.env):**
- `PORT=8001` - Porta do servidor backend
- `MONGO_URL` - URL de conexão do MongoDB
- `JWT_SECRET` - Chave secreta para tokens JWT
- `CORS_ORIGINS` - URLs permitidas para CORS

**Frontend (.env):**
- `REACT_APP_BACKEND_URL` - URL do backend
- `NODE_ENV` - Ambiente de execução

### Logs

**Logs do Backend:**
Aparecem diretamente no Terminal 1 onde o backend está rodando.

**Logs do Frontend:**
Aparecem no Terminal 2 e também no **Console do Navegador** (F12 → Console).

---

## 🚀 DICAS AVANÇADAS

### 1. Usar Extensões do VS Code

**Recomendadas:**
- **Python** (Microsoft)
- **Pylance** (Microsoft)
- **ESLint** (Microsoft)
- **Prettier** (Prettier)
- **MongoDB for VS Code** (MongoDB)

### 2. Atalhos Úteis no VS Code

- `Ctrl + `` ` - Abrir/fechar terminal
- `Ctrl + Shift + `` ` - Novo terminal
- `Ctrl + P` - Buscar arquivo
- `Ctrl + Shift + F` - Buscar em todos os arquivos
- `F5` - Iniciar debug

### 3. Debug no VS Code

**Backend (Python):**
Crie `.vscode/launch.json`:
```json
{
  "version": "0.2.0",
  "configurations": [
    {
      "name": "Python: FastAPI",
      "type": "python",
      "request": "launch",
      "module": "uvicorn",
      "args": [
        "server:app",
        "--reload",
        "--host",
        "0.0.0.0",
        "--port",
        "8001"
      ],
      "cwd": "${workspaceFolder}/backend"
    }
  ]
}
```

**Frontend (React):**
Use o Chrome DevTools (F12) para debug do React.

### 4. Executar Testes

**Backend:**
```bash
cd backend
pytest
```

**Frontend:**
```bash
cd frontend
npm test
```

---

## ✅ CHECKLIST FINAL

Antes de considerar tudo funcionando:

- [ ] MongoDB está rodando
- [ ] Backend iniciou sem erros (porta 8001)
- [ ] Frontend iniciou sem erros (porta 3000)
- [ ] Navegador abre em http://localhost:3000
- [ ] Tela de login aparece com "SLTWEB"
- [ ] Login com admin@empresa.com funciona
- [ ] Dashboard carrega após o login
- [ ] Menu lateral está funcionando
- [ ] Nenhum erro no console do navegador (F12)

---

## 🎉 PARABÉNS!

Você agora tem a aplicação **SLTWEB** rodando localmente no seu computador via VS Code!

**URLs Importantes:**
- **Frontend:** http://localhost:3000
- **Backend API:** http://localhost:8001/api/
- **Docs API:** http://localhost:8001/docs

**Credenciais:**
- Email: `admin@empresa.com`
- Senha: `admin123`

**Próximos Passos:**
1. Explore os módulos da aplicação
2. Crie novos usuários
3. Customize conforme necessário
4. Faça backup do banco de dados
5. Configure para produção quando estiver pronto

**Boa sorte com o desenvolvimento! 🚀**

---

**Criado em:** 06 de Janeiro de 2026  
**Aplicação:** SLTWEB - Sistema de Gestão Fiscal Integrada  
**Versão:** 1.0
