# 🎁 PACOTE GOLD - ConsultSLT

## 📦 INFORMAÇÕES DO PACOTE

**Nome do Arquivo:** `consultslt-gold.zip`  
**Tamanho:** 582 KB (compactado) / 2.4 MB (extraído)  
**Localização:** `/app/consultslt-gold.zip`  
**Data de Criação:** 04 de Janeiro de 2026  
**Versão:** 1.0 Gold

---

## 📥 DOWNLOAD

O arquivo `consultslt-gold.zip` está disponível em:
- **Caminho local:** `/app/consultslt-gold.zip`

Para baixar via linha de comando:
```bash
# Copiar para sua máquina
scp usuario@servidor:/app/consultslt-gold.zip ~/Downloads/
```

---

## 📂 CONTEÚDO DO PACOTE

```
consultslt-gold.zip
└── consultslt-gold/
    ├── README.md                    # 📚 Documentação completa
    ├── INICIO_RAPIDO.md             # ⚡ Guia de início rápido
    ├── setup_mongodb.js             # 🗄️ Script de setup MongoDB
    ├── .gitignore                   # 📝 Arquivo gitignore
    ├── backend/                     # 🐍 Backend Python/FastAPI
    │   ├── .env                     # Configurações (PORT=8001)
    │   ├── server.py                # Arquivo principal
    │   ├── requirements.txt         # Dependências Python
    │   ├── api/                     # Rotas da API
    │   ├── clients/                 # Clientes externos
    │   ├── core/                    # Configurações
    │   ├── engines/                 # Engines de processamento
    │   ├── models/                  # Modelos de dados
    │   ├── robots/                  # Robôs de automação
    │   ├── schemas/                 # Schemas Pydantic
    │   ├── services/                # Lógica de negócio
    │   ├── utils/                   # Utilitários
    │   └── uploads/                 # Pasta de uploads
    └── frontend/                    # ⚛️ Frontend React
        ├── .env                     # Configurações (URL=localhost:8001)
        ├── package.json             # Dependências Node
        ├── public/                  # Arquivos estáticos
        └── src/                     # Código-fonte React
            ├── App.js               # Componente principal
            ├── components/          # Componentes React
            ├── context/             # Context API
            ├── pages/               # Páginas da aplicação
            └── lib/                 # Bibliotecas
```

---

## ⚡ INÍCIO RÁPIDO (5 MINUTOS)

### 1. Extrair o Arquivo
```bash
unzip consultslt-gold.zip
cd consultslt-gold
```

### 2. Abrir no VS Code
```bash
code .
```

### 3. Instalar Dependências

**Terminal 1 - Backend:**
```bash
cd backend
python -m venv venv
source venv/bin/activate  # Linux/Mac
# ou
venv\Scripts\activate     # Windows
pip install -r requirements.txt
```

**Terminal 2 - Frontend:**
```bash
cd frontend
npm install
```

### 4. Iniciar MongoDB
```bash
mongod
```

### 5. Iniciar Servidores

**Terminal 1:**
```bash
cd backend
uvicorn server:app --host 0.0.0.0 --port 8001 --reload
```

**Terminal 2:**
```bash
cd frontend
npm start
```

### 6. Acessar
**URL:** http://localhost:3000

---

## 🔑 CREDENCIAIS DE ACESSO

### ✅ Credenciais Padrão (Funcionam Imediatamente)

**Opção 1:**
```
Email:    admin@empresa.com
Senha:    admin123
Tipo:     Administrador
```

**Opção 2:**
```
Email:    william.lucas@sltconsult.com.br
Senha:    slt@2024
Tipo:     Administrador
```

### 📝 Criar Nova Conta (Recomendado)

Após iniciar o backend, execute:
```bash
curl -X POST http://localhost:8001/api/auth/register \
  -H "Content-Type: application/json" \
  -d '{
    "email": "admin@consultslt.com.br",
    "password": "Admin@123",
    "name": "Administrador ConsultSLT"
  }'
```

Depois faça login com:
```
Email:    admin@consultslt.com.br
Senha:    Admin@123
```

---

## 🔧 CONFIGURAÇÕES IMPORTANTES

### Backend (.env)
```env
PORT=8001                              # Porta do servidor
HOST=0.0.0.0                          # Aceita conexões externas
MONGO_URL=mongodb://127.0.0.1:27017  # URL do MongoDB
DB_NAME=consultslt                    # Nome do banco
JWT_SECRET=...                        # Chave JWT
CORS_ORIGINS=http://localhost:3000   # CORS
```

### Frontend (.env)
```env
REACT_APP_BACKEND_URL=http://localhost:8001  # URL do backend
NODE_ENV=development                         # Ambiente
```

**⚠️ IMPORTANTE:** Se for acessar de outra máquina, altere `localhost` para o IP da máquina.

