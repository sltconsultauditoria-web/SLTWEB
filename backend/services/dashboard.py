"""
Serviço de Dashboard - KPIs dinâmicos
"""

from datetime import datetime, timedelta
from typing import Dict, Any, List, Optional
from motor.motor_asyncio import AsyncIOMotorDatabase

from backend.repositories.dashboard import DashboardRepository


class DashboardService:
    def __init__(self, db: AsyncIOMotorDatabase):
        self.db = db
        self.repository = DashboardRepository(db)

    async def calcular_kpis_atuais(self) -> Dict[str, Any]:

        empresas_ativas = await self.db["empresas"].count_documents({"status": "ATIVA"})
        empresas_inativas = await self.db["empresas"].count_documents({"status": "INATIVA"})

        documentos_mes = await self.db["documentos"].count_documents({
            "data_criacao": {"$gte": datetime.utcnow() - timedelta(days=30)}
        })

        certidoes_mes = await self.db["certidoes"].count_documents({
            "data_emissao": {"$gte": datetime.utcnow() - timedelta(days=30)}
        })

        alertas_criticos = await self.db["alertas"].count_documents({
            "nivel": "CRITICO",
            "status": "ABERTO"
        })

        obrigacoes_pendentes = await self.db["obrigacoes"].count_documents({
            "status": "PENDENTE"
        })

        total_obrigacoes = await self.db["obrigacoes"].count_documents({})
        conformes = await self.db["obrigacoes"].count_documents({"status": "CONFORME"})

        taxa_conformidade = (conformes / total_obrigacoes * 100) if total_obrigacoes > 0 else 0.0

        receita = await self.db["faturamentos"].aggregate([
            {"$match": {"data": {"$gte": datetime.utcnow() - timedelta(days=30)}}},
            {"$group": {"_id": None, "total": {"$sum": "$valor"}}}
        ]).to_list(1)

        despesa = await self.db["despesas"].aggregate([
            {"$match": {"data": {"$gte": datetime.utcnow() - timedelta(days=30)}}},
            {"$group": {"_id": None, "total": {"$sum": "$valor"}}}
        ]).to_list(1)

        return {
            "empresas_ativas": empresas_ativas,
            "empresas_inativas": empresas_inativas,
            "documentos_mes": documentos_mes,
            "certidoes_emitidas_mes": certidoes_mes,
            "alertas_criticos": alertas_criticos,
            "obrigacoes_pendentes": obrigacoes_pendentes,
            "taxa_conformidade": round(taxa_conformidade, 2),
            "receita_bruta_mes": round(receita[0]["total"] if receita else 0.0, 2),
            "despesa_mensal": round(despesa[0]["total"] if despesa else 0.0, 2),
        }

    async def calcular_proximos_vencimentos(self) -> List[Dict[str, Any]]:
        hoje = datetime.utcnow()

        pipeline = [
            {"$match": {"data_vencimento": {"$gte": hoje}}},
            {"$sort": {"data_vencimento": 1}},
            {"$limit": 10},
            {
                "$project": {
                    "_id": 0,
                    "empresa_id": 1,
                    "empresa_nome": 1,
                    "tipo": 1,
                    "data_vencimento": 1,
                    "prioridade": 1,
                    "dias_restantes": {
                        "$ceil": {
                            "$divide": [
                                {"$subtract": ["$data_vencimento", hoje]},
                                1000 * 60 * 60 * 24
                            ]
                        }
                    }
                }
            }
        ]

        return await self.db["obrigacoes"].aggregate(pipeline).to_list(10)

    async def gerar_dashboard_inicial(self) -> Dict[str, Any]:
        try:
            kpis = await self.calcular_kpis_atuais()
            proximos = await self.calcular_proximos_vencimentos()

            dados = {
                **kpis,
                "proximos_vencimentos": proximos,
                "atividades_recentes": []
            }

            await self.repository.criar_metrica(dados)
            return dados

        except Exception as e:
            print(f"Erro ao gerar dashboard: {e}")
            return {}

    # ================= CRUD =================

    async def criar_metrica(self, dados: Dict[str, Any]):
        return await self.repository.criar_metrica(dados)

    async def obter_metricas(self, skip=0, limit=10):
        return await self.repository.obter_todas(skip, limit)

    async def obter_pela_id(self, metrica_id: str):
        return await self.repository.obter_por_id(metrica_id)

    async def atualizar_metrica(self, metrica_id: str, dados: Dict[str, Any]):
        return await self.repository.atualizar(metrica_id, dados)

    async def deletar_metrica(self, metrica_id: str):
        return await self.repository.deletar(metrica_id)

    async def obter_historico(self, dias=30):
        data_inicio = datetime.utcnow() - timedelta(days=dias)
        data_fim = datetime.utcnow()
        return await self.repository.obter_por_periodo(data_inicio, data_fim)