# Dashboard com KPIs e Métricas - Documentação Completa

## 📋 Sumário

- [Visão Geral](#visão-geral)
- [Arquitetura](#arquitetura)
- [Backend (FastAPI + MongoDB)](#backend)
- [Frontend (React)](#frontend)
- [Endpoints da API](#endpoints)
- [Como Usar](#como-usar)
- [Testes](#testes)
- [Troubleshooting](#troubleshooting)

---

## 🎯 Visão Geral

Sistema completo de **Dashboard com KPIs (Key Performance Indicators)** e Métricas totalmente funcional, persistente e integrado:

✅ **Backend**: FastAPI + MongoDB com CRUD completo
✅ **Frontend**: React + Tailwind CSS com modal de edição
✅ **Persistência**: MongoDB com índices e soft delete
✅ **Snapshots**: Histórico de métricas para comparação
✅ **Atividades**: Registro de ações recentes
✅ **Testes**: Suite completa de testes

---

## 🏗️ Arquitetura

```
┌─────────────────────────────────────────┐
│          Frontend (React)                │
│  - Dashboard.jsx (KPIs + Modal CRUD)    │
│  - Componentes reutilizáveis            │
│  - Integração com API via Axios         │
└──────────────┬──────────────────────────┘
               │ HTTP (REST API)
┌──────────────▼──────────────────────────┐
│       Backend (FastAPI)                  │
│  - /api/dashboard/overview (GET)         │
│  - /api/dashboard/metricas (GET/POST)    │
│  - /api/dashboard/metricas/{id} (PUT)    │
│  - /api/dashboard/metricas/{id} (DELETE) │
│  - /api/dashboard/historico (GET)        │
│  - /api/dashboard/comparacao (GET)       │
└──────────────┬──────────────────────────┘
               │ Motor (Async Driver)
┌──────────────▼──────────────────────────┐
│      MongoDB (Persistência)              │
│  - dashboard_metrics (coleção)           │
│  - dashboard_snapshots (coleção)         │
└─────────────────────────────────────────┘
```

---

## 🔧 Backend

### Estrutura de Diretórios

```
backend/
├── api/
│   ├── dashboard.py          # Endpoints FastAPI
│   └── __init__.py           # Registra router
├── schemas/
│   └── dashboard.py          # Pydantic models
├── models/
│   └── dashboard.py          # MongoEngine documents
├── repositories/
│   └── dashboard.py          # DAO (Data Access Object)
├── services/
│   └── dashboard.py          # Lógica de negócio
└── main_enterprise.py        # App FastAPI principal
```

### Modelos Pydantic (Schemas)

**DashboardMetricCreate** - Para criar nova métrica
```python
{
  "empresas_ativas": 127,
  "empresas_inativas": 12,
  "das_gerados_mes": 98,
  "certidoes_emitidas_mes": 245,
  "alertas_criticos": 3,
  "taxa_conformidade": 94.5,
  "receita_bruta_mes": 458000.0,
  "despesa_mensal": 125000.0,
  "obrigacoes_pendentes": 42
}
```

**DashboardMetric** - Resposta da API
```python
{
  "id": "507f1f77bcf86cd799439011",  # MongoDB ObjectId
  "empresas_ativas": 127,
  "...": "...",
  "proximos_vencimentos": [...],
  "atividades_recentes": [...],
  "data_geracao": "2026-02-15T18:30:00",
  "data_atualizacao": "2026-02-15T18:30:00",
  "ativo": true
}
```

### Modelos MongoDB (MongoEngine)

**DashboardMetric** - Documento principal
- Índices: `data_geracao`, `data_atualizacao`, `ativo`, `-data_geracao`
- Embedded Documents: `ProximoVencimentoDoc`, `AtividadeRecenteDoc`
- Soft delete: marca como `ativo=false` ao deletar

**DashboardSnapshot** - Histórico
- Armazena JSON serializado das métricas
- Rastreia alterações entre snapshots

### Serviço (DashboardService)

Lógica principal de negócio:

```python
# Criar nova métrica
await DashboardService.criar_metrica(dados)

# Obter todas (paginado)
await DashboardService.obter_metricas(skip=0, limit=10)

# Atualizar métrica
await DashboardService.atualizar_metrica(metrica_id, dados_atualizacao)

# Deletar métrica
await DashboardService.deletar_metrica(metrica_id)

# Obter histórico
await DashboardService.obter_historico(dias=30)

# Registrar atividade
await DashboardService.registrar_atividade(
    empresa_id="emp_001",
    empresa_nome="Empresa X",
    acao="DAS gerado"
)

# Comparar períodos
await DashboardService.comparar_periodos(
    data_inicio1, data_fim1,
    data_inicio2, data_fim2
)
```

---

## 📡 Endpoints

### 1. GET `/api/dashboard/overview`
**Obtém overview do dashboard com KPIs principais**

Response:
```json
{
  "total_empresas": 139,
  "empresas_ativas": 127,
  "empresas_inativas": 12,
  "das_gerados_mes": 98,
  "certidoes_emitidas_mes": 245,
  "alertas_criticos": 3,
  "taxa_conformidade": 94.5,
  "obrigacoes_pendentes": 42,
  "ultima_atualizacao": "2026-02-15T18:30:00"
}
```

### 2. GET `/api/dashboard/metricas`
**Lista todas as métricas com paginação**

Query Parameters:
- `skip`: int (default: 0) - Registros a pular
- `limit`: int (default: 10, max: 100) - Limite de registros

Response: `Array[DashboardMetric]`

### 3. POST `/api/dashboard/metricas`
**Cria nova métrica e snapshot**

Body: `DashboardMetricCreate`

Response: `DashboardMetric` (status 201)

### 4. GET `/api/dashboard/metricas/{metrica_id}`
**Obtém métrica específica**

Response: `DashboardMetric`

### 5. PUT `/api/dashboard/metricas/{metrica_id}`
**Atualiza métrica (cria snapshot das alterações)**

Body: `DashboardMetricUpdate` (todos campos opcionais)

Response: `DashboardMetric`

### 6. DELETE `/api/dashboard/metricas/{metrica_id}`
**Deleta métrica (soft delete - marca como inativa)**

Response: 204 No Content

### 7. GET `/api/dashboard/historico`
**Obtém snapshots históricos**

Query Parameters:
- `dias`: int (default: 30, max: 365) - Número de dias

Response: `Array[DashboardMetric]`

### 8. GET `/api/dashboard/comparacao`
**Compara métricas entre dois períodos**

Query Parameters:
- `data_inicio1`: datetime
- `data_fim1`: datetime
- `data_inicio2`: datetime
- `data_fim2`: datetime

Response:
```json
{
  "periodo_1": {
    "empresas_ativas_media": 125.5,
    "das_media": 85.2,
    "conformidade_media": 92.1
  },
  "periodo_2": {
    "empresas_ativas_media": 128.3,
    "das_media": 92.5,
    "conformidade_media": 94.2
  }
}
```

### 9. POST `/api/dashboard/registrar-atividade`
**Registra atividade recente no dashboard**

Query Parameters:
- `empresa_id`: str (obrigatório)
- `empresa_nome`: str (obrigatório)
- `acao`: str (obrigatório)
- `usuario_id`: str (opcional)
- `detalhes`: str (opcional)

Response:
```json
{
  "mensagem": "Atividade registrada com sucesso"
}
```

---

## 🎨 Frontend

### Componente Dashboard.jsx

**Localização**: `frontend/src/pages/Dashboard.jsx`

**Features**:
- ✅ KPI Cards (8 métricas)
- ✅ Modal CRUD para criar/editar métricas
- ✅ Histórico de métricas com editar/deletar
- ✅ Próximos vencimentos
- ✅ Atividades recentes
- ✅ Atualização em tempo real
- ✅ Loading states
- ✅ Confirmação de deleção

### Subcomponentes

**StatCard**
```jsx
<StatCard
  title="Empresas Ativas"
  value={127}
  icon={Building2}
  color="bg-blue-500"
  subtitle="+5 este mês"
/>
```

**ModalMetrica**
- Abrir: `setIsMod

alOpen(true)`
- Campos: empresas_ativas, das_gerados_mes, taxa_conformidade, etc.
- Criar: POST para `/api/dashboard/metricas`
- Editar: PUT para `/api/dashboard/metricas/{id}`

**Histórico de Métricas**
- Lista todas as métricas com data/hora
- Botões Editar e Deletar
- Exibe: empresas_ativas, das_gerados_mes, taxa_conformidade

### Estado (useState)

```javascript
const [kpis, setKpis] = useState({...})           // KPIs principais
const [metricas, setMetricas] = useState([])      // Histórico
const [isModalOpen, setIsModalOpen] = useState()  // Modal aberto?
const [metricaEditando, setMetricaEditando] = useState()  // Qual editar?
const [isAlertOpen, setIsAlertOpen] = useState()  // Confirmar deleção?
const [loading, setLoading] = useState(true)     // Carregando?
```

### Fluxo de Dados

```
1. Página carrega → carregarDados()
   ├── GET /api/dashboard/overview → setKpis()
   └── GET /api/dashboard/metricas → setMetricas()

2. Usuário clica "Nova Métrica" → setIsModalOpen(true)
   ├── Modal abre com campo vazio
   └── Usuário preenche formulário

3. Usuário clica "Criar" → handleCriarMetrica()
   ├── POST /api/dashboard/metricas
   ├── Sucesso → carregarDados() (atualiza lista)
   └── Modal fecha

4. Usuário clica "Editar" em uma métrica → handleEditarMetrica()
   ├── setMetricaEditando(metrica)
   └── Modal abre com dados preenchidos

5. Usuário clica "Salvar" → handleCriarMetrica(dados, metricaId)
   ├── PUT /api/dashboard/metricas/{metricaId}
   ├── Sucesso → carregarDados()
   └── Modal fecha

6. Usuário clica "Deletar" → setIsAlertOpen(true)
   ├── Alert dialog abre
   └── Usuário confirma

7. Usuário confirma deleção → handleDeletarMetrica()
   ├── DELETE /api/dashboard/metricas/{metricaId}
   ├── Sucesso → carregarDados()
   └── Alert fecha
```

---

## 🚀 Como Usar

### Backend

**1. Registrar o router (já feito em `/api/__init__.py`)**
```python
from .dashboard import router as dashboard_router
api_router.include_router(dashboard_router)
```

**2. Iniciar servidor**
```bash
cd backend
python -m uvicorn main_enterprise:app --reload
```

**3. Testar endpoints**
```bash
# GET overview
curl http://localhost:8000/api/dashboard/overview

# POST criar métrica
curl -X POST http://localhost:8000/api/dashboard/metricas \
  -H "Content-Type: application/json" \
  -d '{"empresas_ativas": 100, "das_gerados_mes": 50}'

# GET metricas
curl http://localhost:8000/api/dashboard/metricas

# PUT atualizar
curl -X PUT http://localhost:8000/api/dashboard/metricas/{id} \
  -H "Content-Type: application/json" \
  -d '{"empresas_ativas": 120}'

# DELETE deletar
curl -X DELETE http://localhost:8000/api/dashboard/metricas/{id}
```

### Frontend

**1. Acessar Dashboard**
```
http://localhost:3000/dashboard
```

**2. Criar Nova Métrica**
- Clique em "+ Nova Métrica"
- Preencha os campos
- Clique em "Criar"

**3. Editar Métrica**
- Clique em "Editar" na linha da métrica
- Altere os valores
- Clique em "Atualizar"

**4. Deletar Métrica**
- Clique em "Deletar" na linha da métrica
- Confirme no dialog
- Métrica é deletada

**5. Atualizar Dashboard**
- Clique em "Atualizar" (botão refresh)
- KPIs e histórico são recarregados

---

## ✅ Testes

### Executar Testes

```bash
# Todos os testes
pytest tests/test_dashboard.py -v

# Testes específicos
pytest tests/test_dashboard.py::TestDashboardRepository -v

# Com output de print
pytest tests/test_dashboard.py -v -s

# Com cobertura
pytest tests/test_dashboard.py --cov=backend.services.dashboard --cov-report=html
```

### Testes Inclusos

**TestDashboardRepository**
- `test_criar_metrica` - ✅ Criar no MongoDB
- `test_obter_ultima_metrica` - ✅ Obter última métrica
- `test_atualizar_metrica` - ✅ Atualizar campos
- `test_deletar_metrica` - ✅ Soft delete
- `test_obter_por_periodo` - ✅ Período customizado

**TestDashboardService**
- `test_criar_metrica_via_servico` - ✅ Via serviço
- `test_registrar_atividade` - ✅ Registrar ação
- `test_calcular_kpis` - ✅ Cálculo de KPIs
- `test_calcular_proximos_vencimentos` - ✅ Vencimentos
- `test_gerar_dashboard_inicial` - ✅ Dashboard inicial

**TestDashboardCRUD**
- `test_crud_workflow` - ✅ Ciclo completo CREATE→READ→UPDATE→DELETE

**TestPersistencia**
- `test_dados_persistem_apos_atualizacao` - ✅ MongoDB persiste
- `test_snapshot_criado` - ✅ Snapshots para histórico

**TestDashboardAPI**
- `test_get_overview` - ✅ GET /overview
- `test_post_metrica` - ✅ POST criar
- `test_get_metricas` - ✅ GET listar
- `test_put_metrica` - ✅ PUT atualizar
- `test_delete_metrica` - ✅ DELETE

---

## 🐛 Troubleshooting

### Erro: "Conexão recusada ao MongoDB"
```
Solução:
1. Verificar se MongoDB está rodando
2. Verificar MONGO_URI em .env
3. Testar: mongosh mongodb://localhost:27017
```

### Erro: "404 Not Found" ao acessar /api/dashboard
```
Solução:
1. Verificar se router foi registrado em /api/__init__.py
2. Reiniciar backend
3. Verificar: GET http://localhost:8000/api/dashboard/overview
```

### Erro: "Modal não abre"
```
Solução:
1. Verificar se Dialog foi importado do @/components/ui/dialog
2. Verificar estado isModalOpen
3. Verificar se DialogTrigger está presente
```

### Erro: "Métrica não atualiza na lista"
```
Solução:
1. Verificar console do navegador (Network tab)
2. Verificar se response status é 200
3. Chamar carregarDados() após salvar
```

### Erro: "Dados não persistem após reload"
```
Solução:
1. Verificar MongoDB: é o banco certo?
2. Verificar se DashboardRepository.criar_metrica() é chamado
3. Verificar índices: db.dashboard_metrics.getIndexes()
```

---

## 📊 Fluxo de Dados Completo

```
┌─────────────────────────────────────────────────────┐
│                  Browser / React                     │
│                                                     │
│  Dashboard.jsx                                      │
│  ├── State: kpis, metricas, loading               │
│  ├── Método: carregarDados()                       │
│  └── Componentes: ModalMetrica, StatCard           │
└─────────────────────────────────────────────────────┘
         ▲                                     │
         │                                     │ HTTP
         │                                     ▼
┌────────┴─────────────────────────────────────────────┐
│                 FastAPI (Backend)                    │
│                                                     │
│  Routes: /api/dashboard/*                           │
│  ├── GET /overview                                  │
│  ├── GET /metricas                                  │
│  ├── POST /metricas                                 │
│  ├── PUT /metricas/{id}                             │
│  └── DELETE /metricas/{id}                          │
│                                                     │
│  Services/Dashboard: Lógica                         │
│  ├── criar_metrica()                                │
│  ├── atualizar_metrica()                            │
│  └── deletar_metrica()                              │
│                                                     │
│  Repository/Dashboard: CRUD                         │
│  └── Operações com MongoDB                          │
└────────┬─────────────────────────────────────────────┘
         │
         │ Motor (async)
         ▼
┌─────────────────────────────────────────────────────┐
│              MongoDB (Persistência)                  │
│                                                     │
│  Collection: dashboard_metrics                      │
│  ├── Índices: data_geracao, data_atualizacao      │
│  ├── Documentos: {...dados...}                      │
│  └── Soft delete: ativo = false                     │
│                                                     │
│  Collection: dashboard_snapshots                    │
│  └── Histórico para comparação                      │
└─────────────────────────────────────────────────────┘
```

---

## 🎓 Resumo de Funcionalidades

| Feature | Backend | Frontend | MongoDB | Status |
|---------|---------|----------|---------|--------|
| Criar métrica | ✅ POST | ✅ Modal + Form | ✅ Inserir | ✅ Completo |
| Listar métricas | ✅ GET paginado | ✅ Tabela | ✅ Query | ✅ Completo |
| Obter métrica | ✅ GET por ID | ✅ Modal editar | ✅ FindByID | ✅ Completo |
| Atualizar métrica | ✅ PUT | ✅ Modal editar | ✅ Update | ✅ Completo |
| Deletar métrica | ✅ DELETE soft | ✅ Botão | ✅ ativo=false | ✅ Completo |
| KPIs Overview | ✅ Agregação | ✅ StatCards | ✅ Cálculo | ✅ Completo |
| Próximos vencimentos | ✅ Cálculo | ✅ Lista | ✅ Embedded | ✅ Completo |
| Atividades recentes | ✅ Registro | ✅ Lista | ✅ Embedded | ✅ Completo |
| Snapshots histórico | ✅ Criar | ✅ - | ✅ Coleção | ✅ Completo |
| Comparação períodos | ✅ Agregação | ✅ - | ✅ Query | ✅ Completo |
| Testes unitários | ✅ 14+ testes | ⚠️ Jest (future) | ✅ Mocks | ✅ Completo |

---

## 📝 Notas Importantes

1. **Soft Delete**: Métricas não são deletadas, apenas marcadas como `ativo=false`
2. **Snapshots**: Criados automaticamente ao criar/atualizar métricas para histórico
3. **Paginação**: Métodos GET suportam `skip` e `limit` para grandes volumes
4. **Async**: Todas operações repository são async/await
5. **MongoDB**: Usa MongoEngine com índices para performance

---

## 🔮 Implementações Futuras

- [ ] Gráficos históricos (Chart.js / Recharts)
- [ ] Exportar dados (CSV / PDF)
- [ ] Alertas automáticos
- [ ] Webhooks para integração
- [ ] Dashboard por usuário/empresa
- [ ] Real-time updates (WebSocket)

---

**Versão**: 1.0.0  
**Data**: 15/02/2026  
**Status**: ✅ Produção Pronta
