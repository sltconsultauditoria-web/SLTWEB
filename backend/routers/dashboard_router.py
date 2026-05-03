from datetime import datetime, timedelta

from fastapi import APIRouter

from backend.core.database import get_db


router = APIRouter(prefix="/dashboard", tags=["dashboard"])
db = get_db()


@router.get("/")
async def dashboard():
    hoje = datetime.utcnow()
    empresas_ativas = await db["empresas"].count_documents({"ativo": {"$ne": False}})
    alertas_abertos = await db["alertas"].count_documents({"ativo": {"$ne": False}})
    documentos = await db["documentos"].count_documents({"ativo": {"$ne": False}})
    obrigacoes = await db["obrigacoes"].count_documents({"ativo": {"$ne": False}})
    proximos = await db["obrigacoes"].find({
        "ativo": {"$ne": False},
        "$or": [
            {"data_vencimento": {"$gte": hoje.isoformat(), "$lte": (hoje + timedelta(days=30)).isoformat()}},
            {"dataVencimento": {"$gte": hoje, "$lte": hoje + timedelta(days=30)}},
        ],
    }).limit(10).to_list(10)

    return {
        "empresas_ativas": empresas_ativas,
        "alertas_abertos": alertas_abertos,
        "documentos": documentos,
        "obrigacoes": obrigacoes,
        "proximos_vencimentos": [
            {**{k: v for k, v in item.items() if k != "_id"}, "id": str(item.get("_id"))}
            for item in proximos
        ],
    }
