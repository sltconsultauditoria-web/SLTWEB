# 🔄 FLUXO DE DADOS - DASHBOARD COM KPIs

## Diagrama Completo de Arquitetura

```
┌─────────────────────────────────────────────────────────────────────────┐
│                         FRONTEND (React + TailwindCSS)                  │
│                                                                         │
│                    http://localhost:3000/dashboard                      │
│                                                                         │
│  ┌───────────────────────────────────────────────────────────────────┐ │
│  │                      Dashboard.jsx (846 linhas)                   │ │
│  │                                                                   │ │
│  │  State:                                                           │ │
│  │  ├─ kpis: {empresas_ativas, das_gerados_mes, ...}              │ │
│  │  ├─ metricas: Array<DashboardMetric>                           │ │
│  │  ├─ loading: boolean                                            │ │
│  │  ├─ isModalOpen: boolean                                        │ │
│  │  ├─ metricaEditando: DashboardMetric | null                    │ │
│  │  └─ isAlertOpen: boolean                                        │ │
│  │                                                                   │ │
│  │  Componentes:                                                    │ │
│  │  ├─ StatCard (8x) → exibe KPI com ícone                        │ │
│  │  ├─ ModalMetrica → cria/edita com 9 campos                     │ │
│  │  ├─ Histórico Tabela → editar/deletar por linha                │ │
│  │  ├─ Próximos Vencimentos → prioridades                         │ │
│  │  └─ Atividades Recentes → timeline                             │ │
│  │                                                                   │ │
│  │  Métodos:                                                        │ │
│  │  ├─ carregarDados() → GET /overview + /metricas                │ │
│  │  ├─ handleCriarMetrica() → POST ou PUT                         │ │
│  │  ├─ handleEditarMetrica() → abre modal                         │ │
│  │  ├─ handleDeletarMetrica() → DELETE                            │ │
│  │  └─ getPrioridadeColor() → cores por prioridade                │ │
│  └───────────────────────────────────────────────────────────────────┘ │
│                              ▲                                          │
│                              │ HTTP / Axios                            │
│                              │                                          │
└──────────────────────────────┼──────────────────────────────────────────┘
                               │
                    HTTP REST API Calls
                               │
                               ▼
┌─────────────────────────────────────────────────────────────────────────┐
│                    BACKEND (FastAPI + Python)                           │
│                                                                         │
│              http://localhost:8000/api/dashboard/*                      │
│              http://localhost:8000/docs (Swagger UI)                    │
│                                                                         │
│  ┌───────────────────────────────────────────────────────────────────┐ │
│  │              Routes / Endpoints (api/dashboard.py)                │ │
│  │                                                                   │ │
│  │  1. GET /overview                                                │ │
│  │     └─ Retorna DashboardOverview                                 │ │
│  │        ├─ empresas_ativas                                        │ │
│  │        ├─ das_gerados_mes                                        │ │
│  │        ├─ taxa_conformidade                                      │ │
│  │        └─ ... mais 5 campos                                      │ │
│  │                                                                   │ │
│  │  2. GET /metricas (paginado)                                     │ │
│  │     └─ Retorna [DashboardMetric] com skip/limit                │ │
│  │                                                                   │ │
│  │  3. POST /metricas                                               │ │
│  │     └─ Cria + Snapshot automático (201)                         │ │
│  │                                                                   │ │
│  │  4. GET /metricas/{id}                                           │ │
│  │     └─ Retorna DashboardMetric específica                       │ │
│  │                                                                   │ │
│  │  5. PUT /metricas/{id}                                           │ │
│  │     └─ Atualiza + Snapshot com alterações                       │ │
│  │                                                                   │ │
│  │  6. DELETE /metricas/{id}                                        │ │
│  │     └─ Soft delete: ativo = false (204)                         │ │
│  │                                                                   │ │
│  │  7. GET /historico?dias=N                                        │ │
│  │     └─ Histórico dos últimos N dias                             │ │
│  │                                                                   │ │
│  │  8. GET /comparacao?data_inicio1=...                             │ │
│  │     └─ Compara dois períodos                                     │ │
│  │                                                                   │ │
│  │  9. POST /registrar-atividade                                    │ │
│  │     └─ Registra ação recente                                     │ │
│  └───────────────────────────────────────────────────────────────────┘ │
│                              ▲                                          │
│                              │                                          │
│  ┌───────────────────────────┴──────────────────────────────────────┐ │
│  │   Services (services/dashboard.py)                               │ │
│  │                                                                   │ │
│  │   ├─ calcular_kpis_atuais()                                     │ │
│  │   ├─ calcular_proximos_vencimentos()                            │ │
│  │   ├─ registrar_atividade()                                      │ │
│  │   ├─ gerar_dashboard_inicial()                                  │ │
│  │   ├─ criar_metrica()                                            │ │
│  │   ├─ atualizar_metrica()                                        │ │
│  │   ├─ deletar_metrica()                                          │ │
│  │   └─ comparar_periodos()                                        │ │
│  └───────────────────────────────────────────────────────────────────┘ │
│                              ▲                                          │
│                              │                                          │
│  ┌───────────────────────────┴──────────────────────────────────────┐ │
│  │  Repositories (repositories/dashboard.py)                        │ │
│  │  [Data Access Object - CRUD Operations]                         │ │
│  │                                                                   │ │
│  │   ├─ criar_metrica(dados) ─────────────────────────┐           │ │
│  │   ├─ obter_par_id(id) ──────────────────────────┐  │           │ │
│  │   ├─ obter_ultima() ────────────────────────┐   │  │           │ │
│  │   ├─ obter_todas() ─────────────────────┐   │   │  │           │ │
│  │   ├─ obter_por_periodo(dt1, dt2) ────┐  │   │   │  │           │ │
│  │   ├─ atualizar(id, dados) ─────────┐  │  │   │   │  │           │ │
│  │   ├─ deletar(id) ───────────────┐   │  │  │   │   │  │           │ │
│  │   ├─ adicionar_vencimento() ──┐  │   │  │  │   │   │  │           │ │
│  │   ├─ adicionar_atividade() ──┐ │   │  │  │   │   │  │           │ │
│  │   ├─ criar_snapshot() ────────┘ │   │  │  │   │   │  │           │ │
│  │   └─ obter_snapshots() ─────────┘   │  │  │   │   │  │           │ │
│  │                                      │  │  │   │   │  │           │ │
│  │       All methods async/await ◄──────┴──┴──┴───┴───┴──┘           │ │
│  └───────────────────────────────────────────────────────────────────┘ │
│                              ▲                                          │
│                              │ MongoEngine                             │
│                              │ (Async Motor driver)                    │
└──────────────────────────────┼──────────────────────────────────────────┘
                               │
                    MongoDB Database Queries
                               │
                               ▼
┌─────────────────────────────────────────────────────────────────────────┐
│                      MONGODB (Persistência)                             │
│                                                                         │
│                    mongodb://localhost:27017                            │
│                                                                         │
│  Database: consultslt (ou conforme .env)                              │
│                                                                         │
│  ┌───────────────────────────────────────────────────────────────────┐ │
│  │  Coleção: dashboard_metrics                                       │ │
│  │  ├─ Índices:                                                      │ │
│  │  │  ├─ data_geracao                                              │ │
│  │  │  ├─ data_atualizacao                                          │ │
│  │  │  ├─ ativo (para filtrar soft-delete)                         │ │
│  │  │  └─ -data_geracao (descendente, mais recentes primeiro)       │ │
│  │  │                                                               │ │
│  │  └─ Documentos:                                                  │ │
│  │     {                                                            │ │
│  │       "_id": ObjectId("507f..."),                               │ │
│  │       "empresas_ativas": 127,                                   │ │
│  │       "empresas_inativas": 12,                                  │ │
│  │       "das_gerados_mes": 98,                                    │ │
│  │       "certidoes_emitidas_mes": 245,                            │ │
│  │       "alertas_criticos": 3,                                    │ │
│  │       "taxa_conformidade": 94.5,                                │ │
│  │       "receita_bruta_mes": 458000.0,                            │ │
│  │       "despesa_mensal": 125000.0,                               │ │
│  │       "obrigacoes_pendentes": 42,                               │ │
│  │       "proximos_vencimentos": [                                 │ │
│  │         {                                                       │ │
│  │           "empresa_id": "emp_001",                              │ │
│  │           "empresa_nome": "EMPRESA X",                          │ │
│  │           "tipo": "DAS 01/2025",                                │ │
│  │           "data_vencimento": ISODate("..."),                    │ │
│  │           "prioridade": "critica",                              │ │
│  │           "dias_restantes": 5                                   │ │
│  │         }                                                       │ │
│  │       ],                                                        │ │
│  │       "atividades_recentes": [                                  │ │
│  │         {                                                       │ │
│  │           "acao": "DAS gerado",                                 │ │
│  │           "empresa_id": "emp_001",                              │ │
│  │           "timestamp": ISODate("..."),                          │ │
│  │           "usuario_id": "user_001"                              │ │
│  │         }                                                       │ │
│  │       ],                                                        │ │
│  │       "data_geracao": ISODate("2026-02-15T18:30:00Z"),         │ │
│  │       "data_atualizacao": ISODate("2026-02-15T19:00:00Z"),     │ │
│  │       "ativo": true                                             │ │
│  │     }                                                            │ │
│  └───────────────────────────────────────────────────────────────────┘ │
│                                                                         │
│  ┌───────────────────────────────────────────────────────────────────┐ │
│  │  Coleção: dashboard_snapshots (Histórico para auditoria)         │ │
│  │  ├─ Índices:                                                      │ │
│  │  │  ├─ data_snapshot                                             │ │
│  │  │  └─ -criado_em                                                │ │
│  │  │                                                               │ │
│  │  └─ Documentos:                                                  │ │
│  │     {                                                            │ │
│  │       "_id": ObjectId("..."),                                   │ │
│  │       "data_snapshot": ISODate("2026-02-15T18:30:00Z"),        │ │
│  │       "metricas_json": "{...}",                                 │ │
│  │       "alteracoes": "{\"das_gerados_mes\": {...}}",             │ │
│  │       "criado_em": ISODate("2026-02-15T18:30:00Z")             │ │
│  │     }                                                            │ │
│  └───────────────────────────────────────────────────────────────────┘ │
│                                                                         │
└─────────────────────────────────────────────────────────────────────────┘
```

