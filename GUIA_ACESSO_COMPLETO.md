# 🚀 GUIA COMPLETO DE ACESSO E USO - SLTWEB

Sistema de Gestão Fiscal Integrada - 100% Funcional e Persistente

---

## 📋 1. USUÁRIOS E SENHAS

### Usuários Administradores

#### 1. Super Administrador
- **Email:** `admin@consultslt.com.br`
- **Senha:** `Admin@123`
- **Perfil:** `SUPER_ADMIN`
- **Permissões:** Acesso total ao sistema
- **Primeiro Login:** Não (senha não precisa ser trocada)

#### 2. Administrador Principal
- **Email:** `william.lucas@sltconsult.com.br`
- **Senha:** `slt@2024`
- **Perfil:** `ADMIN`
- **Permissões:** Criar, editar e visualizar (exceto exclusão de usuários)
- **Primeiro Login:** Não

#### 3. Administrador Padrão (Força Troca de Senha)
- **Email:** `admin@empresa.com`
- **Senha:** `admin123`
- **Perfil:** `ADMIN`
- **Permissões:** Criar, editar e visualizar
- **Primeiro Login:** **SIM** - Sistema força troca de senha no primeiro acesso

### Resumo de Perfis RBAC

| Perfil | Permissões | Pode Criar | Pode Editar | Pode Excluir |
|--------|-----------|-----------|-------------|--------------|
| **SUPER_ADMIN** | Todas | ✅ | ✅ | ✅ |
| **ADMIN** | Administrativas | ✅ | ✅ | ⚠️ (exceto usuários) |
| **USER** | Operacionais | ❌ | ❌ | ❌ |
| **VIEW** | Somente Leitura | ❌ | ❌ | ❌ |

---

## 🔒 2. REDEFINIR SENHA (Se Necessário)

Se precisar redefinir a senha de algum usuário:

```bash
# Conectar ao servidor
ssh root@192.168.5.162

# Navegar até o backend
cd /app/backend

# Executar script Python para redefinir senha
python3 << EOF
import bcrypt
from database import get_db_context
from models import User

with get_db_context() as db:
    user = db.query(User).filter(User.email == "admin@consultslt.com.br").first()
    if user:
        # Nova senha: Admin@123
        user.password = bcrypt.hashpw("Admin@123".encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
        db.commit()
        print("✅ Senha redefinida com sucesso!")
    else:
        print("❌ Usuário não encontrado")
EOF
```

---

## 💻 3. ACESSO AO SERVIDOR VIA VS CODE

### 3.1. Requisitos
- Visual Studio Code instalado
- Extensão "Remote - SSH" instalada

### 3.2. Instalar Extensão Remote SSH

1. Abrir VS Code
2. Ir em Extensions (Ctrl+Shift+X)
3. Buscar: `Remote - SSH`
4. Instalar a extensão da Microsoft

### 3.3. Conectar ao Servidor

#### Opção 1: Via Command Palette
```
1. Pressionar: Ctrl+Shift+P (ou Cmd+Shift+P no Mac)
2. Digitar: "Remote-SSH: Connect to Host"
3. Selecionar: "Add New SSH Host"
4. Digitar: root@192.168.5.162
5. Selecionar arquivo de config (geralmente ~/.ssh/config)
6. Clicar em "Connect"
7. Digitar a senha quando solicitado
```

#### Opção 2: Via Terminal
```bash
# No terminal local
ssh root@192.168.5.162

# Digitar senha quando solicitado
```

#### Opção 3: Configuração Manual SSH Config
```bash
# Editar arquivo de configuração SSH
nano ~/.ssh/config

# Adicionar:
Host sltweb
    HostName 192.168.5.162
    User root
    Port 22

# Salvar (Ctrl+O) e Fechar (Ctrl+X)

# Conectar usando o nome configurado
ssh sltweb
```

### 3.4. Abrir Projeto no VS Code via SSH

1. Após conectado via SSH
2. No VS Code: File → Open Folder
3. Navegar até: `/app`
4. Clicar em "OK"
5. Projeto será aberto remotamente

---

## 📁 4. ESTRUTURA DE PASTAS NO SERVIDOR

