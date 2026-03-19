# 📚 EXEMPLOS PRÁTICOS - Dashboard com KPIs

## 1. Como Usar o Dashboard em Produção

### Cenário 1: Gerente visualiza KPIs diários

```
1. Manager acessa: http://localhost:3000/dashboard
2. Vê overview com 8 KPI cards atualizados
3. Clica "Atualizar" para recarregar dados
4. Observa histórico de métricas da última semana
```

### Cenário 2: Manager cria nova métrica mensal

```javascript
// FRONTEND (Manager clica "+ Nova Métrica")
1. Modal abre com 9 campos vazios
2. Preenche:
   - Empresas Ativas: 150
   - DAS Gerados: 85
   - Taxa Conformidade: 95.5
   - ... outros campos
3. Clica "Crear"

// BACKEND (API processa)
POST /api/dashboard/metricas
{
  "empresas_ativas": 150,
  "das_gerados_mes": 85,
  "taxa_conformidade": 95.5,
  ...
}
→ Response 201 Created com ID da métrica

// MONGODB (Persiste)
db.dashboard_metrics.insertOne({
  _id: ObjectId("507f1.."),
  empresas_ativas: 150,
  das_gerados_mes: 85,
  data_geracao: ISODate("2026-02-15T18:30:00"),
  ativo: true,
  ...
})

// FRONTEND (Sucesso)
Modal fecha
Tabela de histórico atualiza e exibe novo registro
```

### Cenário 3: Manager edita métrica anterior

```javascript
// FRONTEND
1. Vê métrica de ontem na tabela
2. Clica "Editar"
3. Modal abre com dados preenchidos
4. Altera: das_gerados_mes: 85 → 92
5. Clica "Atualizar"

// BACKEND (API processa)
PUT /api/dashboard/metricas/{metrica_id}
{
  "das_gerados_mes": 92
}

// MONGODB (Atualiza + Snapshot automático)
db.dashboard_metrics.updateOne(
  { _id: ObjectId("507f1..") },
  {
    $set: {
      das_gerados_mes: 92,
      data_atualizacao: ISODate("2026-02-15T19:00:00")
    }
  }
)

db.dashboard_snapshots.insertOne({
  data_snapshot: ISODate("2026-02-15T19:00:00"),
  metricas_json: "{ ... }",
  alteracoes: {
    "das_gerados_mes": {
      "anterior": 85,
      "novo": 92
    }
  }
})

// FRONTEND (Feedback visual)
Modal fecha
Histórico recarrega
Registro exibe valor atualizado (92)
```

### Cenário 4: Manager deleta métrica por erro

```javascript
// FRONTEND
1. Vê métrica criada erroneamente
2. Clica "Deletar"
3. AlertDialog abre: "Tem certeza?"
4. Clica "Deletar" para confirmar

// BACKEND (API soft-delete)
DELETE /api/dashboard/metricas/{metrica_id}

// MONGODB (Marca como inativo, não deleta)
db.dashboard_metrics.updateOne(
  { _id: ObjectId("507f1..") },
  { $set: { ativo: false } }
)

// FRONTEND (Desaparece da lista)
AlertDialog fecha
Tabela recarrega
Métrica não aparece mais (porque ativo=false)

// Dados seguros no banco para auditoria! ✅
```

---

## 2. Exemplos de Requisições CURL

### GET Overview
```bash
curl http://localhost:8000/api/dashboard/overview

# Response
{
  "total_empresas": 139,
  "empresas_ativas": 127,
  "das_gerados_mes": 98,
  "taxa_conformidade": 94.5,
  "ultima_atualizacao": "2026-02-15T18:30:00"
}
```

### POST Criar Métrica
```bash
curl -X POST http://localhost:8000/api/dashboard/metricas \
  -H "Content-Type: application/json" \
  -d '{
    "empresas_ativas": 120,
    "das_gerados_mes": 75,
    "certidoes_emitidas_mes": 150,
    "alertas_criticos": 5,
    "taxa_conformidade": 92.0,
    "receita_bruta_mes": 500000,
    "despesa_mensal": 100000,
    "obrigacoes_pendentes": 20
  }'

# Response 201
{
  "id": "507f1f77bcf86cd799439011",
  "empresas_ativas": 120,
  "das_gerados_mes": 75,
  "data_geracao": "2026-02-15T18:30:00",
  "ativo": true
}
```