---

## Fluxo de Requisição Detalhado

### 1. Usuário Carrega Dashboard

```
┌─ User acessa: http://localhost:3000/dashboard
│
├─ React monta Dashboard.jsx
│  └─ useEffect[] → chama carregarDados()
│
├─ Frontend HTTP GET /api/dashboard/overview
│  │
│  ├─ Backend recebe GET /overview
│  │  │
│  │  ├─ Route handler chama DashboardService.gerar_dashboard_inicial()
│  │  │
│  │  ├─ Service chama DashboardRepository.obter_ultima()
│  │  │
│  │  ├─ Repository faz query no MongoDB:
│  │  │  db.dashboard_metrics.find({ ativo: true })
│  │  │                       .sort({ data_geracao: -1 })
│  │  │                       .limit(1)
│  │  │
│  │  └─ MongoDB retorna último documento
│  │
│  ├─ Backend converte para DashboardOverview
│  │
│  └─ HTTP 200 com JSON
│
├─ Frontend Frontend HTTP GET /api/dashboard/metricas?skip=0&limit=10
│  │
│  ├─ Backend recebe GET /metricas
│  │  │
│  │  ├─ Service chama Repository.obter_todas()
│  │  │
│  │  ├─ Repository faz query:
│  │  │  db.dashboard_metrics.find({ ativo: true })
│  │  │                       .sort({ data_geracao: -1 })
│  │  │                       .skip(0)
│  │  │                       .limit(10)
│  │  │
│  │  └─ MongoDB retorna array com até 10 docs
│  │
│  ├─ Backend converte para [DashboardMetric]
│  │
│  └─ HTTP 200 com JSON Array
│
├─ Frontend recebe ambas respostas
│  │
│  ├─ setState(kpis) com overview
│  ├─ setState(metricas) com histórico
│  ├─ setState(loading, false)
│  │
│  └─ React re-renderiza Dashboard com dados
│
└─ User vê:
   ├─ 8 KPI Cards com dados atuais
   ├─ Tabela de histórico com até 10 registros
   ├─ Próximos vencimentos
   ├─ Atividades recentes
   └─ Botão "+ Nova Métrica"
```

