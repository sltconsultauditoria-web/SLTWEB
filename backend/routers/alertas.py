from fastapi import APIRouter, HTTPException, Depends
from backend.core.database import get_db
from backend.schemas.alertas_schema import AlertasCreate, AlertasUpdate, AlertasSchema
from typing import List
from bson import ObjectId

router = APIRouter(prefix="/api/alertas", tags=["alertas"])

async def get_db_dependency():
    return get_db()

def _normalize_priority(value):
    raw = str(value or "").strip().lower()
    mapping = {
        "crítico": "critica",
        "critico": "critica",
        "critical": "critica",
        "alta": "alta",
        "high": "alta",
        "media": "media",
        "média": "media",
        "medium": "media",
        "baixa": "baixa",
        "low": "baixa",
    }
    return mapping.get(raw, raw or "media")


def _normalize_status(value):
    raw = str(value or "").strip().lower()
    mapping = {
        "lido": "lido",
        "read": "lido",
        "resolvido": "resolvido",
        "resolved": "resolvido",
        "arquivado": "arquivado",
        "archived": "arquivado",
        "pendente": "pendente",
        "pending": "pendente",
    }
    return mapping.get(raw, raw or "pendente")


def _normalize_alert(item):
    payload = item.get("data") if isinstance(item.get("data"), dict) else {}
    prioridade = _normalize_priority(item.get("prioridade") or payload.get("prioridade") or item.get("nivel") or payload.get("nivel"))
    status = _normalize_status(item.get("status") or payload.get("status") or ("resolvido" if item.get("resolvido") or payload.get("resolvido") else "pendente"))
    resolved = bool(item.get("resolvido") or payload.get("resolvido") or status in {"resolvido", "arquivado"})
    read = bool(item.get("lido") or payload.get("lido") or status == "lido")
    created_at = item.get("created_at") or payload.get("created_at") or item.get("createdAt") or payload.get("createdAt") or item.get("timestamp") or payload.get("timestamp")

    return {
        **item,
        "id": str(item.get("_id") or item.get("id") or ""),
        "titulo": item.get("titulo") or payload.get("titulo") or item.get("mensagem") or payload.get("mensagem") or "Alerta",
        "descricao": item.get("descricao") or payload.get("descricao") or item.get("mensagem") or payload.get("mensagem") or "",
        "prioridade": prioridade,
        "status": status,
        "lido": read,
        "resolvido": resolved,
        "data": created_at,
        "payload": payload,
    }


@router.get("/")
async def list_items(db=Depends(get_db_dependency)):
    items = await db["alertas"].find().to_list(100)
    return [_normalize_alert(item) for item in items]

@router.post("/", response_model=AlertasSchema)
async def create_item(item: AlertasCreate, db=Depends(get_db_dependency)):
    result = await db["alertas"].insert_one(item.dict())
    item_dict = item.dict()
    item_dict["id"] = str(result.inserted_id)
    item_dict["ativo"] = True
    return item_dict