```
/app/
├── backend/                    # Backend FastAPI
│   ├── server.py              # Servidor principal
│   ├── database.py            # Configuração PostgreSQL
│   ├── models.py              # Modelos de dados
│   ├── schemas.py             # Validações Pydantic
│   ├── auth_utils.py          # Autenticação JWT
│   ├── seed_users.py          # Criar usuários
│   ├── seed_data.py           # Dados de exemplo
│   ├── requirements.txt       # Dependências Python
│   ├── .env                   # Variáveis de ambiente
│   └── api/                   # Módulos de API
│       ├── empresas.py
│       ├── guias.py
│       ├── alertas.py
│       ├── usuarios.py
│       ├── certidoes.py
│       ├── debitos.py
│       ├── documentos.py
│       ├── obrigacoes.py
│       └── relatorios.py
│
├── frontend/                   # Frontend React
│   ├── src/
│   │   ├── App.js
│   │   ├── context/
│   │   │   └── AuthContext.jsx
│   │   ├── pages/
│   │   │   ├── LoginPage.jsx
│   │   │   ├── Dashboard.jsx
│   │   │   ├── Empresas.jsx
│   │   │   ├── Alertas.jsx
│   │   │   └── ...outras páginas
│   │   └── components/ui/
│   ├── package.json
│   └── .env
│
├── ENTREGA_FINAL.md           # Documentação de entrega
├── README_INTEGRACAO.md       # Documentação técnica
└── docker-compose.yml         # PostgreSQL (opcional)
```

---

## 🚀 5. INICIAR BACKEND

### Verificar Status
```bash
# Conectar ao servidor
ssh root@192.168.5.162

# Verificar se backend está rodando
sudo supervisorctl status backend
```

### Iniciar Backend
```bash
# Se não estiver rodando, iniciar
sudo supervisorctl start backend

# Ou reiniciar
sudo supervisorctl restart backend
```

### Ver Logs do Backend
```bash
# Logs de erro
tail -f /var/log/supervisor/backend.err.log

# Logs de saída
tail -f /var/log/supervisor/backend.out.log

# Últimas 50 linhas
tail -n 50 /var/log/supervisor/backend.err.log
```

### Testar Backend Diretamente
```bash
# Health check
curl http://192.168.5.162:8001/api/health

# Deve retornar:
# {"status":"healthy","database":"connected","version":"2.0.0"}
```

---

## 🎨 6. INICIAR FRONTEND

### Verificar Status
```bash
# Verificar se frontend está rodando
sudo supervisorctl status frontend
```

### Iniciar Frontend
```bash
# Se não estiver rodando, iniciar
sudo supervisorctl start frontend

# Ou reiniciar
sudo supervisorctl restart frontend
```

### Ver Logs do Frontend
```bash
# Logs de erro
tail -f /var/log/supervisor/frontend.err.log

# Logs de saída
tail -f /var/log/supervisor/frontend.out.log

# Verificar se compilou com sucesso
tail -n 100 /var/log/supervisor/frontend.out.log | grep "Compiled"
```

### Acessar Frontend no Navegador
```
URL: http://192.168.5.162:3000

Credenciais de Teste:
- admin@consultslt.com.br / Admin@123
- william.lucas@sltconsult.com.br / slt@2024
```

---

## 🗄️ 7. VALIDAR CONEXÃO COM BANCO DE DADOS

### Verificar PostgreSQL
```bash
# Status do PostgreSQL
sudo service postgresql status

# Conectar ao banco via psql
sudo -u postgres psql -d app_database

# Dentro do psql:
\dt                              # Listar tabelas
SELECT COUNT(*) FROM users;      # Contar usuários
SELECT email, perfil FROM users; # Listar usuários
\q                              # Sair
```

### Testar Conexão via Backend
```bash
cd /app/backend
python3 << EOF
from database import health_check
if health_check():
    print("✅ Banco de dados conectado!")
else:
    print("❌ Erro na conexão com banco")
EOF
```

---

## 🧪 8. TESTAR LOGIN COM USUÁRIOS

### Teste via CURL (Backend)
```bash
# Login como SUPER_ADMIN
curl -X POST http://192.168.5.162:8001/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{
    "email": "admin@consultslt.com.br",
    "password": "Admin@123"
  }'

# Resposta esperada:
# {
#   "success": true,
#   "message": "Login bem-sucedido!",
#   "token": "eyJhbGc...",
#   "primeiro_login": false,
#   "user": {
#     "id": "...",
#     "email": "admin@consultslt.com.br",
#     "nome": "Super Administrador",
#     "perfil": "super_admin",
#     "permissoes": [...]
#   }
# }
```