### 2. Usuário Cria Nova Métrica

```
┌─ User clica "+ Nova Métrica"
│  └─ setIsModalOpen(true)
│     └─ ModalMetrica exibida
│
├─ User preenche formulário (9 campos)
│
├─ User clica "Criar"
│  │
│  ├─ Frontend valida dados
│  │  └─ OK: todos campos preenchidos
│  │
│  ├─ Frontend HTTP POST /api/dashboard/metricas
│  │  Body:
│  │  {
│  │    "empresas_ativas": 150,
│  │    "das_gerados_mes": 75,
│  │    "taxa_conformidade": 92.5,
│  │    ...
│  │  }
│  │
│  ├─ Backend recebe POST /metricas
│  │  │
│  │  ├─ Pydantic valida schema DashboardMetricCreate
│  │  │  └─ OK: tipos corretos
│  │  │
│  │  ├─ Service chama Repository.criar_metrica(dados)
│  │  │
│  │  ├─ Repository:
│  │  │  ├─ Cria documento DashboardMetric
│  │  │  ├─ Salva no MongoDB:
│  │  │  │  db.dashboard_metrics.insertOne({
│  │  │  │    empresas_ativas: 150,
│  │  │  │    das_gerados_mes: 75,
│  │  │  │    data_geracao: ISODate(),
│  │  │  │    data_atualizacao: ISODate(),
│  │  │  │    ativo: true
│  │  │  │  })
│  │  │  │
│  │  │  └─ Retorna documento com _id gerado
│  │  │
│  │  ├─ Service chama Repository.criar_snapshot(metrica_id)
│  │  │  └─ MongoDB:
│  │  │     db.dashboard_snapshots.insertOne({
│  │  │       data_snapshot: ISODate(),
│  │  │       metricas_json: "{...}",
│  │  │       criado_em: ISODate()
│  │  │     })
│  │  │
│  │  ├─ Backend converte para DashboardMetric
│  │  │
│  │  └─ HTTP 201 Created com JSON
│  │     {
│  │       "id": "507f1f77bcf86cd799439011",
│  │       "empresas_ativas": 150,
│  │       "data_geracao": "2026-02-15T18:30:00",
│  │       ...
│  │     }
│  │
│  ├─ Frontend recebe HTTP 201
│  │  │
│  │  ├─ Modal fecha: setIsModalOpen(false)
│  │  ├─ Chama carregarDados() para recarregar
│  │  │
│  │  ├─ GET /api/dashboard/overview (atualizado)
│  │  ├─ GET /api/dashboard/metricas (com novo registro)
│  │  │
│  │  └─ setState(metricas) com nova métrica no topo
│  │
│  └─ User vê:
│     ├─ Modal fecha
│     ├─ Tabela atualiza
│     ├─ Novo registro aparece no topo
│     └─ Feedback visual de sucesso
│
└─ ✅ Métrica criada e persistida!
```

