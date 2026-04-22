from fastapi import APIRouter, HTTPException
from backend.core.database import get_db
from backend.schemas.dashboard_metrics_schema import Dashboard_metricsCreate, Dashboard_metricsUpdate, Dashboard_metricsSchema
from typing import List
from bson import ObjectId
from datetime import datetime

router = APIRouter(prefix="/api/dashboard_metrics", tags=["dashboard_metrics"])

db = get_db()

@router.get("/", response_model=dict)
async def get_dashboard_metrics():
    """Consolida dados reais para o Dashboard"""
    try:
        empresas_ativas = await db["empresas"].count_documents({"status": "ativa"})
        obrigacoes_pendentes = await db["obrigacoes"].count_documents({"status": "pendente"})
        proximas_obrigacoes = await db["obrigacoes"].find({
            "status": "pendente",
            "dataVencimento": {"$lte": datetime.utcnow()}
        }).to_list(10)
        certidoes_emitidas = await db["documentos"].count_documents({"tipo": "certidao"})
        alertas_criticos = await db["alertas"].count_documents({"nivel": "crítico", "status": "pendente"})
        atividades_recentes = await db["logs"].find().sort("createdAt", -1).limit(10).to_list(10)

        return {
            "empresas_ativas": empresas_ativas,
            "obrigacoes_pendentes": obrigacoes_pendentes,
            "proximas_obrigacoes": proximas_obrigacoes,
            "certidoes_emitidas": certidoes_emitidas,
            "alertas_criticos": alertas_criticos,
            "atividades_recentes": atividades_recentes
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/", response_model=Dashboard_metricsSchema)
async def create_item(item: Dashboard_metricsCreate):
    result = await db["dashboard_metrics"].insert_one(item.dict())
    item_dict = item.dict()
    item_dict["id"] = str(result.inserted_id)
    item_dict["ativo"] = True
    return item_dict

@router.get("/{item_id}", response_model=Dashboard_metricsSchema)
async def get_item(item_id: str):
    item = await db["dashboard_metrics"].find_one({"_id": ObjectId(item_id)})
    if not item:
        raise HTTPException(status_code=404, detail="Item não encontrado")
    item["id"] = str(item["_id"])
    return item

@router.put("/{item_id}", response_model=Dashboard_metricsSchema)
async def update_item(item_id: str, item: Dashboard_metricsUpdate):
    await db["dashboard_metrics"].update_one({"_id": ObjectId(item_id)}, {"$set": item.dict(exclude_unset=True)})
    updated = await db["dashboard_metrics"].find_one({"_id": ObjectId(item_id)})
    updated["id"] = str(updated["_id"])
    return updated

@router.delete("/{item_id}", response_model=dict)
async def delete_item(item_id: str):
    result = await db["dashboard_metrics"].delete_one({"_id": ObjectId(item_id)})
    return {"deleted": result.deleted_count}
