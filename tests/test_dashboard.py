"""
Testes para Dashboard e KPIs
Valida CRUD completo e persistência
"""
import pytest
import asyncio
from datetime import datetime, timedelta
from backend.repositories.dashboard import DashboardRepository
from backend.services.dashboard import DashboardService
from backend.schemas.dashboard import DashboardMetricCreate, DashboardMetricUpdate


class TestDashboardRepository:
    """Testes do repositório de Dashboard"""

    @pytest.mark.asyncio
    async def test_criar_metrica(self):
        """Testa criação de métrica"""
        dados = {
            'empresas_ativas': 100,
            'empresas_inativas': 10,
            'das_gerados_mes': 50,
            'certidoes_emitidas_mes': 75,
            'alertas_criticos': 5,
            'taxa_conformidade': 90.5,
            'receita_bruta_mes': 100000.0,
            'despesa_mensal': 25000.0,
            'obrigacoes_pendentes': 10,
        }
        
        metrica = await DashboardRepository.criar_metrica(dados)
        assert metrica is not None
        assert metrica.empresas_ativas == 100
        assert metrica.das_gerados_mes == 50

    @pytest.mark.asyncio
    async def test_obter_ultima_metrica(self):
        """Testa obtenção da última métrica"""
        # Criar uma métrica
        dados = {
            'empresas_ativas': 150,
            'das_gerados_mes': 80
        }
        metrica_criada = await DashboardRepository.criar_metrica(dados)
        
        # Obter a última
        ultima = await DashboardRepository.obter_ultima()
        assert ultima is not None
        assert str(ultima.id) == str(metrica_criada.id)

    @pytest.mark.asyncio
    async def test_atualizar_metrica(self):
        """Testa atualização de métrica"""
        # Criar
        dados = {'empresas_ativas': 50}
        metrica = await DashboardRepository.criar_metrica(dados)
        metrica_id = str(metrica.id)
        
        # Atualizar
        dados_atualizacao = {'empresas_ativas': 75}
        atualizada = await DashboardRepository.atualizar(metrica_id, dados_atualizacao)
        
        assert atualizada.empresas_ativas == 75

    @pytest.mark.asyncio
    async def test_deletar_metrica(self):
        """Testa deleção (soft delete) de métrica"""
        # Criar
        dados = {'empresas_ativas': 60}
        metrica = await DashboardRepository.criar_metrica(dados)
        metrica_id = str(metrica.id)
        
        # Deletar
        sucesso = await DashboardRepository.deletar(metrica_id)
        assert sucesso is True
        
        # Verificar que fica marcada como inativa
        obtida = await DashboardRepository.obter_por_id(metrica_id)
        assert obtida is None  # Pois retorna apenas ativas

    @pytest.mark.asyncio
    async def test_obter_por_periodo(self):
        """Testa obtenção de métricas por período"""
        hoje = datetime.utcnow()
        ontem = hoje - timedelta(days=1)
        amanha = hoje + timedelta(days=1)
        
        # Criar métrica
        dados = {'empresas_ativas': 90}
        await DashboardRepository.criar_metrica(dados)
        
        # Obter do período
        metricas = await DashboardRepository.obter_por_periodo(ontem, amanha)
        assert len(metricas) > 0


class TestDashboardService:
    """Testes do serviço de Dashboard"""

    @pytest.mark.asyncio
    async def test_criar_metrica_via_servico(self):
        """Testa criação via serviço"""
        dados = DashboardMetricCreate(
            empresas_ativas=120,
            das_gerados_mes=60,
            certificacoes_emitidas_mes=90,
            taxa_conformidade=92.3
        )
        
        metrica = await DashboardService.criar_metrica(dados)
        assert metrica is not None
        assert metrica['empresas_ativas'] == 120

    @pytest.mark.asyncio
    async def test_registrar_atividade(self):
        """Testa registro de atividade"""
        # Criar uma métrica primeiro
        dados = {'empresas_ativas': 100}
        await DashboardRepository.criar_metrica(dados)
        
        # Registrar atividade
        await DashboardService.registrar_atividade(
            empresa_id='emp_001',
            empresa_nome='Empresa X',
            acao='DAS gerado',
            usuario_id='user_001',
            detalhes='DAS mês 01/2025'
        )
        
        # Verificar que foi registrada
        ultima = await DashboardRepository.obter_ultima()
        assert len(ultima.atividades_recentes) > 0

    @pytest.mark.asyncio
    async def test_calcular_kpis(self):
        """Testa cálculo de KPIs"""
        kpis = await DashboardService.calcular_kpis_atuais()
        assert kpis['empresas_ativas'] > 0
        assert 'taxa_conformidade' in kpis

    @pytest.mark.asyncio
    async def test_calcular_proximos_vencimentos(self):
        """Testa cálculo de próximos vencimentos"""
        vencimentos = await DashboardService.calcular_proximos_vencimentos()
        assert len(vencimentos) > 0
        assert 'empresa_nome' in vencimentos[0]
        assert 'data_vencimento' in vencimentos[0]

    @pytest.mark.asyncio
    async def test_gerar_dashboard_inicial(self):
        """Testa geração do dashboard inicial"""
        dashboard = await DashboardService.gerar_dashboard_inicial()
        assert dashboard is not None
        assert 'empresas_ativas' in dashboard
        assert 'proximos_vencimentos' in dashboard