### 3. Usuário Edita Métrica

```
┌─ User vê métrica na tabela
│  └─ Clica botão "Editar"
│
├─ Frontend:
│  ├─ setMetricaEditando(metrica) // metrica com todos dados
│  ├─ setIsModalOpen(true)
│  │
│  └─ ModalMetrica renderiza com dados preenchidos
│
├─ User altera alguns valores
│  └─ eg: das_gerados_mes: 75 → 85
│
├─ User clica "Atualizar"
│  │
│  ├─ Frontend HTTP PUT /api/dashboard/metricas/{metrica_id}
│  │  Body:
│  │  {
│  │    "das_gerados_mes": 85
│  │  }
│  │
│  ├─ Backend recebe PUT /metricas/{id}
│  │  │
│  │  ├─ Service chama Repository.obter_por_id(id)
│  │  │  └─ Salva estado anterior para comparação
│  │  │
│  │  ├─ Service chama Repository.atualizar(id, dados)
│  │  │
│  │  ├─ Repository:
│  │  │  ├─ MongoDB update:
│  │  │  │  db.dashboard_metrics.updateOne(
│  │  │  │    { _id: ObjectId(...) },
│  │  │  │    { $set: {
│  │  │  │      das_gerados_mes: 85,
│  │  │  │      data_atualizacao: ISODate()
│  │  │  │    }}
│  │  │  │  )
│  │  │  │
│  │  │  └─ Retorna documento atualizado
│  │  │
│  │  ├─ Repository.criar_snapshot(id, alteracoes)
│  │  │  └─ MongoDB snapshot com diff:
│  │  │     {
│  │  │       "das_gerados_mes": {
│  │  │         "anterior": 75,
│  │  │         "novo": 85
│  │  │       }
│  │  │     }
│  │  │
│  │  └─ HTTP 200 OK com documento atualizado
│  │
│  ├─ Frontend recebe HTTP 200
│  │  │
│  │  ├─ Modal fecha
│  │  ├─ Chama carregarDados()
│  │  │
│  │  └─ setState(metricas) com lista atualizada
│  │
│  └─ User vê:
│     ├─ Tabela atualiza
│     ├─ Novo valor exibido (85)
│     └─ data_atualizacao mostra agora
│
└─ ✅ Métrica atualizada com rastreamento via snapshot!
```

### 4. Usuário Deleta Métrica

