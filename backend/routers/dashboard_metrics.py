"""
Router de Dashboard - /api/dashboard_metrics
Metricas e KPIs do dashboard principal
"""
import logging
from datetime import datetime
from typing import List, Optional, Any
from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from motor.motor_asyncio import AsyncIOMotorDatabase
from backend.core.database import get_db

logger = logging.getLogger(__name__)

router = APIRouter( tags=["Dashboard"])


class DashboardOverview(BaseModel):
    total_empresas: int = 0
    empresas_ativas: int = 0
    empresas_inativas: int = 0
    obrigacoes_pendentes: int = 0
    alertas_criticos: int = 0
    certidoes_vencidas: int = 0
    guias_pendentes: int = 0
    debitos_em_aberto: int = 0
    ultima_atualizacao: Optional[datetime] = None


@router.get("/overview", response_model=DashboardOverview)
async def get_overview(db: AsyncIOMotorDatabase = Depends(get_db)):
    """Retorna overview do dashboard com KPIs principais."""
    try:
        total_empresas = await db["empresas"].count_documents({})
        empresas_ativas = await db["empresas"].count_documents({"ativo": True})
        obrigacoes_pendentes = await db["obrigacoes"].count_documents({"status": "pendente"})
        alertas_criticos = await db["alertas"].count_documents({"prioridade": "urgente", "status": "pendente"})
        certidoes_vencidas = await db["certidoes"].count_documents({"status": "vencida"})
        guias_pendentes = await db["guias"].count_documents({"status": "pendente"})
        debitos_em_aberto = await db["debitos"].count_documents({"status": "em_aberto"})

        return DashboardOverview(
            total_empresas=total_empresas,
            empresas_ativas=empresas_ativas,
            empresas_inativas=total_empresas - empresas_ativas,
            obrigacoes_pendentes=obrigacoes_pendentes,
            alertas_criticos=alertas_criticos,
            certidoes_vencidas=certidoes_vencidas,
            guias_pendentes=guias_pendentes,
            debitos_em_aberto=debitos_em_aberto,
            ultima_atualizacao=datetime.utcnow()
        )
    except Exception as e:
        logger.error(f"Erro ao gerar overview: {e}")
        raise HTTPException(status_code=500, detail=f"Erro ao gerar overview: {e}")


@router.get("/kpis")
async def get_kpis(db: AsyncIOMotorDatabase = Depends(get_db)):
    """Retorna KPIs para o dashboard."""
    try:
        total_empresas = await db["empresas"].count_documents({})
        empresas_ativas = await db["empresas"].count_documents({"ativo": True})
        obrigacoes_pendentes = await db["obrigacoes"].count_documents({"status": "pendente"})
        alertas_total = await db["alertas"].count_documents({})
        alertas_criticos = await db["alertas"].count_documents({"prioridade": "urgente", "status": "pendente"})

        return {
            "empresas": {"total": total_empresas, "ativas": empresas_ativas},
            "obrigacoes": {"pendentes": obrigacoes_pendentes},
            "alertas": {"total": alertas_total, "criticos": alertas_criticos},
            "atualizado_em": datetime.utcnow().isoformat()
        }
    except Exception as e:
        logger.error(f"Erro ao obter KPIs: {e}")
        raise HTTPException(status_code=500, detail=f"Erro ao obter KPIs: {e}")


@router.get("/metricas")
async def listar_metricas(db: AsyncIOMotorDatabase = Depends(get_db)):
    """Lista metricas salvas."""
    try:
        items = await db["dashboard_metrics"].find().to_list(100)
        for i in items:
            i["id"] = str(i.get("_id", i.get("id", "")))
            i.pop("_id", None)
        return items
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro: {e}")


@router.get("/proximos-vencimentos")
async def get_proximos_vencimentos(db: AsyncIOMotorDatabase = Depends(get_db)):
    """Retorna proximos vencimentos de obrigacoes e guias."""
    try:
        obrigacoes = await db["obrigacoes"].find(
            {"status": "pendente", "vencimento": {"$ne": None}}
        ).sort("vencimento", 1).limit(10).to_list(10)

        guias = await db["guias"].find(
            {"status": "pendente", "vencimento": {"$ne": None}}
        ).sort("vencimento", 1).limit(10).to_list(10)

        vencimentos = []
        for o in obrigacoes:
            o["id"] = str(o.get("_id", o.get("id", "")))
            o.pop("_id", None)
            o["origem"] = "obrigacao"
            vencimentos.append(o)

        for g in guias:
            g["id"] = str(g.get("_id", g.get("id", "")))
            g.pop("_id", None)
            g["origem"] = "guia"
            vencimentos.append(g)

        return {"vencimentos": vencimentos, "total": len(vencimentos)}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro: {e}")