class TestDashboardCRUD:
    """Testes de CRUD completo"""

    @pytest.mark.asyncio
    async def test_crud_workflow(self):
        """Testa workflow completo: Create -> Read -> Update -> Delete"""
        
        # CREATE
        dados_criar = {
            'empresas_ativas': 110,
            'empresas_inativas': 5,
            'das_gerados_mes': 55,
            'certidoes_emitidas_mes': 85,
            'alertas_criticos': 2,
            'taxa_conformidade': 95.0,
            'receita_bruta_mes': 150000.0,
            'despesa_mensal': 40000.0,
            'obrigacoes_pendentes': 8
        }
        metrica = await DashboardRepository.criar_metrica(dados_criar)
        metrica_id = str(metrica.id)
        
        assert metrica.empresas_ativas == 110
        
        # READ
        obtida = await DashboardRepository.obter_por_id(metrica_id)
        assert obtida is not None
        assert obtida.das_gerados_mes == 55
        
        # UPDATE
        dados_atualizacao = {
            'empresas_ativas': 125,
            'das_gerados_mes': 70
        }
        atualizada = await DashboardRepository.atualizar(metrica_id, dados_atualizacao)
        assert atualizada.empresas_ativas == 125
        assert atualizada.das_gerados_mes == 70
        
        # DELETE
        sucesso = await DashboardRepository.deletar(metrica_id)
        assert sucesso is True


class TestPersistencia:
    """Testes de persistência em MongoDB"""

    @pytest.mark.asyncio
    async def test_dados_persistem_apos_atualizacao(self):
        """Verifica que dados persistem após atualização"""
        # Criar
        dados = {'empresas_ativas': 200, 'das_gerados_mes': 100}
        metrica = await DashboardRepository.criar_metrica(dados)
        metrica_id = str(metrica.id)
        
        # Atualizar
        await DashboardRepository.atualizar(metrica_id, {'receita_bruta_mes': 500000.0})
        
        # Obter novamente
        renovada = await DashboardRepository.obter_por_id(metrica_id)
        
        # Verificar persistência
        assert renovada.empresas_ativas == 200  # valor original mantido
        assert renovada.receita_bruta_mes == 500000.0  # novo valor

    @pytest.mark.asyncio
    async def test_snapshot_criado(self):
        """Verifica criação de snapshots para histórico"""
        # Criar métrica
        dados = {'empresas_ativas': 180}
        metrica = await DashboardRepository.criar_metrica(dados)
        
        # Obter snapshots
        snapshots = await DashboardRepository.obter_snapshots(limit=10)
        assert len(snapshots) > 0


# ===============================
# INTEGRAÇÃO COM API
# ===============================
class TestDashboardAPI:
    """Testes de integração com API FastAPI"""

    @pytest.fixture
    def client(self):
        """Cria cliente HTTP para testes"""
        from fastapi.testclient import TestClient
        from backend.main_enterprise import app
        return TestClient(app)

    def test_get_overview(self, client):
        """Testa GET /api/dashboard/overview"""
        response = client.get("/api/dashboard/overview")
        assert response.status_code == 200
        data = response.json()
        assert 'empresas_ativas' in data
        assert 'taxa_conformidade' in data

    def test_post_metrica(self, client):
        """Testa POST /api/dashboard/metricas"""
        payload = {
            'empresas_ativas': 130,
            'das_gerados_mes': 65,
            'certidoes_emitidas_mes': 100,
            'taxa_conformidade': 93.5
        }
        response = client.post("/api/dashboard/metricas", json=payload)
        assert response.status_code == 201
        data = response.json()
        assert data['empresas_ativas'] == 130

    def test_get_metricas(self, client):
        """Testa GET /api/dashboard/metricas"""
        response = client.get("/api/dashboard/metricas")
        assert response.status_code == 200
        assert isinstance(response.json(), list)

    def test_put_metrica(self, client):
        """Testa PUT /api/dashboard/metricas/{id}"""
        # Criar primeiro
        payload_criar = {'empresas_ativas': 140}
        resp_criar = client.post("/api/dashboard/metricas", json=payload_criar)
        metrica_id = resp_criar.json()['id']
        
        # Atualizar
        payload_atualizar = {'empresas_ativas': 155}
        response = client.put(f"/api/dashboard/metricas/{metrica_id}", json=payload_atualizar)
        assert response.status_code == 200
        assert response.json()['empresas_ativas'] == 155

    def test_delete_metrica(self, client):
        """Testa DELETE /api/dashboard/metricas/{id}"""
        # Criar primeiro
        payload = {'empresas_ativas': 145}
        resp_criar = client.post("/api/dashboard/metricas", json=payload)
        metrica_id = resp_criar.json()['id']
        
        # Deletar
        response = client.delete(f"/api/dashboard/metricas/{metrica_id}")
        assert response.status_code == 204


if __name__ == '__main__':
    pytest.main([__file__, '-v', '-s'])
