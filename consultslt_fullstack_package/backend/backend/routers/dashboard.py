
from fastapi import APIRouter
# from database import db

router = APIRouter(prefix="/api/dashboard", tags=["dashboard"])

@router.get("/")
async def dashboard():
    pass
from database import db

    empresas = db.empresas.count_documents({})
    alertas = db.alertas.count_documents({"lido":False})
    obrigacoes = db.obrigacoes_empresa.count_documents({"status":"pendente"})

    return {
        "empresas": empresas,
        "alertas": alertas,
        "obrigacoes_pendentes": obrigacoes
    }