---

## 📚 DOCUMENTAÇÃO

### Arquivos Incluídos:
1. **README.md** - Documentação completa (8.500+ palavras)
   - Instalação detalhada
   - Estrutura do projeto
   - Configuração avançada
   - Solução de problemas
   - Deploy em produção

2. **INICIO_RAPIDO.md** - Guia rápido de 5 minutos
   - Comandos essenciais
   - Credenciais
   - Problemas comuns

3. **setup_mongodb.js** - Script de setup do MongoDB
   - Criação de índices
   - Verificação de usuários
   - Instruções de uso

---

## 🎯 FUNCIONALIDADES INCLUÍDAS

### Módulos do Sistema:
- ✅ **Autenticação:** Login/Registro/Logout com JWT
- ✅ **Dashboard:** Visão geral do sistema
- ✅ **Empresas:** Gestão de clientes
- ✅ **Documentos:** Upload e gestão de documentos fiscais
- ✅ **Obrigações:** Controle de obrigações tributárias
- ✅ **Guias:** Geração e controle de guias
- ✅ **Alertas:** Sistema de notificações
- ✅ **Relatórios:** Relatórios gerenciais
- ✅ **Robôs (RPA):** Automação de processos
- ✅ **Fiscal (IRIS):** Módulo fiscal completo
- ✅ **Auditoria (Kolossus):** Auditoria fiscal
- ✅ **OCR:** Reconhecimento ótico de caracteres

### Tecnologias:
- ⚛️ React 18.2.0
- 🐍 FastAPI (Python)
- 🗄️ MongoDB
- 🎨 Tailwind CSS
- 🧩 Radix UI
- 🔐 JWT Authentication
- 🔄 React Router v6

---

## 🐛 SOLUÇÃO DE PROBLEMAS

### Problema: MongoDB não conecta
```bash
# Verificar se está rodando
mongosh

# Se não estiver, iniciar:
mongod
```

### Problema: Porta em uso
```bash
# Ver processo na porta
lsof -i :8001

# Matar processo
kill -9 <PID>
```

### Problema: Módulo não encontrado
```bash
# Backend
pip install -r requirements.txt

# Frontend
npm install
```

### Mais Problemas?
Consulte o arquivo **README.md** seção "Solução de Problemas"

---

## 🚀 PRÓXIMOS PASSOS

Após a instalação e teste:

1. **Configurar Banco de Dados:**
   - Execute o script: `mongosh < setup_mongodb.js`
   - Crie backup automático

2. **Personalizar:**
   - Altere JWT_SECRET para produção
   - Configure CORS para seu domínio
   - Adicione logo da empresa

3. **Deploy:**
   - Backend: Heroku, Railway, DigitalOcean
   - Frontend: Vercel, Netlify, GitHub Pages
   - Database: MongoDB Atlas

4. **Segurança:**
   - Ative HTTPS (SSL/TLS)
   - Configure autenticação MongoDB
   - Implemente rate limiting
   - Configure backup automático

---

## ✅ CHECKLIST DE VERIFICAÇÃO

Antes de considerar a instalação completa:

- [ ] MongoDB está rodando
- [ ] Backend iniciou sem erros (porta 8001)
- [ ] Frontend iniciou sem erros (porta 3000)
- [ ] Consegue acessar http://localhost:3000
- [ ] Consegue fazer login com credenciais padrão
- [ ] Dashboard carrega corretamente
- [ ] Sem erros no console do navegador (F12)

---

## 📞 INFORMAÇÕES ADICIONAIS

### URLs Importantes:
- **Frontend:** http://localhost:3000
- **Backend API:** http://localhost:8001/api/
- **Documentação API:** http://localhost:8001/docs
- **ReDoc:** http://localhost:8001/redoc

### Portas Usadas:
- **3000:** Frontend React
- **8001:** Backend FastAPI
- **27017:** MongoDB

### Comandos Rápidos:
```bash
# Verificar serviços
curl http://localhost:8001/api/        # Backend
curl http://localhost:3000             # Frontend

# Ver logs
tail -f backend.log
tail -f frontend.log

# Conectar MongoDB
mongosh
use consultslt
db.users.find({}, {password: 0})
```

---

## 🎉 PRONTO PARA USO!

O pacote **ConsultSLT Gold** está completo e pronto para ser usado.

**Qualquer dúvida, consulte:**
- 📖 README.md (documentação completa)
- ⚡ INICIO_RAPIDO.md (guia rápido)
- 🗄️ setup_mongodb.js (setup do banco)

**Boa sorte com seu projeto!** 🚀

---

**Pacote criado por:** Agente E1 - Emergent AI  
**Data:** 04 de Janeiro de 2026  
**Versão:** 1.0 Gold