### GET Listar com Paginação
```bash
curl "http://localhost:8000/api/dashboard/metricas?skip=0&limit=5"

# Response
[
  {
    "id": "507f...",
    "empresas_ativas": 120,
    "data_geracao": "2026-02-15T18:30:00"
  },
  {
    "id": "507f...",
    "empresas_ativas": 125,
    "data_geracao": "2026-02-14T18:30:00"
  },
  ...
]
```

### PUT Atualizar
```bash
curl -X PUT http://localhost:8000/api/dashboard/metricas/507f1f... \
  -H "Content-Type: application/json" \
  -d '{
    "empresas_ativas": 130,
    "taxa_conformidade": 94.5
  }'

# Response 200
{
  "id": "507f1f...",
  "empresas_ativas": 130,
  "taxa_conformidade": 94.5,
  "data_atualizacao": "2026-02-15T19:00:00"
}
```

### DELETE Soft Delete
```bash
curl -X DELETE http://localhost:8000/api/dashboard/metricas/507f1f...

# Response 204 No Content
```

### GET Histórico
```bash
curl "http://localhost:8000/api/dashboard/historico?dias=7"

# Response
[
  {
    "id": "507f...",
    "empresas_ativas": 130,
    "data_geracao": "2026-02-15T18:30:00"
  },
  {
    "id": "507f...",
    "empresas_ativas": 125,
    "data_geracao": "2026-02-14T18:30:00"
  },
  ...
]
```

### POST Registrar Atividade
```bash
curl -X POST "http://localhost:8000/api/dashboard/registrar-atividade?empresa_id=emp_001&empresa_nome=EMPRESA%20X&acao=DAS%20gerado&usuario_id=user_001"

# Response 200
{
  "mensagem": "Atividade registrada com sucesso"
}
```

---

## 3. Exemplos de Código Frontend

### Chamar API do Dashboard em outro componente

```javascript
// Em Empresas.jsx ou qualquer outro componente
import axios from 'axios';

const BACKEND_URL = process.env.REACT_APP_BACKEND_URL;
const API = `${BACKEND_URL}/api`;

// Registrar atividade quando cria empresa
const handleCriarEmpresa = async (dados) => {
  try {
    // 1. Cria empresa
    const response = await axios.post(`${API}/empresas`, dados);
    const empresa = response.data;
    
    // 2. Registra atividade no dashboard
    await axios.post(
      `${API}/dashboard/registrar-atividade?empresa_id=${empresa.id}&empresa_nome=${empresa.razao_social}&acao=Empresa%20criada`,
      {}
    );
    
    // 3. Exibe feedback
    alert('Empresa criada com sucesso!');
  } catch (error) {
    console.error('Erro:', error);
  }
};
```

### Obter KPIs atuais em outro componente

```javascript
// Em qualquer página que necessite KPIs
import { useEffect, useState } from 'react';
import axios from 'axios';

const MinhaComponent = () => {
  const [kpis, setKpis] = useState(null);

  useEffect(() => {
    axios.get(`${process.env.REACT_APP_BACKEND_URL}/api/dashboard/overview`)
      .then(res => setKpis(res.data))
      .catch(err => console.error(err));
  }, []);

  if (!kpis) return <div>Carregando...</div>;

  return (
    <div>
      <h2>Empresas Ativas: {kpis.empresas_ativas}</h2>
      <h2>Taxa Conformidade: {kpis.taxa_conformidade}%</h2>
    </div>
  );
};

export default MinhaComponent;
```

---

## 4. Exemplos de Código Backend

### Registrar atividades automaticamente

