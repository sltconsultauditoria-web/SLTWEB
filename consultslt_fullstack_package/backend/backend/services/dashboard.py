"""
Serviço para Dashboard - Lógica de negócio e cálculo de KPIs
"""
from datetime import datetime, timedelta
from typing import Optional, List, Dict, Any
from motor.motor_asyncio import AsyncIOMotorDatabase

from backend.repositories.dashboard import DashboardRepository
from backend.schemas.dashboard import DashboardMetricCreate, DashboardMetricUpdate


class DashboardService:
    """Serviço para operações com Dashboard e cálculo de métricas"""

    def __init__(self, db: AsyncIOMotorDatabase):
        self.db = db
        self.repository = DashboardRepository(db)

    async def calcular_kpis_atuais(self) -> Dict[str, Any]:
        """
        Calcula KPIs em tempo real consultando coleções do MongoDB
        """
        # Contagens principais
        empresas_ativas = await self.db["empresas"].count_documents({"status": "ativo"})
        empresas_inativas = await self.db["empresas"].count_documents({"status": "inativo"})
        das_gerados_mes = await self.db["obrigacoes"].count_documents({"tipo": "DAS"})
        certidoes_emitidas_mes = await self.db["certidoes"].count_documents({"status": "emitida"})
        alertas_criticos = await self.db["alertas"].count_documents({"tipo": "critico"})
        obrigacoes_pendentes = await self.db["obrigacoes"].count_documents({"status": "pendente"})

        # Receita e despesa podem vir de fiscal_data
        receita_bruta_mes = await self.db["fiscal_data"].aggregate([
            {"$group": {"_id": None, "total": {"$sum": "$receita"}}}
        ]).to_list(1)
        despesa_mensal = await self.db["fiscal_data"].aggregate([
            {"$group": {"_id": None, "total": {"$sum": "$despesa"}}}
        ]).to_list(1)

        receita_valor = receita_bruta_mes[0]["total"] if receita_bruta_mes else 0.0
        despesa_valor = despesa_mensal[0]["total"] if despesa_mensal else 0.0

        # Taxa de conformidade pode ser calculada como proporção de obrigações cumpridas
        total_obrigacoes = await self.db["obrigacoes"].count_documents({})
        cumpridas = await self.db["obrigacoes"].count_documents({"status": "cumprida"})
        taxa_conformidade = (cumpridas / total_obrigacoes * 100) if total_obrigacoes > 0 else 0.0

        return {
            "empresas_ativas": empresas_ativas,
            "empresas_inativas": empresas_inativas,
            "das_gerados_mes": das_gerados_mes,
            "certidoes_emitidas_mes": certidoes_emitidas_mes,
            "alertas_criticos": alertas_criticos,
            "taxa_conformidade": taxa_conformidade,
            "receita_bruta_mes": receita_valor,
            "despesa_mensal": despesa_valor,
            "obrigacoes_pendentes": obrigacoes_pendentes,
            "data_geracao": datetime.utcnow().isoformat()
        }

    async def calcular_proximos_vencimentos(self) -> List[Dict[str, Any]]:
        """
        Busca obrigações com data de vencimento futura
        """
        hoje = datetime.utcnow()
        cursor = self.db["obrigacoes"].find({"data_vencimento": {"$gte": hoje}}).sort("data_vencimento", 1).limit(5)
        proximos = []
        async for doc in cursor:
            dias_restantes = (doc["data_vencimento"] - hoje).days
            proximos.append({
                "empresa_id": str(doc.get("empresaId")),
                "empresa_nome": doc.get("empresa_nome", ""),
                "tipo": doc.get("tipo", ""),
                "data_vencimento": doc["data_vencimento"].isoformat(),
                "prioridade": doc.get("prioridade", "normal"),
                "dias_restantes": dias_restantes
            })
        return proximos

    async def gerar_dashboard_inicial(self) -> Dict[str, Any]:
        """
        Gera ou obtém dashboard inicial com KPIs
        """
        try:
            ultimas = await self.repository.obter_por_periodo(
                datetime.utcnow() - timedelta(hours=1),
                datetime.utcnow(),
                limit=1
            )
            if ultimas:
                return ultimas[0]

            kpis = await self.calcular_kpis_atuais()
            proximos = await self.calcular_proximos_vencimentos()

            dados = {
                **kpis,
                "proximos_vencimentos": proximos,
                "atividades_recentes": []
            }
            nova_metrica = await self.repository.criar_metrica(dados)
            return nova_metrica
        except Exception as e:
            print(f"Erro ao gerar dashboard inicial: {e}")
            return {}

    # Demais métodos (criar_metrica, obter_metricas, etc.) permanecem iguais
