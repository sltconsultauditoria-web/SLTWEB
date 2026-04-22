# 🔐 CONFIGURAÇÃO MICROSOFT ENTRA ID - CONSULTSLT

## 📋 INFORMAÇÕES PARA REGISTRO DO APLICATIVO

---

## 1️⃣ REDIRECT URI (URI DE REDIRECIONAMENTO)

### ✅ URI de Callback Principal

```
http://localhost:8001/api/auth/entra/callback
```

**Tipo:** Web  
**Descrição:** Endpoint que processa a resposta de autenticação após o login do usuário no Microsoft Entra ID.

### 🌐 URIs Adicionais para Produção/Staging

Quando deployar em produção, adicione também:

```
https://SEU_DOMINIO.com/api/auth/entra/callback
https://api.SEU_DOMINIO.com/api/auth/entra/callback
```

**Onde configurar no Portal Azure:**
1. Acesse **Azure Portal** → **Entra ID** → **App registrations**
2. Selecione seu aplicativo
3. Vá em **Authentication** (Autenticação)
4. Em **Platform configurations** → **Add a platform** → **Web**
5. Adicione as URIs de redirecionamento acima
6. Marque **ID tokens** e **Access tokens** em **Implicit grant and hybrid flows**

---

## 2️⃣ PERMISSÕES DE API NECESSÁRIAS

### 📊 RESUMO EXECUTIVO

| API | Permissões | Tipo | Admin Consent |
|-----|-----------|------|---------------|
| Microsoft Graph | 6 permissões | Delegated | ✅ Sim |
| SharePoint | 2 permissões | Application | ✅ Sim |

---

## 🔵 MICROSOFT GRAPH API

### **1. User.Read** *(Delegated)*

**Escopo:** `https://graph.microsoft.com/User.Read`

**Justificativa:**
- Permite ler o perfil básico do usuário autenticado
- Necessário para obter informações como nome, email, ID do usuário
- Usado no endpoint `/api/auth/entra/callback` para identificar o usuário
- Implementado em: `/backend/services/entra_auth.py` (método `get_user_info()`)

**Código relacionado:**
```python
# Linha 149-179 de entra_auth.py
def get_user_info(self, access_token: str) -> Dict:
    response = requests.get(
        "https://graph.microsoft.com/v1.0/me",
        headers=headers
    )
    return {
        "id": user_data.get("id"),
        "displayName": user_data.get("displayName"),
        "userPrincipalName": user_data.get("userPrincipalName"),
        "mail": user_data.get("mail")
    }
```

---

### **2. email** *(Delegated)*

**Escopo:** `openid` scope padrão

**Justificativa:**
- Permite acesso ao endereço de email do usuário
- Necessário para identificação única do usuário no sistema
- Usado para criar/associar conta local do usuário
- Email é usado como identificador principal na coleção `users` do MongoDB

**Dados obtidos:**
- Email principal do usuário
- Email de trabalho (se disponível)

---

### **3. profile** *(Delegated)*

**Escopo:** `openid` scope padrão

**Justificativa:**
- Permite acesso ao perfil completo do usuário
- Necessário para obter nome completo, foto, cargo
- Melhora a experiência do usuário mostrando informações personalizadas
- Usado no dashboard e na interface do sistema

**Dados obtidos:**
- Nome completo (displayName)
- Nome e sobrenome (givenName, surname)
- Cargo (jobTitle)
- Telefone (mobilePhone)

---

### **4. Sites.Read.All** *(Delegated)*

**Escopo:** `https://graph.microsoft.com/Sites.Read.All`

**Justificativa:**
- Permite acesso de leitura aos sites SharePoint da organização
- Necessário para a funcionalidade de integração SharePoint
- Usado para listar documentos fiscais armazenados no SharePoint
- Implementado em: `/backend/services/sharepoint_service.py`

**Funcionalidades que dependem:**
- Listagem de sites SharePoint
- Navegação em bibliotecas de documentos
- Download de arquivos fiscais (NFe, SPED, etc.)
- Sincronização de documentos com o sistema

**Código relacionado:**
```python
# sharepoint_service.py
async def list_sites(self):
    """Lista todos os sites SharePoint acessíveis"""
    url = f"{self.graph_api_base}/sites"
```

---

### **5. Files.Read.All** *(Delegated)*

**Escopo:** `https://graph.microsoft.com/Files.Read.All`

**Justificativa:**
- Permite ler arquivos armazenados no OneDrive e SharePoint
- Necessário para acessar documentos fiscais compartilhados
- Usado no módulo de Robôs para ingestão automática de documentos
- Implementado em: `/backend/robots/sharepoint_ingestion_robot.py`