### Teste via Frontend
```
1. Abrir navegador: http://192.168.5.162:3000
2. Fazer login com: admin@consultslt.com.br / Admin@123
3. Deve redirecionar para Dashboard
4. Dashboard deve mostrar KPIs reais do banco
5. Navegar para "Empresas" - deve listar 3 empresas
6. Criar nova empresa - deve persistir no banco
7. Recarregar página - dados continuam lá
```

---

## 🔧 9. COMANDOS ÚTEIS

### Gerenciar Serviços
```bash
# Ver status de todos os serviços
sudo supervisorctl status

# Reiniciar backend
sudo supervisorctl restart backend

# Reiniciar frontend
sudo supervisorctl restart frontend

# Parar serviço
sudo supervisorctl stop backend

# Ver logs em tempo real
sudo supervisorctl tail -f backend stderr
```

### Gerenciar PostgreSQL
```bash
# Iniciar PostgreSQL
sudo service postgresql start

# Parar PostgreSQL
sudo service postgresql stop

# Status PostgreSQL
sudo service postgresql status

# Reiniciar PostgreSQL
sudo service postgresql restart
```

### Executar Seeds Novamente
```bash
cd /app/backend

# Recriar usuários (se necessário)
python3 seed_users.py

# Recriar dados de exemplo
python3 seed_data.py
```

---

## ✅ 10. VALIDAÇÃO FINAL

### Checklist de Testes

```bash
# 1. Backend está rodando?
curl http://192.168.5.162:8001/api/health
# Espera: {"status":"healthy","database":"connected"}

# 2. Login funciona?
curl -X POST http://192.168.5.162:8001/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{"email":"admin@consultslt.com.br","password":"Admin@123"}'
# Espera: {"success":true,"token":"..."}

# 3. API de empresas funciona?
TOKEN="seu_token_aqui"
curl -L http://192.168.5.162:8001/api/empresas/ \
  -H "Authorization: Bearer $TOKEN"
# Espera: array com 3 empresas

# 4. Frontend carrega?
curl -I http://192.168.5.162:3000
# Espera: HTTP/1.1 200 OK

# 5. PostgreSQL está rodando?
sudo service postgresql status
# Espera: "online"

# 6. Dados persistem?
# Reiniciar backend
sudo supervisorctl restart backend
# Testar novamente API de empresas - deve retornar as mesmas 3 empresas
```

### Teste Completo de CRUD

```bash
# Obter token
TOKEN=$(curl -s -X POST http://192.168.5.162:8001/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{"email":"admin@consultslt.com.br","password":"Admin@123"}' \
  | python3 -c "import sys,json;print(json.load(sys.stdin)['token'])")

# 1. Listar empresas (READ)
curl -L http://192.168.5.162:8001/api/empresas/ \
  -H "Authorization: Bearer $TOKEN"

# 2. Criar empresa (CREATE)
curl -X POST http://192.168.5.162:8001/api/empresas/ \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "cnpj": "99.888.777/0001-66",
    "razao_social": "TESTE EMPRESA LTDA",
    "nome_fantasia": "Teste",
    "regime_tributario": "SIMPLES_NACIONAL",
    "email": "teste@teste.com"
  }'

# 3. Listar novamente - deve ter 4 empresas agora
curl -L http://192.168.5.162:8001/api/empresas/ \
  -H "Authorization: Bearer $TOKEN"

# 4. Excluir empresa criada
EMPRESA_ID=$(curl -s -L http://192.168.5.162:8001/api/empresas/ \
  -H "Authorization: Bearer $TOKEN" \
  | python3 -c "import sys,json; empresas=json.load(sys.stdin); print([e['id'] for e in empresas if e['cnpj']=='99.888.777/0001-66'][0])")

curl -X DELETE http://192.168.5.162:8001/api/empresas/$EMPRESA_ID \
  -H "Authorization: Bearer $TOKEN"

# 5. Listar novamente - deve voltar a ter 3 empresas
curl -L http://192.168.5.162:8001/api/empresas/ \
  -H "Authorization: Bearer $TOKEN"
```

---

## 🆘 11. RESOLUÇÃO DE PROBLEMAS

