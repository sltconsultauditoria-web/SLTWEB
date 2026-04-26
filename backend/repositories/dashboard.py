"""
Repositório Dashboard - CRUD Motor (MongoDB)
Dinâmico e sem dados estáticos
"""

from typing import List, Optional, Dict, Any
from datetime import datetime
from bson import ObjectId
from motor.motor_asyncio import AsyncIOMotorDatabase
from pymongo import ReturnDocument
import json

from backend.models.dashboard import (
    serialize_metric,
    serialize_snapshot,
    DASHBOARD_COLLECTION,
    SNAPSHOT_COLLECTION
)


class DashboardRepository:
    """Repositório para dashboard com MongoDB (Motor)"""

    def __init__(self, db: AsyncIOMotorDatabase):
        self.db = db
        self.collection = self.db[DASHBOARD_COLLECTION]
        self.snapshot_collection = self.db[SNAPSHOT_COLLECTION]

    # ========================================
    # CRUD MÉTRICAS
    # ========================================
    async def criar_metrica(self, dados: dict) -> Dict[str, Any]:
        documento = {
            "empresas_ativas": dados.get("empresas_ativas", 0),
            "empresas_inativas": dados.get("empresas_inativas", 0),
            "das_gerados_mes": dados.get("das_gerados_mes", 0),
            "certidoes_emitidas_mes": dados.get("certidoes_emitidas_mes", 0),
            "alertas_criticos": dados.get("alertas_criticos", 0),
            "taxa_conformidade": dados.get("taxa_conformidade", 0.0),
            "receita_bruta_mes": dados.get("receita_bruta_mes", 0.0),
            "despesa_mensal": dados.get("despesa_mensal", 0.0),
            "obrigacoes_pendentes": dados.get("obrigacoes_pendentes", 0),
            "proximos_vencimentos": dados.get("proximos_vencimentos", []),
            "atividades_recentes": dados.get("atividades_recentes", []),
            "data_geracao": datetime.utcnow(),
            "data_atualizacao": datetime.utcnow(),
            "ativo": True
        }

        resultado = await self.collection.insert_one(documento)
        documento["_id"] = resultado.inserted_id
        return serialize_metric(documento)

    async def obter_todas(self, skip: int = 0, limit: int = 10) -> List[Dict[str, Any]]:
        cursor = self.collection.find({"ativo": True}).sort("data_geracao", -1).skip(skip).limit(limit)
        docs = await cursor.to_list(length=limit)
        return [serialize_metric(doc) for doc in docs]

    async def obter_por_id(self, id_str: str) -> Optional[Dict[str, Any]]:
        try:
            object_id = ObjectId(id_str)
        except Exception:
            return None

        doc = await self.collection.find_one({"_id": object_id, "ativo": True})
        return serialize_metric(doc) if doc else None

    async def atualizar(self, id_str: str, dados: dict) -> Optional[Dict[str, Any]]:
        try:
            object_id = ObjectId(id_str)
        except Exception:
            return None

        dados.pop("_id", None)
        dados.pop("data_geracao", None)
        dados["data_atualizacao"] = datetime.utcnow()

        resultado = await self.collection.find_one_and_update(
            {"_id": object_id, "ativo": True},
            {"$set": dados},
            return_document=ReturnDocument.AFTER
        )
        return serialize_metric(resultado) if resultado else None

    async def deletar(self, id_str: str) -> bool:
        try:
            object_id = ObjectId(id_str)
        except Exception:
            return False

        resultado = await self.collection.update_one(
            {"_id": object_id, "ativo": True},
            {"$set": {"ativo": False, "data_atualizacao": datetime.utcnow()}}
        )
        return resultado.modified_count > 0

    # ========================================
    # SNAPSHOTS
    # ========================================
    async def criar_snapshot(self, metrica_id: str, alteracoes: Optional[dict] = None) -> Dict[str, Any]:
        try:
            object_id = ObjectId(metrica_id)
        except Exception:
            raise ValueError("ID inválido")

        doc = await self.collection.find_one({"_id": object_id})
        if not doc:
            raise ValueError("Métrica não encontrada")

        snapshot = {
            "data_snapshot": datetime.utcnow(),
            "metricas_json": json.dumps(serialize_metric(doc), default=str),
            "alteracoes": json.dumps(alteracoes, default=str) if alteracoes else None,
            "criado_em": datetime.utcnow()
        }

        resultado = await self.snapshot_collection.insert_one(snapshot)
        snapshot["_id"] = resultado.inserted_id
        return serialize_snapshot(snapshot)

    async def obter_snapshots(self, limit: int = 10, skip: int = 0) -> List[Dict[str, Any]]:
        cursor = self.snapshot_collection.find({}).sort("criado_em", -1).skip(skip).limit(limit)
        docs = await cursor.to_list(length=limit)
        return [serialize_snapshot(doc) for doc in docs]

    # ========================================
    # AGREGADOS
    # ========================================
    async def contar_total(self) -> int:
        return await self.collection.count_documents({"ativo": True})

    async def obter_por_periodo(self, data_inicio: datetime, data_fim: datetime, limit: int = 100):
        cursor = self.collection.find({
            "ativo": True,
            "data_geracao": {"$gte": data_inicio, "$lte": data_fim}
        }).sort("data_geracao", -1).limit(limit)

        docs = await cursor.to_list(length=limit)
        return [serialize_metric(doc) for doc in docs]

    async def adicionar_atividade(self, id_str: str, atividade: dict):
        try:
            object_id = ObjectId(id_str)
        except Exception:
            return None

        atividade_doc = {
            "acao": atividade.get("acao"),
            "empresa_id": atividade.get("empresa_id"),
            "empresa_nome": atividade.get("empresa_nome"),
            "timestamp": datetime.utcnow(),
            "usuario_id": atividade.get("usuario_id"),
            "detalhes": atividade.get("detalhes")
        }

        resultado = await self.collection.find_one_and_update(
            {"_id": object_id, "ativo": True},
            {
                "$push": {
                    "atividades_recentes": {
                        "$each": [atividade_doc],
                        "$position": 0,
                        "$slice": 20
                    }
                },
                "$set": {"data_atualizacao": datetime.utcnow()}
            },
            return_document=ReturnDocument.AFTER
        )

        return serialize_metric(resultado) if resultado else None