**Funcionalidades que dependem:**
- Download de documentos fiscais do SharePoint
- Leitura de metadados de arquivos
- Sincronização automática de documentos
- Módulo OCR para processar documentos

**Fluxo de uso:**
1. Robô lista arquivos em pasta SharePoint específica
2. Download de arquivos PDF/XML para processamento
3. Extração de dados via OCR
4. Armazenamento no MongoDB

---

### **6. ListItem.Read.All** *(Delegated - OPCIONAL)*

**Escopo:** `https://graph.microsoft.com/Sites.Read.All` (incluso)

**Justificativa:**
- Permite ler itens de listas SharePoint
- Opcional: usado apenas se houver listas customizadas com metadados fiscais
- Facilita a leitura de metadados estruturados de documentos
- Melhora a performance ao evitar parsing de nomes de arquivo

**Funcionalidades que dependem:**
- Leitura de metadados de documentos em listas SharePoint
- Filtros avançados de documentos
- Categorização automática de documentos

**Nota:** Esta permissão é **OPCIONAL** se você não usar listas SharePoint customizadas.

---

## 🟢 SHAREPOINT (APPLICATION PERMISSIONS)

### **7. Sites.Read.All** *(Application)*

**Escopo:** `https://graph.microsoft.com/.default`

**Justificativa:**
- Permite acesso de leitura a **TODOS** os sites SharePoint sem interação do usuário
- Necessário para automação via Client Credentials Flow
- Usado pelos robôs de ingestão que rodam em background
- Implementado em: `/backend/clients/azure_auth_client.py`

**Funcionalidades que dependem:**
- Robô de ingestão automática de documentos (background job)
- Sincronização programada de documentos (cron job)
- Health checks de conectividade SharePoint
- Backup automático de documentos

**Código relacionado:**
```python
# azure_auth_client.py - Linha 48
GRAPH_SCOPE = "https://graph.microsoft.com/.default"

# Client Credentials Flow (sem usuário)
async def get_token(self) -> str:
    data = {
        "grant_type": "client_credentials",
        "client_id": self.client_id,
        "client_secret": self.client_secret,
        "scope": self.GRAPH_SCOPE
    }
```

---

### **8. Files.Read.All** *(Application)*

**Escopo:** `https://graph.microsoft.com/.default`

**Justificativa:**
- Permite acesso de leitura a **TODOS** os arquivos sem interação do usuário
- Necessário para robôs que processam arquivos em horários agendados
- Usado para ingestão automática noturna de documentos
- Implementado em: `/backend/robots/sharepoint_ingestion_robot.py`

**Funcionalidades que dependem:**
- Ingestão automática de documentos (scheduler APScheduler)
- Processamento em lote de arquivos fiscais
- Backup automático de documentos críticos
- Auditoria de documentos

**Fluxo do robô:**
```python
# Executa diariamente às 2h da manhã
scheduler.add_job(
    func=sync_sharepoint_documents,
    trigger='cron',
    hour=2,
    minute=0
)
```

---

## 🔒 TIPO DE CONSENTIMENTO

### Delegated Permissions (Permissões Delegadas)
- ✅ User.Read
- ✅ email
- ✅ profile
- ✅ Sites.Read.All
- ✅ Files.Read.All
- ✅ ListItem.Read.All (opcional)

**Consentimento:** Usuário final ou Admin  
**Quando usado:** Durante login interativo do usuário

### Application Permissions (Permissões de Aplicativo)
- ✅ Sites.Read.All
- ✅ Files.Read.All

**Consentimento:** **ADMIN CONSENT OBRIGATÓRIO** ✅  
**Quando usado:** Robôs e processos em background

---

## ⚙️ CONFIGURAÇÃO PASSO A PASSO NO AZURE PORTAL

### 1. Criar App Registration

1. Acesse **Azure Portal** → **Entra ID** → **App registrations**
2. Clique em **New registration**
3. Preencha:
   - **Name:** ConsultSLT Web App
   - **Supported account types:** Accounts in this organizational directory only (Single tenant)
   - **Redirect URI:** Web → `http://localhost:8001/api/auth/entra/callback`
4. Clique em **Register**

### 2. Configurar Authentication

1. No menu lateral, clique em **Authentication**
2. Em **Platform configurations**, verifique se a URI está correta
3. Em **Implicit grant and hybrid flows**, marque:
   - ✅ Access tokens
   - ✅ ID tokens
4. Em **Allow public client flows**, deixe **No**
5. Clique em **Save**

### 3. Adicionar Permissões de API

1. No menu lateral, clique em **API permissions**
2. Clique em **Add a permission**