### Backend não inicia
```bash
# Ver erro específico
tail -n 100 /var/log/supervisor/backend.err.log

# Problemas comuns:
# - Porta 8001 em uso: sudo lsof -i :8001
# - PostgreSQL não conecta: sudo service postgresql status
# - Dependências faltando: cd /app/backend && pip install -r requirements.txt
```

### Frontend não inicia
```bash
# Ver erro específico
tail -n 100 /var/log/supervisor/frontend.err.log

# Problemas comuns:
# - Porta 3000 em uso: sudo lsof -i :3000
# - Dependências faltando: cd /app/frontend && yarn install
# - Arquivo .env incorreto: cat /app/frontend/.env
```

### Banco de dados não conecta
```bash
# Verificar se PostgreSQL está rodando
sudo service postgresql status

# Tentar iniciar
sudo service postgresql start

# Verificar conexão
sudo -u postgres psql -c "SELECT 1"
```

### "Nenhum dado aparece" no frontend
```bash
# Verificar se tem dados no banco
sudo -u postgres psql -d app_database -c "SELECT COUNT(*) FROM empresas;"

# Se retornar 0, executar seed:
cd /app/backend
python3 seed_data.py
```

---

## 📞 12. INFORMAÇÕES TÉCNICAS

### Portas Utilizadas
- **Frontend:** 3000
- **Backend:** 8001
- **PostgreSQL:** 5432

### Credenciais do Banco
```
Host: localhost
Port: 5432
Database: app_database
User: srv_waza
Password: strong_2026
```

### URLs de Acesso
```
Frontend: http://192.168.5.162:3000
Backend API: http://192.168.5.162:8001
Backend Health: http://192.168.5.162:8001/api/health
Backend Docs (Swagger): http://192.168.5.162:8001/docs
```

### Estrutura de APIs
```
POST   /api/auth/login           # Login
POST   /api/auth/trocar-senha    # Trocar senha
GET    /api/auth/me              # Dados do usuário logado

GET    /api/empresas/            # Listar empresas
POST   /api/empresas/            # Criar empresa
GET    /api/empresas/{id}        # Detalhes empresa
PUT    /api/empresas/{id}        # Atualizar empresa
DELETE /api/empresas/{id}        # Excluir empresa

GET    /api/guias/               # Listar guias
POST   /api/guias/               # Criar guia
PUT    /api/guias/{id}           # Atualizar guia
DELETE /api/guias/{id}           # Excluir guia

GET    /api/alertas/             # Listar alertas
POST   /api/alertas/             # Criar alerta
PATCH  /api/alertas/{id}/marcar-lido  # Marcar como lido
DELETE /api/alertas/{id}         # Excluir alerta

GET    /api/usuarios/            # Listar usuários (ADMIN)
POST   /api/usuarios/            # Criar usuário (ADMIN)
PUT    /api/usuarios/{id}        # Atualizar usuário (ADMIN)
DELETE /api/usuarios/{id}        # Excluir usuário (ADMIN)
```

---

## 🎯 13. GARANTIAS TÉCNICAS

✅ **100% Funcional** - Todas as APIs e telas funcionando  
✅ **Totalmente Persistente** - Dados salvos em PostgreSQL  
✅ **Frontend + Backend + Banco Integrados** - Comunicação completa  
✅ **Sem Mocks** - Todos os dados vêm do banco  
✅ **Sem Dados Fake** - Dados reais persistidos  
✅ **CRUD Completo** - Criar, ler, atualizar e excluir funcionando  
✅ **Autenticação Real** - JWT com expiração de 24h  
✅ **RBAC Ativo** - Controle de acesso por perfil  
✅ **Persistência Garantida** - Restart não perde dados  

---

## 📝 14. RESUMO RÁPIDO

```bash
# 1. Conectar ao servidor
ssh root@192.168.5.162

# 2. Verificar serviços
sudo supervisorctl status

# 3. Acessar no navegador
# http://192.168.5.162:3000

# 4. Login
# Email: admin@consultslt.com.br
# Senha: Admin@123

# 5. Testar CRUD
# Ir em Empresas → Criar → Editar → Excluir

# 6. Verificar persistência
# Recarregar página → dados continuam lá
```

---

**Sistema SLTWEB - 100% Funcional e Pronto para Uso**
