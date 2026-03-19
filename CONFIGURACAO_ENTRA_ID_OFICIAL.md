# 🔐 GUIA OFICIAL DE CONFIGURAÇÃO - MICROSOFT ENTRA ID
## Sistema SLTWEB - Integração com Azure Active Directory

**Versão:** 1.0  
**Data:** Janeiro 2026  
**Aplicação:** SLTWEB - Sistema de Gestão Fiscal Integrada

---

## 📋 ÍNDICE

1. [Visão Geral](#visão-geral)
2. [Redirect URI](#redirect-uri)
3. [API Permissions](#api-permissions)
4. [Passo a Passo de Configuração](#passo-a-passo)
5. [Boas Práticas de Segurança](#boas-práticas)
6. [Troubleshooting](#troubleshooting)

---

## 🎯 VISÃO GERAL

### Objetivo da Integração

O SLTWEB integra-se com Microsoft Entra ID (anteriormente Azure AD) para:

1. **Autenticação de Usuários** - Login com credenciais corporativas Microsoft
2. **Acesso ao SharePoint** - Leitura de documentos fiscais armazenados
3. **Sincronização de Dados** - Ingestão automática de documentos via robôs

### Fluxos de Autenticação Utilizados

- **OAuth 2.0 Authorization Code Flow** - Para login de usuários interativo
- **OAuth 2.0 Client Credentials Flow** - Para processos em background (robôs)

### Arquitetura da Solução

```
┌─────────────┐         ┌──────────────┐         ┌─────────────┐
│   Browser   │────────>│   Backend    │────────>│  Entra ID   │
│  (Frontend) │<────────│   (FastAPI)  │<────────│  (Azure AD) │
└─────────────┘         └──────────────┘         └─────────────┘
                               │
                               ▼
                        ┌──────────────┐
                        │  SharePoint  │
                        │   (Docs)     │
                        └──────────────┘
```

---

## 1️⃣ REDIRECT URI (URI DE REDIRECIONAMENTO)

### 📍 O que é Redirect URI?

O Redirect URI é o endpoint da aplicação para onde o Microsoft Entra ID redirecionará o usuário após a autenticação bem-sucedida, enviando o código de autorização (Authorization Code).

### 🌐 Redirect URIs por Ambiente

#### **Desenvolvimento Local:**
```
http://localhost:8001/api/auth/entra/callback
```
**Quando usar:** Desenvolvimento e testes locais no VS Code

---

#### **Servidor de Homologação/Testes (192.168.5.162):**
```
http://192.168.5.162:8001/api/auth/entra/callback
```
**Quando usar:** Testes na rede interna, homologação

---

#### **Produção (Domínio Público):**
```
https://sltweb.suaempresa.com.br/api/auth/entra/callback
```
**Quando usar:** Ambiente de produção com HTTPS obrigatório

⚠️ **IMPORTANTE:** Em produção, SEMPRE use HTTPS. O Entra ID permite HTTP apenas para localhost.

---

### 📐 Estrutura do Redirect URI

```
[PROTOCOLO]://[DOMÍNIO_OU_IP]:[PORTA]/api/auth/entra/callback
```

**Componentes:**
- **Protocolo:** `http` (dev/local) ou `https` (produção)
- **Domínio/IP:** Endereço onde o backend está rodando
- **Porta:** `8001` (porta do backend FastAPI)
- **Path:** `/api/auth/entra/callback` (endpoint fixo da aplicação)

---

### 🔄 Fluxo de Autenticação (OAuth 2.0 Authorization Code)

```
1. Usuário clica em "Login com Microsoft"
   ↓
2. Frontend redireciona para:
   GET https://login.microsoftonline.com/{tenant}/oauth2/v2.0/authorize
   ↓
3. Usuário faz login no Microsoft
   ↓
4. Entra ID redireciona para o Redirect URI com código:
   http://localhost:8001/api/auth/entra/callback?code=ABC123&state=XYZ
   ↓
5. Backend troca o código por access token:
   POST https://login.microsoftonline.com/{tenant}/oauth2/v2.0/token
   ↓
6. Backend obtém dados do usuário:
   GET https://graph.microsoft.com/v1.0/me
   ↓
7. Backend cria sessão e redireciona usuário para dashboard
```

---

### ⚙️ Onde Configurar no Entra ID

**Portal Azure → Entra ID → App registrations → [Seu App] → Authentication**

1. Na seção **Platform configurations**, clique em **Add a platform**
2. Selecione **Web**
3. Em **Redirect URIs**, adicione:
   ```
   http://localhost:8001/api/auth/entra/callback
   http://192.168.5.162:8001/api/auth/entra/callback
   https://sltweb.suaempresa.com.br/api/auth/entra/callback
   ```
4. Em **Implicit grant and hybrid flows**, marque:
   - ✅ **Access tokens** (used for implicit flows)
   - ✅ **ID tokens** (used for implicit and hybrid flows)
5. Clique em **Configure**

---

### 📝 Configuração na Aplicação

**Arquivo:** `/app/backend/.env`

```env
# Redirect URI (usado pela aplicação)
OAUTH_REDIRECT_URI=http://localhost:8001/api/auth/entra/callback

# Para produção, altere para:
# OAUTH_REDIRECT_URI=https://sltweb.suaempresa.com.br/api/auth/entra/callback
```

**Arquivo relacionado:** `/app/backend/services/entra_auth.py` (linha 35-40)

---

## 2️⃣ API PERMISSIONS (PERMISSÕES DE API)

### 📊 Visão Geral das Permissões

| API | Tipo | Permissão | Admin Consent | Justificativa |
|-----|------|-----------|---------------|---------------|
| Microsoft Graph | Delegated | User.Read | Não | Dados básicos do usuário |
| Microsoft Graph | Delegated | email | Não | Email do usuário |
| Microsoft Graph | Delegated | openid | Não | Autenticação OpenID |
| Microsoft Graph | Delegated | profile | Não | Perfil completo do usuário |
| Microsoft Graph | Delegated | Sites.Read.All | **Sim** | Acesso a sites SharePoint |
| Microsoft Graph | Delegated | Files.Read.All | **Sim** | Leitura de arquivos |
| Microsoft Graph | Application | Sites.Read.All | **Sim** | Acesso SharePoint (robôs) |
| Microsoft Graph | Application | Files.Read.All | **Sim** | Leitura arquivos (robôs) |

---

### 🔵 PERMISSÕES DELEGATED (Para usuários interativos)

#### 1. **User.Read** *(Delegated)*

**API:** Microsoft Graph  
**Escopo:** `https://graph.microsoft.com/User.Read`  
**Admin Consent:** ❌ Não necessário  
**Tipo:** Delegated Permission

**Justificativa:**
Permite que a aplicação leia o perfil básico do usuário autenticado, incluindo:
- ID único do usuário (objectId)
- Nome de exibição (displayName)
- Email principal (userPrincipalName)
- Foto do perfil (opcional)

**Uso na aplicação:**
```python
# Arquivo: backend/services/entra_auth.py (linhas 149-179)
def get_user_info(self, access_token: str) -> Dict:
    response = requests.get(
        "https://graph.microsoft.com/v1.0/me",
        headers={"Authorization": f"Bearer {access_token}"}
    )
    return response.json()
```

**Dados obtidos:**
```json
{
  "id": "12345678-1234-1234-1234-123456789012",
  "displayName": "João Silva",
  "userPrincipalName": "joao.silva@empresa.com.br",
  "mail": "joao.silva@empresa.com.br"
}
```

**Princípio do menor privilégio:** ✅ Cumprido  
Esta é a permissão mínima necessária para identificar o usuário após o login.

---

#### 2. **email** *(Delegated)*

**API:** Microsoft Graph (OpenID Connect)  
**Escopo:** `openid email`  
**Admin Consent:** ❌ Não necessário  
**Tipo:** OpenID Connect Scope

**Justificativa:**
Permite acesso ao endereço de email do usuário autenticado. Essential para:
- Identificação única do usuário no sistema
- Criação/associação de conta local
- Envio de notificações (se implementado)
- Recuperação de senha (se implementado)

**Uso na aplicação:**
O email é usado como identificador primário na coleção `users` do MongoDB:
```python
# Arquivo: backend/server.py (linha 121)
user = await db.users.find_one({"email": request.email})
```

**Princípio do menor privilégio:** ✅ Cumprido  
Acesso apenas ao email do usuário autenticado, não de outros usuários.

---

#### 3. **openid** *(Delegated)*

**API:** Microsoft Graph (OpenID Connect)  
**Escopo:** `openid`  
**Admin Consent:** ❌ Não necessário  
**Tipo:** OpenID Connect Scope

**Justificativa:**
Scope obrigatório para autenticação OpenID Connect. Permite:
- Receber um ID Token após autenticação
- Validar a identidade do usuário
- Obter informações básicas de autenticação

**Uso na aplicação:**
```python
# Arquivo: backend/services/entra_auth.py (linha 88)
params = {
    'scope': 'openid email profile User.Read Sites.Read.All Files.Read.All'
}
```

**Princípio do menor privilégio:** ✅ Cumprido  
Scope padrão do OpenID Connect, sem dados adicionais.

---

#### 4. **profile** *(Delegated)*

**API:** Microsoft Graph (OpenID Connect)  
**Escopo:** `openid profile`  
**Admin Consent:** ❌ Não necessário  
**Tipo:** OpenID Connect Scope

**Justificativa:**
Permite acesso ao perfil completo do usuário para melhorar a experiência:
- Nome completo (givenName, surname)
- Cargo/função (jobTitle)
- Telefone (mobilePhone)
- Localização (officeLocation)

**Uso na aplicação:**
Dados exibidos no dashboard e perfil do usuário:
```jsx
// Arquivo: frontend/src/components/Layout/Sidebar.jsx
<div>
  <p>{user.displayName}</p>
  <p className="text-xs">{user.jobTitle}</p>
</div>
```

**Princípio do menor privilégio:** ✅ Cumprido  
Acesso apenas ao perfil do usuário autenticado.

---

#### 5. **Sites.Read.All** *(Delegated)*

**API:** Microsoft Graph  
**Escopo:** `https://graph.microsoft.com/Sites.Read.All`  
**Admin Consent:** ✅ **OBRIGATÓRIO**  
**Tipo:** Delegated Permission

**Justificativa:**
Permite que o usuário autenticado acesse sites SharePoint da organização para:
- Listar sites disponíveis
- Navegar em bibliotecas de documentos
- Visualizar metadados de arquivos
- Baixar documentos fiscais (NFe, SPED, XML)

**Uso na aplicação:**
```python
# Arquivo: backend/services/sharepoint_service.py (linhas 50-60)
async def list_sites(self):
    url = f"{self.graph_api_base}/sites"
    response = requests.get(url, headers=self.headers)
    return response.json()

async def get_site_drives(self, site_id: str):
    url = f"{self.graph_api_base}/sites/{site_id}/drives"
    response = requests.get(url, headers=self.headers)
    return response.json()
```

**Funcionalidades dependentes:**
- 📄 Módulo "Documentos" - Listagem de arquivos do SharePoint
- 🗂️ Sincronização de documentos fiscais
- 📥 Download de NFe, SPED, CT-e do SharePoint

**Por que Admin Consent é necessário:**
Esta permissão permite acesso a **todos os sites SharePoint** da organização, não apenas aos sites do usuário. Por isso, requer aprovação do administrador.

**Princípio do menor privilégio:** ✅ Cumprido  
Permissão de **leitura apenas** (Read). Não permite criar, editar ou deletar sites/documentos.

**Alternativa mais restritiva:** Não disponível. Para acessar sites SharePoint programaticamente, esta é a permissão mínima necessária.

---

#### 6. **Files.Read.All** *(Delegated)*

**API:** Microsoft Graph  
**Escopo:** `https://graph.microsoft.com/Files.Read.All`  
**Admin Consent:** ✅ **OBRIGATÓRIO**  
**Tipo:** Delegated Permission

**Justificativa:**
Permite leitura de arquivos armazenados no OneDrive e SharePoint para:
- Download de documentos fiscais
- Processamento OCR de PDFs
- Extração de dados de XMLs
- Sincronização com banco de dados local

**Uso na aplicação:**
```python
# Arquivo: backend/services/sharepoint_service.py (linhas 80-95)
async def download_file(self, drive_id: str, item_id: str):
    url = f"{self.graph_api_base}/drives/{drive_id}/items/{item_id}/content"
    response = requests.get(url, headers=self.headers)
    return response.content

async def list_drive_items(self, drive_id: str, folder_path: str = None):
    url = f"{self.graph_api_base}/drives/{drive_id}/root/children"
    response = requests.get(url, headers=self.headers)
    return response.json()
```

**Funcionalidades dependentes:**
- 📥 Download de documentos fiscais (PDF, XML)
- 🔍 Módulo OCR - Processamento de documentos
- 🤖 Robôs de ingestão de documentos
- 📊 Extração de dados de SPED

**Por que Admin Consent é necessário:**
Permite acesso a **todos os arquivos** da organização no SharePoint/OneDrive, não apenas aos arquivos do usuário.

**Princípio do menor privilégio:** ✅ Cumprido  
Permissão de **leitura apenas** (Read). Não permite upload, edição ou exclusão de arquivos.

---

### 🟢 PERMISSÕES APPLICATION (Para processos em background)

#### 7. **Sites.Read.All** *(Application)*

**API:** Microsoft Graph  
**Escopo:** `https://graph.microsoft.com/.default`  
**Admin Consent:** ✅ **OBRIGATÓRIO**  
**Tipo:** Application Permission

**Justificativa:**
Permite que a aplicação acesse sites SharePoint **sem interação do usuário**, necessário para:
- Robôs de ingestão automática (background jobs)
- Sincronização programada de documentos (cron jobs)
- Health checks de conectividade SharePoint
- Processos noturnos de backup

**Uso na aplicação:**
```python
# Arquivo: backend/clients/azure_auth_client.py (linhas 48-65)
GRAPH_SCOPE = "https://graph.microsoft.com/.default"

async def get_token(self) -> str:
    """Obtém token via Client Credentials Flow (sem usuário)"""
    data = {
        "grant_type": "client_credentials",
        "client_id": self.client_id,
        "client_secret": self.client_secret,
        "scope": self.GRAPH_SCOPE
    }
    response = requests.post(self.token_url, data=data)
    return response.json()["access_token"]
```

**Funcionalidades dependentes:**
```python
# Arquivo: backend/robots/sharepoint_ingestion_robot.py (linhas 50-70)
class SharePointIngestionRobot:
    def __init__(self):
        self.scheduler = AsyncIOScheduler()
        
    async def sync_documents_scheduled(self):
        """Executa diariamente às 2h da manhã"""
        await self.sync_all_documents()
    
    def start(self):
        self.scheduler.add_job(
            func=self.sync_documents_scheduled,
            trigger='cron',
            hour=2,
            minute=0
        )
        self.scheduler.start()
```

**Por que Admin Consent é obrigatório:**
Application Permissions sempre requerem Admin Consent, pois concedem acesso amplo sem interação do usuário.

**Princípio do menor privilégio:** ✅ Cumprido  
Permissão de **leitura apenas** (Read). Robôs não criam, editam ou deletam documentos.

**Controle de acesso:**
O acesso é restrito pelo Client Secret, que deve ser armazenado de forma segura e rotacionado periodicamente.

---

#### 8. **Files.Read.All** *(Application)*

**API:** Microsoft Graph  
**Escopo:** `https://graph.microsoft.com/.default`  
**Admin Consent:** ✅ **OBRIGATÓRIO**  
**Tipo:** Application Permission

**Justificativa:**
Permite que robôs processem arquivos em horários programados sem usuário logado:
- Ingestão automática noturna de documentos
- Processamento em lote de arquivos fiscais
- Backup automático de documentos críticos
- Auditoria de documentos (verificação de integridade)

**Uso na aplicação:**
```python
# Arquivo: backend/robots/sharepoint_ingestion_robot.py (linhas 90-120)
async def process_files_batch(self, file_list: List[str]):
    """Processa lote de arquivos sem interação do usuário"""
    for file_path in file_list:
        # Download arquivo
        content = await self.sharepoint_client.download_file(file_path)
        
        # Processar OCR
        extracted_data = await self.ocr_service.process(content)
        
        # Salvar no MongoDB
        await self.save_to_database(extracted_data)
```

**Fluxo do robô:**
```
Cron Job (2h AM)
    ↓
Client Credentials Flow (obter token)
    ↓
Listar novos arquivos SharePoint
    ↓
Download de PDFs/XMLs
    ↓
Processamento OCR
    ↓
Extração de dados
    ↓
Armazenamento no MongoDB
    ↓
Log de auditoria
```

**Por que Admin Consent é obrigatório:**
Application Permissions concedem acesso amplo e permanente, sem consentimento do usuário final.

**Princípio do menor privilégio:** ✅ Cumprido  
- **Leitura apenas** (Read)
- **Escopo limitado:** Apenas arquivos em pastas específicas (configurável)
- **Auditoria:** Todos os acessos são logados

---

### 📋 RESUMO DE PERMISSÕES

#### Permissões Delegated (6):
```
openid                     # OpenID Connect - Autenticação
email                      # Email do usuário
profile                    # Perfil completo
User.Read                  # Dados básicos do usuário
Sites.Read.All            # Acesso SharePoint (com usuário)
Files.Read.All            # Leitura de arquivos (com usuário)
```

#### Permissões Application (2):
```
Sites.Read.All            # Acesso SharePoint (sem usuário)
Files.Read.All            # Leitura de arquivos (sem usuário)
```

#### Admin Consent Necessário (4):
```
Sites.Read.All (Delegated)       ✅ Sim
Files.Read.All (Delegated)       ✅ Sim
Sites.Read.All (Application)     ✅ Sim
Files.Read.All (Application)     ✅ Sim
```

---

## 3️⃣ PASSO A PASSO DE CONFIGURAÇÃO NO ENTRA ID

### 📝 PRÉ-REQUISITOS

Antes de começar, certifique-se de ter:

- ✅ Conta Microsoft com privilégios de **Application Administrator** ou **Global Administrator**
- ✅ Acesso ao [Portal Azure](https://portal.azure.com)
- ✅ Tenant ID da organização
- ✅ URLs da aplicação (dev, homologação, produção)

---

### PASSO 1: Criar App Registration

1. Acesse o **Portal Azure**: https://portal.azure.com
2. No menu lateral, clique em **Microsoft Entra ID** (ou **Azure Active Directory**)
3. No menu esquerdo, clique em **App registrations**
4. Clique em **+ New registration** (topo da página)

**Preencha o formulário:**

| Campo | Valor |
|-------|-------|
| **Name** | `SLTWEB - Sistema de Gestão Fiscal` |
| **Supported account types** | `Accounts in this organizational directory only (Single tenant)` |
| **Redirect URI (optional)** | Deixe em branco por enquanto (configuraremos na próxima etapa) |

5. Clique em **Register**

✅ **Resultado:** Você será redirecionado para a página do aplicativo registrado.

📋 **Anote imediatamente:**
- **Application (client) ID**: `xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx`
- **Directory (tenant) ID**: `yyyyyyyy-yyyy-yyyy-yyyy-yyyyyyyyyyyy`

---

### PASSO 2: Configurar Redirect URI

1. Na página do aplicativo, no menu lateral, clique em **Authentication**
2. Em **Platform configurations**, clique em **+ Add a platform**
3. Selecione **Web**

**Configure os Redirect URIs:**

```
http://localhost:8001/api/auth/entra/callback
http://192.168.5.162:8001/api/auth/entra/callback
https://sltweb.suaempresa.com.br/api/auth/entra/callback
```

**IMPORTANTE:** Adicione todas as URLs que você usará (dev, homologação, produção).

4. Em **Implicit grant and hybrid flows**, marque:
   - ✅ **Access tokens** (used for implicit flows)
   - ✅ **ID tokens** (used for implicit and hybrid flows)

5. Em **Allow public client flows**, deixe **No**

6. Clique em **Configure**

7. Clique em **Save** (topo da página)

✅ **Resultado:** Redirect URIs configurados com sucesso.

---

### PASSO 3: Configurar API Permissions

1. No menu lateral, clique em **API permissions**
2. Clique em **+ Add a permission**

#### 3.1 Adicionar Permissões Delegated

**Passo 3.1.1: Microsoft Graph - Delegated**

1. Selecione **Microsoft Graph**
2. Selecione **Delegated permissions**
3. Use a barra de busca para encontrar e marcar:
   - ✅ **openid** (OpenID Connect → openid)
   - ✅ **email** (OpenID Connect → email)
   - ✅ **profile** (OpenID Connect → profile)
   - ✅ **User.Read** (User → User.Read)
   - ✅ **Sites.Read.All** (Sites → Sites.Read.All)
   - ✅ **Files.Read.All** (Files → Files.Read.All)

4. Clique em **Add permissions**

#### 3.2 Adicionar Permissões Application

**Passo 3.2.1: Microsoft Graph - Application**

1. Clique novamente em **+ Add a permission**
2. Selecione **Microsoft Graph**
3. Selecione **Application permissions**
4. Use a barra de busca para encontrar e marcar:
   - ✅ **Sites.Read.All** (Sites → Sites.Read.All)
   - ✅ **Files.Read.All** (Files → Files.Read.All)

5. Clique em **Add permissions**

✅ **Resultado:** Todas as 8 permissões adicionadas.

📋 **Verificação:** A página deve mostrar:

| Permission | Type | Status |
|-----------|------|--------|
| email | Delegated | Not granted |
| Files.Read.All | Delegated | Not granted |
| Files.Read.All | Application | Not granted |
| openid | Delegated | Not granted |
| profile | Delegated | Not granted |
| Sites.Read.All | Delegated | Not granted |
| Sites.Read.All | Application | Not granted |
| User.Read | Delegated | Granted |

---

### PASSO 4: Conceder Admin Consent

⚠️ **CRÍTICO:** Este passo requer privilégios de **Global Administrator** ou **Application Administrator**.

1. Na mesma página (**API permissions**)
2. Clique no botão **✅ Grant admin consent for [Your Organization]**
3. Uma janela de confirmação aparecerá
4. Clique em **Yes**

✅ **Resultado:** Todas as permissões devem mostrar status "✅ Granted for [Your Organization]"

📋 **Verificação Final:**

| Permission | Type | Status |
|-----------|------|--------|
| email | Delegated | ✅ Granted |
| Files.Read.All | Delegated | ✅ Granted |
| Files.Read.All | Application | ✅ Granted |
| openid | Delegated | ✅ Granted |
| profile | Delegated | ✅ Granted |
| Sites.Read.All | Delegated | ✅ Granted |
| Sites.Read.All | Application | ✅ Granted |
| User.Read | Delegated | ✅ Granted |

---

### PASSO 5: Gerar Client Secret

1. No menu lateral, clique em **Certificates & secrets**
2. Clique na aba **Client secrets**
3. Clique em **+ New client secret**

**Configure o secret:**

| Campo | Valor |
|-------|-------|
| **Description** | `SLTWEB Production Secret` |
| **Expires** | `24 months` (recomendado) ou `Custom` |

4. Clique em **Add**

⚠️ **ATENÇÃO MÁXIMA:** O **Value** (valor do secret) será exibido **apenas UMA VEZ**!

📋 **Copie imediatamente:**
- **Secret ID**: `abc123...` (identificador)
- **Value**: `xyz789~...` (valor do secret) ← **ESTE É O SECRET!**
- **Expires**: Data de expiração

✅ **Resultado:** Client Secret gerado com sucesso.

🔐 **Armazenamento Seguro:**
1. Copie o **Value** imediatamente
2. Armazene em local seguro (Password Manager, Azure Key Vault)
3. **NUNCA** comite no Git
4. Configure alerta para renovação 30 dias antes da expiração

---

### PASSO 6: Coletar Informações Necessárias

Você agora possui todas as informações necessárias:

| Informação | Onde Encontrar | Exemplo |
|------------|----------------|---------|
| **Tenant ID** | Overview → Directory (tenant) ID | `12345678-1234-1234-1234-123456789012` |
| **Client ID** | Overview → Application (client) ID | `87654321-4321-4321-4321-210987654321` |
| **Client Secret** | Certificates & secrets → Value | `abc~XyZ123...` |
| **Redirect URI** | Authentication → Redirect URIs | `http://localhost:8001/api/auth/entra/callback` |

---

### PASSO 7: Configurar na Aplicação

#### 7.1 Configurar Backend (.env)

**Arquivo:** `C:\Users\admin-local\ServerApp\consultSLT_web\backend\.env`

Adicione ou edite estas linhas:

```env
# Microsoft Entra ID (Azure AD) - Autenticação
ENTRA_ID_TENANT_ID=12345678-1234-1234-1234-123456789012
ENTRA_ID_CLIENT_ID=87654321-4321-4321-4321-210987654321
ENTRA_ID_CLIENT_SECRET=abc~XyZ123...

# Azure Client (para robôs e processos background)
AZURE_TENANT_ID=12345678-1234-1234-1234-123456789012
AZURE_CLIENT_ID=87654321-4321-4321-4321-210987654321
AZURE_CLIENT_SECRET=abc~XyZ123...

# OAuth Redirect URI
OAUTH_REDIRECT_URI=http://localhost:8001/api/auth/entra/callback

# SharePoint (opcional)
SHAREPOINT_SITE_URL=https://suaempresa.sharepoint.com/sites/fiscal
SHAREPOINT_DRIVE_ID=b!abc123...
```

**Substitua:**
- `12345678-1234-1234-1234-123456789012` → Seu Tenant ID
- `87654321-4321-4321-4321-210987654321` → Seu Client ID
- `abc~XyZ123...` → Seu Client Secret
- `http://localhost:8001/api/auth/entra/callback` → Seu Redirect URI
- `https://suaempresa.sharepoint.com/sites/fiscal` → URL do seu SharePoint

#### 7.2 Reiniciar Backend

```bash
cd C:\Users\admin-local\ServerApp\consultSLT_web\backend
# Parar servidor (Ctrl+C)
uvicorn server:app --host 0.0.0.0 --port 8001 --reload
```

Aguarde ver:
```
INFO:     Application startup complete.
✓ Credenciais Azure AD configuradas
✓ SharePoint Site URL configurado
Servidor pronto para receber requisições!
```

✅ **Configuração concluída!**

---

### PASSO 8: Testar Integração

#### 8.1 Teste via API (Backend)

```bash
# Testar Client Credentials Flow (robôs)
curl -X POST "https://login.microsoftonline.com/{TENANT_ID}/oauth2/v2.0/token" \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "client_id={CLIENT_ID}" \
  -d "client_secret={CLIENT_SECRET}" \
  -d "scope=https://graph.microsoft.com/.default" \
  -d "grant_type=client_credentials"
```

**Resposta esperada:**
```json
{
  "token_type": "Bearer",
  "expires_in": 3599,
  "access_token": "eyJ0eXAiOiJKV1QiLCJub..."
}
```

#### 8.2 Teste via Frontend (Browser)

1. Acesse: `http://localhost:3000`
2. Na tela de login, clique em **"Login com Microsoft"**
3. Você será redirecionado para `login.microsoftonline.com`
4. Faça login com sua conta Microsoft
5. Aceite as permissões (primeira vez)
6. Você será redirecionado de volta para `http://localhost:8001/api/auth/entra/callback`
7. O backend processará o código e redirecionará para o dashboard

✅ **Se chegou ao dashboard, a integração está funcionando!**

---

## 4️⃣ BOAS PRÁTICAS DE SEGURANÇA

### 🔐 Proteção de Client Secret

#### ✅ O QUE FAZER:

1. **Use Azure Key Vault** (Produção)
   ```python
   from azure.keyvault.secrets import SecretClient
   
   secret_client = SecretClient(vault_url="https://seu-vault.vault.azure.net", credential=credential)
   client_secret = secret_client.get_secret("ENTRA-CLIENT-SECRET").value
   ```

2. **Use variáveis de ambiente**
   - ✅ Armazene em `.env` (local)
   - ✅ Use variables de ambiente do servidor (produção)
   - ❌ NUNCA hardcode no código

3. **Rotação de Secrets**
   - Configure expiração em 12-24 meses
   - Configure alerta 30 dias antes da expiração
   - Gere novo secret antes da expiração
   - Atualize aplicação sem downtime (blue-green deployment)

4. **Auditoria de Acessos**
   ```python
   # Log todos os usos do secret
   logger.info(f"Client Secret usado por: {service_name} às {datetime.now()}")
   ```

5. **Permissões de Acesso**
   - Limite quem pode ver o secret no Azure
   - Use RBAC (Role-Based Access Control)
   - Apenas administradores devem ter acesso

#### ❌ O QUE NÃO FAZER:

- ❌ Comitar `.env` no Git
- ❌ Compartilhar secret via email/chat
- ❌ Armazenar em código-fonte
- ❌ Usar mesmo secret em dev/prod
- ❌ Secret sem expiração
- ❌ Copiar/colar em documentos não seguros

---

### 🌍 Considerações por Ambiente

#### 🔵 DESENVOLVIMENTO (Local)

**Configuração:**
```env
ENTRA_ID_TENANT_ID=12345...
ENTRA_ID_CLIENT_ID=67890...
ENTRA_ID_CLIENT_SECRET=dev-secret-abc123...
OAUTH_REDIRECT_URI=http://localhost:8001/api/auth/entra/callback
```

**Boas Práticas:**
- ✅ Use App Registration separado para dev
- ✅ Permissões idênticas à produção (para testes realistas)
- ✅ Secret com expiração de 6-12 meses
- ✅ `.env` no `.gitignore`
- ✅ Documente configuração no README

**Segurança:**
- 🟡 HTTP é aceitável (localhost apenas)
- 🟡 Secret pode ser armazenado em `.env` local
- 🟢 Não compartilhe secret entre desenvolvedores

---

#### 🟡 HOMOLOGAÇÃO (Rede Interna)

**Configuração:**
```env
ENTRA_ID_TENANT_ID=12345...
ENTRA_ID_CLIENT_ID=11111...
ENTRA_ID_CLIENT_SECRET=hml-secret-xyz789...
OAUTH_REDIRECT_URI=http://192.168.5.162:8001/api/auth/entra/callback
```

**Boas Práticas:**
- ✅ Use App Registration separado para homologação
- ✅ Mesmas permissões da produção
- ✅ Secret com expiração de 12 meses
- ✅ Armazene secret em variável de ambiente do servidor
- ✅ Acesso restrito à equipe de testes

**Segurança:**
- 🟡 HTTP aceitável se rede interna segura
- 🟠 HTTPS recomendado mesmo internamente
- 🟢 Firewall deve bloquear acesso externo

---

#### 🔴 PRODUÇÃO (Internet Pública)

**Configuração:**
```env
ENTRA_ID_TENANT_ID=12345...
ENTRA_ID_CLIENT_ID=99999...
ENTRA_ID_CLIENT_SECRET={{KEY_VAULT_REFERENCE}}
OAUTH_REDIRECT_URI=https://sltweb.suaempresa.com.br/api/auth/entra/callback
```

**Boas Práticas:**
- ✅ App Registration exclusivo para produção
- ✅ Secret armazenado no **Azure Key Vault**
- ✅ Secret com expiração de 24 meses
- ✅ Alerta de expiração configurado
- ✅ Plano de rotação documentado
- ✅ **HTTPS obrigatório** (SSL/TLS)
- ✅ Certificado válido (Let's Encrypt ou comercial)
- ✅ Logs de auditoria ativados
- ✅ Monitoramento 24/7

**Segurança:**
- 🔴 **HTTP proibido** (Entra ID rejeita)
- 🔴 Secrets em Key Vault (nunca em `.env`)
- 🔴 RBAC estrito (apenas ops/admins)
- 🔴 Backup de configuração
- 🔴 Disaster recovery plan

---

### 🔒 Princípio do Menor Privilégio

#### ✅ PERMISSÕES CORRETAS (Aplicação SLTWEB)

**Por quê estas permissões são suficientes:**

1. **User.Read** → Apenas dados básicos do usuário logado
2. **Sites.Read.All** → Leitura apenas, sem escrita
3. **Files.Read.All** → Download apenas, sem upload
4. **Application Permissions** → Necessário para robôs, mas ainda Read-Only

#### ❌ PERMISSÕES EXCESSIVAS (Evitar)

**NÃO solicite estas permissões (não são necessárias):**

- ❌ **Sites.ReadWrite.All** → Permite editar sites (desnecessário)
- ❌ **Files.ReadWrite.All** → Permite deletar arquivos (perigoso)
- ❌ **Mail.Send** → Sistema não envia emails via Graph API
- ❌ **User.ReadWrite.All** → Permite editar qualquer usuário (muito amplo)
- ❌ **Directory.ReadWrite.All** → Acesso total ao AD (extremamente perigoso)
- ❌ **User.Export.All** → Exportar dados de usuários (violação LGPD)

**Por quê evitar:**
- Aumenta superfície de ataque
- Dificulta aprovação pelo admin
- Viola compliance (LGPD, ISO 27001)
- Não segue princípio do menor privilégio

---

### 📋 Checklist de Segurança

#### Antes de Deploy em Produção:

- [ ] Client Secret armazenado em Key Vault
- [ ] Secrets diferentes por ambiente (dev/hml/prod)
- [ ] HTTPS configurado com certificado válido
- [ ] Redirect URI usa HTTPS (não HTTP)
- [ ] Firewall configurado (apenas portas necessárias)
- [ ] Logs de auditoria ativados
- [ ] Monitoramento de erros (Sentry, Application Insights)
- [ ] Backup de configuração documentado
- [ ] Plano de rotação de secrets documentado
- [ ] Alerta de expiração configurado (30 dias antes)
- [ ] Acesso ao Azure restrito (RBAC)
- [ ] `.env` no `.gitignore`
- [ ] Documentação atualizada
- [ ] Testes de integração passando
- [ ] Admin Consent concedido
- [ ] Permissões auditadas (apenas as necessárias)

---

## 5️⃣ TROUBLESHOOTING

### ❌ Erro: "AADSTS50011: The reply URL specified in the request does not match..."

**Causa:** Redirect URI não configurado corretamente no Entra ID.

**Solução:**
1. Vá para Portal Azure → Entra ID → App registrations → [Seu App] → Authentication
2. Verifique se o Redirect URI está **exatamente** como na aplicação
3. Certifique-se de incluir a porta (ex: `:8001`)
4. Lembre-se: `http://localhost:8001` ≠ `http://127.0.0.1:8001`

---

### ❌ Erro: "AADSTS65001: The user or administrator has not consented..."

**Causa:** Admin Consent não foi concedido para permissões que requerem.

**Solução:**
1. Portal Azure → Entra ID → App registrations → [Seu App] → API permissions
2. Clique em **Grant admin consent for [Your Organization]**
3. Confirme clicando em **Yes**

---

### ❌ Erro: "Invalid client secret provided"

**Causa:** Client Secret incorreto ou expirado.

**Solução:**
1. Verifique se copiou o **Value** (não o Secret ID)
2. Verifique data de expiração: Portal Azure → Certificates & secrets
3. Se expirado, gere novo secret e atualize na aplicação

---

### ❌ Erro: "Insufficient privileges to complete the operation"

**Causa:** Permissões insuficientes ou Admin Consent não concedido.

**Solução:**
1. Verifique se todas as permissões necessárias foram adicionadas
2. Conceda Admin Consent
3. Aguarde 5-10 minutos para propagação

---

### ❌ Erro: "The tenant '{tenant}' does not exist"

**Causa:** Tenant ID incorreto.

**Solução:**
1. Portal Azure → Entra ID → Overview → Tenant ID
2. Copie o Tenant ID correto
3. Atualize no arquivo `.env`

---

## 📚 REFERÊNCIAS

### Documentação Oficial Microsoft

- [Microsoft Entra ID (Azure AD)](https://learn.microsoft.com/en-us/entra/identity/)
- [Microsoft Graph API](https://learn.microsoft.com/en-us/graph/api/overview)
- [Microsoft Graph Permissions Reference](https://learn.microsoft.com/en-us/graph/permissions-reference)
- [OAuth 2.0 Authorization Code Flow](https://learn.microsoft.com/en-us/entra/identity-platform/v2-oauth2-auth-code-flow)
- [OAuth 2.0 Client Credentials Flow](https://learn.microsoft.com/en-us/entra/identity-platform/v2-oauth2-client-creds-grant-flow)

### Arquivos da Aplicação SLTWEB

- `/backend/services/entra_auth.py` - Serviço de autenticação Entra ID
- `/backend/clients/azure_auth_client.py` - Cliente OAuth2 para robôs
- `/backend/services/sharepoint_service.py` - Integração SharePoint
- `/backend/robots/sharepoint_ingestion_robot.py` - Robô de ingestão
- `/frontend/src/components/EntraIDLogin.jsx` - Componente de login

---

## ✅ CHECKLIST FINAL

Antes de considerar a configuração completa:

- [ ] App Registration criado no Entra ID
- [ ] Redirect URI configurado para todos os ambientes
- [ ] 6 Permissões Delegated adicionadas
- [ ] 2 Permissões Application adicionadas
- [ ] Admin Consent concedido ✅
- [ ] Client Secret gerado e armazenado com segurança
- [ ] Tenant ID, Client ID e Client Secret copiados
- [ ] Arquivo `.env` do backend configurado
- [ ] Backend reiniciado sem erros
- [ ] Teste via API (Client Credentials) passou
- [ ] Teste via Frontend (Authorization Code) passou
- [ ] Login com Microsoft funcionando
- [ ] Acesso ao SharePoint verificado
- [ ] Documentação atualizada

---

## 📞 SUPORTE

Para dúvidas sobre esta integração:

1. **Problemas com Entra ID:** Abra ticket no Azure Support
2. **Problemas com a aplicação:** Verifique logs do backend
3. **Permissões negadas:** Verifique Admin Consent
4. **Secret expirado:** Gere novo secret e atualize aplicação

---

**Documento criado em:** 06 de Janeiro de 2026  
**Versão:** 1.0  
**Aplicação:** SLTWEB - Sistema de Gestão Fiscal Integrada  
**Autor:** Equipe de Desenvolvimento SLTWEB