**Para Microsoft Graph (Delegated):**
1. Selecione **Microsoft Graph**
2. Escolha **Delegated permissions**
3. Marque:
   - ✅ User.Read
   - ✅ email
   - ✅ openid
   - ✅ profile
   - ✅ Sites.Read.All
   - ✅ Files.Read.All
4. Clique em **Add permissions**

**Para Microsoft Graph (Application):**
1. Clique em **Add a permission** novamente
2. Selecione **Microsoft Graph**
3. Escolha **Application permissions**
4. Marque:
   - ✅ Sites.Read.All
   - ✅ Files.Read.All
5. Clique em **Add permissions**

### 4. Conceder Admin Consent

**⚠️ CRÍTICO: Este passo requer privilégios de Administrador Global ou Application Administrator**

1. Na página **API permissions**, clique em **Grant admin consent for [Your Organization]**
2. Confirme clicando em **Yes**
3. Verifique se todas as permissões mostram ✅ "Granted for [Your Organization]"

### 5. Criar Client Secret

1. No menu lateral, clique em **Certificates & secrets**
2. Clique em **New client secret**
3. Preencha:
   - **Description:** ConsultSLT Production Secret
   - **Expires:** 24 months (recomendado)
4. Clique em **Add**
5. **⚠️ COPIE O SECRET IMEDIATAMENTE** - ele só é mostrado uma vez!
6. Anote:
   - **Client ID** (Application ID)
   - **Client Secret** (Value)
   - **Tenant ID** (Directory ID)

### 6. Configurar Variáveis de Ambiente

Adicione no arquivo `/app/backend/.env`:

```env
# Microsoft Entra ID (Azure AD)
ENTRA_ID_TENANT_ID=seu-tenant-id-aqui
ENTRA_ID_CLIENT_ID=seu-client-id-aqui
ENTRA_ID_CLIENT_SECRET=seu-client-secret-aqui

# Para Azure Client (SharePoint background jobs)
AZURE_TENANT_ID=seu-tenant-id-aqui
AZURE_CLIENT_ID=seu-client-id-aqui
AZURE_CLIENT_SECRET=seu-client-secret-aqui

# Redirect URI
OAUTH_REDIRECT_URI=http://localhost:8001/api/auth/entra/callback

# SharePoint
SHAREPOINT_SITE_URL=https://suaorganizacao.sharepoint.com/sites/fiscal
SHAREPOINT_DRIVE_ID=seu-drive-id-aqui
```

---

## 🧪 TESTANDO A CONFIGURAÇÃO

### 1. Testar Client Credentials Flow (Background Jobs)

```bash
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

### 2. Testar Authorization Code Flow (Login Usuário)

1. Inicie o backend:
   ```bash
   cd /app/backend
   uvicorn server:app --host 0.0.0.0 --port 8001 --reload
   ```

2. Acesse no navegador:
   ```
   http://localhost:8001/api/auth/entra/login
   ```

3. Você será redirecionado para login Microsoft

4. Após login bem-sucedido, será redirecionado para:
   ```
   http://localhost:8001/api/auth/entra/callback?code=...&state=...
   ```

5. Verifique os logs do backend para confirmar sucesso

### 3. Testar Acesso ao Graph API

```python
import requests

headers = {
    "Authorization": f"Bearer {access_token}",
    "Content-Type": "application/json"
}

# Testar User.Read
response = requests.get("https://graph.microsoft.com/v1.0/me", headers=headers)
print(response.json())