```
┌─ User clica botão "Deletar" em uma linha
│  │
│  ├─ setMetricaParaDeletar(metrica)
│  ├─ setIsAlertOpen(true)
│  │
│  └─ AlertDialog aparece com confirmação
│
├─ User clica "Deletar" (confirma)
│  │
│  ├─ Frontend HTTP DELETE /api/dashboard/metricas/{metrica_id}
│  │
│  ├─ Backend recebe DELETE /metricas/{id}
│  │  │
│  │  ├─ Service chama Repository.deletar(id)
│  │  │
│  │  ├─ Repository:
│  │  │  ├─ MongoDB soft-delete:
│  │  │  │  db.dashboard_metrics.updateOne(
│  │  │  │    { _id: ObjectId(...) },
│  │  │  │    { $set: { ativo: false } }
│  │  │  │  )
│  │  │  │
│  │  │  └─ Retorna true (sucesso)
│  │  │
│  │  └─ HTTP 204 No Content
│  │     (Sem body - é delete bem-sucedido)
│  │
│  ├─ Frontend recebe HTTP 204
│  │  │
│  │  ├─ setIsAlertOpen(false) // fecha alert
│  │  ├─ Chama carregarDados()
│  │  │
│  │  └─ GET /api/dashboard/metricas
│  │     (só traz ativo=true, então deletada não aparece)
│  │
│  └─ setState(metricas) sem o registro deletado
│
└─ User vê:
   ├─ AlertDialog fecha
   ├─ Tabela recarrega
   ├─ Métrica desaparece da lista
   └─ ✅ Dados seguros no MongoDB (nunca foram deletados, apenas inativados!)
```

---

## Estrutura de Pastas e Fluxos

```
consultSLTweb/
│
├─ frontend/
│  └─ src/pages/
│     └─ Dashboard.jsx
│        ├─ [Carrega] → GET /overview + /metricas
│        ├─ [Cria] → POST /metricas
│        ├─ [Edita] → PUT /metricas/{id}
│        └─ [Deleta] → DELETE /metricas/{id}
│
└─ backend/
   ├─ api/
   │  ├─ dashboard.py
   │  │  ├─ GET /overview
   │  │  ├─ GET /metricas
   │  │  ├─ POST /metricas
   │  │  ├─ GET /metricas/{id}
   │  │  ├─ PUT /metricas/{id}
   │  │  ├─ DELETE /metricas/{id}
   │  │  ├─ GET /historico
   │  │  ├─ GET /comparacao
   │  │  └─ POST /registrar-atividade
   │  │
   │  └─ __init__.py (inclui router dashboard)
   │
   ├─ services/
   │  └─ dashboard.py
   │     ├─ criar_metrica()
   │     ├─ obter_metricas()
   │     ├─ atualizar_metrica()
   │     ├─ deletar_metrica()
   │     └─ ... mais 7 métodos
   │
   ├─ repositories/
   │  └─ dashboard.py
   │     ├─ criar_metrica() → MongoDB insert
   │     ├─ obter_todas() → MongoDB find
   │     ├─ obter_por_id() → MongoDB findOne
   │     ├─ obter_por_periodo() → MongoDB range query
   │     ├─ atualizar() → MongoDB updateOne
   │     ├─ deletar() → MongoDB soft-delete
   │     └─ criar_snapshot() → MongoDB insert (snapshots)
   │
   ├─ models/
   │  └─ dashboard.py
   │     ├─ DashboardMetric (MongoEngine Document)
   │     ├─ DashboardSnapshot
   │     ├─ ProximoVencimentoDoc (Embedded)
   │     └─ AtividadeRecenteDoc (Embedded)
   │
   └─ schemas/
      └─ dashboard.py
         ├─ DashboardMetricCreate (Request)
         ├─ DashboardMetricUpdate (Request)
         ├─ DashboardMetric (Response)
         ├─ DashboardOverview (Response)
         └─ Enums + Classes aninhadas

│
└─ MongoDB
   ├─ dashboard_metrics (collection)
   │  ├─ _id: ObjectId
   │  ├─ empresas_ativas: int
   │  ├─ ... 8 mais campos
   │  ├─ proximos_vencimentos: [Embedded]
   │  ├─ atividades_recentes: [Embedded]
   │  ├─ data_geracao: DateTime
   │  ├─ data_atualizacao: DateTime
   │  ├─ ativo: Boolean (para soft delete)
   │  │
   │  ├─ Índices:
   │  │  ├─ data_geracao
   │  │  ├─ data_atualizacao
   │  │  ├─ ativo
   │  │  └─ -data_geracao
   │  │
   │  └─ Documentos: ~10-100+
   │
   └─ dashboard_snapshots (collection)
      ├─ data_snapshot: DateTime
      ├─ metricas_json: String (JSON)
      ├─ alteracoes: String (Diff JSON)
      └─ criado_em: DateTime
```

---

**Fluxo Completo Implementado ✅**