```python
# Em empresas.py ou qualquer rota
from backend.services.dashboard import DashboardService

@router.post("/empresas")
async def criar_empresa(dados: EmpresaCreate):
    # Cria empresa
    empresa = await EmpresaRepository.criar(dados)
    
    # Registra atividade no dashboard
    await DashboardService.registrar_atividade(
        empresa_id=str(empresa.id),
        empresa_nome=empresa.razao_social,
        acao="Empresa cadastrada",
        usuario_id=current_user.id if current_user else None,
        detalhes=f"CNPJ: {empresa.cnpj}"
    )
    
    return empresa
```

### Buscar métricas para relatório

```python
# Em relatórios.py
from backend.services.dashboard import DashboardService

@router.get("/relatorios/comparacao-mensal")
async def comparacao_mensal():
    from datetime import datetime, timedelta
    
    hoje = datetime.utcnow()
    
    # Mês atual
    mes_atual_inicio = hoje.replace(day=1, hour=0, minute=0, second=0)
    mes_atual_fim = hoje
    
    # Mês anterior
    primeiro_dia_mes_anterior = (mes_atual_inicio - timedelta(days=1)).replace(day=1)
    mes_anterior_fim = mes_atual_inicio - timedelta(seconds=1)
    
    # Compara períodos
    comparacao = await DashboardService.comparar_periodos(
        primeiro_dia_mes_anterior,
        mes_anterior_fim,
        mes_atual_inicio,
        mes_atual_fim
    )
    
    return comparacao
```

### Atualizar KPIs após operação

```python
# Em alertas.py ou qualquer rota
from backend.repositories.dashboard import DashboardRepository
from backend.services.dashboard import DashboardService

@router.post("/alertas")
async def criar_alerta(dados: AlertaCreate):
    # Cria alerta
    alerta = await AlertaRepository.criar(dados)
    
    # Atualiza dashboard com novo alerta
    ultima_metrica = await DashboardRepository.obter_ultima()
    if ultima_metrica:
        await DashboardRepository.atualizar(
            str(ultima_metrica.id),
            {'alertas_criticos': ultima_metrica.alertas_criticos + 1}
        )
    
    return alerta
```

---

## 5. Exemplo de Teste Completo

```python
# tests/test_dashboard_completo.py
import pytest
from fastapi.testclient import TestClient
from backend.main_enterprise import app
from backend.repositories.dashboard import DashboardRepository

@pytest.mark.asyncio
async def test_workflow_completo():
    """
    Testa workflow completo:
    1. Criar métrica
    2. Listar métrica
    3. Editar métrica
    4. Obter histórico
    5. Deletar métrica
    """
    
    client = TestClient(app)
    
    # 1. CREATE
    payload_criar = {
        "empresas_ativas": 100,
        "das_gerados_mes": 50,
        "taxa_conformidade": 90.0
    }
    resp_criar = client.post("/api/dashboard/metricas", json=payload_criar)
    assert resp_criar.status_code == 201
    metrica_id = resp_criar.json()["id"]
    print(f"✅ Métrica criada: {metrica_id}")
    
    # 2. READ
    resp_read = client.get(f"/api/dashboard/metricas/{metrica_id}")
    assert resp_read.status_code == 200
    assert resp_read.json()["empresas_ativas"] == 100
    print(f"✅ Métrica lida com sucesso")
    
    # 3. UPDATE
    payload_atualizar = {"empresas_ativas": 120}
    resp_update = client.put(f"/api/dashboard/metricas/{metrica_id}", json=payload_atualizar)
    assert resp_update.status_code == 200
    assert resp_update.json()["empresas_ativas"] == 120
    print(f"✅ Métrica atualizada: 100 → 120")
    
    # 4. HISTORY
    resp_history = client.get("/api/dashboard/historico?dias=1")
    assert resp_history.status_code == 200
    assert len(resp_history.json()) > 0
    print(f"✅ Histórico recuperado com {len(resp_history.json())} registros")
    
    # 5. DELETE
    resp_delete = client.delete(f"/api/dashboard/metricas/{metrica_id}")
    assert resp_delete.status_code == 204
    print(f"✅ Métrica deletada (soft delete)")
    
    # Verificar que não aparece mais
    resp_get = client.get(f"/api/dashboard/metricas/{metrica_id}")
    assert resp_get.status_code == 404
    print(f"✅ Métrica deletada não aparece mais")

if __name__ == "__main__":
    pytest.main([__file__, "-v", "-s"])
```