# Testar Sites.Read.All
response = requests.get("https://graph.microsoft.com/v1.0/sites", headers=headers)
print(response.json())
```

---

## 🔐 SEGURANÇA E MELHORES PRÁTICAS

### ✅ Princípio do Menor Privilégio

As permissões listadas seguem o princípio do menor privilégio:
- **Read-Only**: Nenhuma permissão de escrita solicitada
- **Escopo limitado**: Apenas leitura de perfil, sites e arquivos
- **Sem permissões sensíveis**: Não solicita Mail.Send, User.ReadWrite.All, etc.

### ✅ Rotação de Secrets

- Secrets expiram em 24 meses
- Configure alerta para renovação 30 dias antes do vencimento
- Use Azure Key Vault em produção

### ✅ Monitoramento

Configure alertas para:
- Falhas de autenticação
- Tokens expirados
- Permissões revogadas
- Tentativas de acesso não autorizado

---

## 📊 DIAGRAMA DE FLUXOS

### Fluxo 1: Login do Usuário (Authorization Code Flow)

```
┌─────────┐         ┌──────────┐         ┌────────────┐         ┌──────────┐
│ Browser │         │ Backend  │         │ Entra ID   │         │  Graph   │
└────┬────┘         └────┬─────┘         └─────┬──────┘         └────┬─────┘
     │                   │                     │                      │
     │ 1. GET /login     │                     │                      │
     ├──────────────────>│                     │                      │
     │                   │                     │                      │
     │ 2. Redirect to    │                     │                      │
     │    Entra ID       │                     │                      │
     │<──────────────────┤                     │                      │
     │                   │                     │                      │
     │ 3. Login Page     │                     │                      │
     ├─────────────────────────────────────────>│                      │
     │                   │                     │                      │
     │ 4. User login     │                     │                      │
     ├─────────────────────────────────────────>│                      │
     │                   │                     │                      │
     │ 5. Redirect with code                   │                      │
     │<─────────────────────────────────────────┤                      │
     │                   │                     │                      │
     │ 6. /callback?code=...                   │                      │
     ├──────────────────>│                     │                      │
     │                   │                     │                      │
     │                   │ 7. Exchange code    │                      │
     │                   │    for token        │                      │
     │                   ├────────────────────>│                      │
     │                   │                     │                      │
     │                   │ 8. Access token     │                      │
     │                   │<────────────────────┤                      │
     │                   │                     │                      │
     │                   │ 9. GET /me          │                      │
     │                   ├───────────────────────────────────────────>│
     │                   │                     │                      │
     │                   │ 10. User info       │                      │
     │                   │<───────────────────────────────────────────┤
     │                   │                     │                      │
     │ 11. JWT + User    │                     │                      │
     │<──────────────────┤                     │                      │
     │                   │                     │                      │
```

### Fluxo 2: Robô de Ingestão (Client Credentials Flow)

```
┌──────────────┐         ┌────────────┐         ┌──────────┐
│ Background   │         │ Entra ID   │         │  Graph   │
│ Robot        │         │            │         │   API    │
└──────┬───────┘         └─────┬──────┘         └────┬─────┘
       │                       │                     │
       │ 1. Request token      │                     │
       │   (client_credentials)│                     │
       ├──────────────────────>│                     │
       │                       │                     │
       │ 2. Access token       │                     │
       │<──────────────────────┤                     │
       │                       │                     │
       │ 3. GET /sites         │                     │
       ├─────────────────────────────────────────────>│
       │                       │                     │
       │ 4. Sites list         │                     │
       │<─────────────────────────────────────────────┤
       │                       │                     │
       │ 5. GET /files         │                     │
       ├─────────────────────────────────────────────>│
       │                       │                     │
       │ 6. Files list         │                     │
       │<─────────────────────────────────────────────┤
       │                       │                     │
       │ 7. Download files     │                     │
       ├─────────────────────────────────────────────>│
       │                       │                     │
       │ 8. File content       │                     │
       │<─────────────────────────────────────────────┤
       │                       │                     │
```

---

## 📚 REFERÊNCIAS

### Documentação Oficial Microsoft

- [Microsoft Graph API Reference](https://learn.microsoft.com/en-us/graph/api/overview)
- [Microsoft Graph Permissions Reference](https://learn.microsoft.com/en-us/graph/permissions-reference)
- [OAuth 2.0 Authorization Code Flow](https://learn.microsoft.com/en-us/entra/identity-platform/v2-oauth2-auth-code-flow)
- [OAuth 2.0 Client Credentials Flow](https://learn.microsoft.com/en-us/entra/identity-platform/v2-oauth2-client-creds-grant-flow)

### Arquivos do Projeto

- `/backend/services/entra_auth.py` - Serviço de autenticação
- `/backend/clients/azure_auth_client.py` - Cliente OAuth2
- `/frontend/src/components/EntraIDLogin.jsx` - Componente de login
- `/backend/services/sharepoint_service.py` - Integração SharePoint
- `/backend/robots/sharepoint_ingestion_robot.py` - Robô de ingestão

---

## ✅ CHECKLIST DE CONFIGURAÇÃO

- [ ] App Registration criado no Azure Portal
- [ ] Redirect URI configurado: `http://localhost:8001/api/auth/entra/callback`
- [ ] Permissões Delegated adicionadas (User.Read, email, profile, Sites.Read.All, Files.Read.All)
- [ ] Permissões Application adicionadas (Sites.Read.All, Files.Read.All)
- [ ] Admin Consent concedido para todas as permissões ✅
- [ ] Client Secret criado e anotado com segurança
- [ ] Variáveis de ambiente configuradas no `/app/backend/.env`
- [ ] Teste de Client Credentials Flow realizado com sucesso
- [ ] Teste de Authorization Code Flow realizado com sucesso
- [ ] Acesso ao Graph API testado e funcionando

---

**Documento criado em:** 04 de Janeiro de 2026  
**Versão:** 1.0  
**Aplicação:** ConsultSLT - Sistema de Gestão Fiscal Integrada