### Executar Teste
```bash
pytest tests/test_dashboard_completo.py -v -s

# Output
test_workflow_completo PASSED
✅ Métrica criada: 507f1f77bcf86cd799439011
✅ Métrica lida com sucesso
✅ Métrica atualizada: 100 → 120
✅ Histórico recuperado com 1 registros
✅ Métrica deletada (soft delete)
✅ Métrica deletada não aparece mais
```

---

## 6. Casos de Uso Reais

### Caso 1: Monitoramento Diário
```
09:00 - CFO acessa dashboard
        → Vê KPIs do dia anterior
        → Taxa conformidade: 94.5%
        → Clica "Atualizar" para dados atuais

10:00 - Sistema registra:
        ✓ DAS gerado (empresa 1)
        ✓ Certidão emitida (empresa 2)
        ✓ Alerta crítico (empresa 3)

11:00 - CFO clica "Atualizar"
        → KPIs atualizados
        → Atividades recentes mostram 3 ações
        → Histórico agora tem 2 métricas (atual + anterior)
```

### Caso 2: Auditoria
```
Auditor precisa verificar histórico de KPIs de Janeiro

1. Acessa: http://localhost:3000/dashboard
2. GET /api/dashboard/historico?dias=31
   → Retorna 31 snapshots de janeiro
3. Pode comparar:
   - Dia 1: 100 empresas ativas
   - Dia 15: 110 empresas ativas (+10%)
   - Dia 31: 115 empresas ativas (+15%)
4. Verifica alterações em cada snapshot
   → Rastreabilidade completa!
```

### Caso 3: Relatório Mensal
```
Manager precisa gerar relatório comparativo

1. Sistema calcula:
   - Janeiro: média 105 empresas, 92% conformidade
   - Fevereiro: média 115 empresas, 94% conformidade
   
2. GET /api/dashboard/comparacao
   → Diff: +10 empresas, +2% conformidade
   
3. Exporta para PDF/Excel
   → Relatório visual pronto!
```

---

## 7. Estrutura de Dados no MongoDB

### Exemplo de Documento Completo

```javascript
db.dashboard_metrics.findOne()

{
  "_id": ObjectId("507f1f77bcf86cd799439011"),
  "empresas_ativas": 127,
  "empresas_inativas": 12,
  "das_gerados_mes": 98,
  "certidoes_emitidas_mes": 245,
  "alertas_criticos": 3,
  "taxa_conformidade": 94.5,
  "receita_bruta_mes": 458000.0,
  "despesa_mensal": 125000.0,
  "obrigacoes_pendentes": 42,
  
  "proximos_vencimentos": [
    {
      "empresa_id": "emp_001",
      "empresa_nome": "TRES PINHEIROS LTDA",
      "tipo": "DAS 01/2025",
      "data_vencimento": ISODate("2026-02-20T00:00:00Z"),
      "prioridade": "critica",
      "dias_restantes": 5
    }
  ],
  
  "atividades_recentes": [
    {
      "acao": "DAS gerado",
      "empresa_id": "emp_001",
      "empresa_nome": "TRES PINHEIROS LTDA",
      "timestamp": ISODate("2026-02-15T18:30:00Z"),
      "usuario_id": "user_001",
      "detalhes": "{...}"
    }
  ],
  
  "data_geracao": ISODate("2026-02-15T18:30:00Z"),
  "data_atualizacao": ISODate("2026-02-15T18:30:00Z"),
  "ativo": true
}
```

---

**Fim dos Exemplos Práticos**

Para mais detalhes, consulte:
- `DASHBOARD_DOCUMENTACAO.md` - Documentação técnica
- `DASHBOARD_RESUMO_IMPLEMENTACAO.md` - Resumo geral
- `DASHBOARD_CHECKLIST.md` - Checklist de verificação
