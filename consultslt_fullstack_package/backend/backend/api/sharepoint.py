"""
Endpoints para integração SharePoint
Permite controle manual e monitoramento da integração
"""

from fastapi import APIRouter, HTTPException, BackgroundTasks
from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime
import logging
import os

from backend.services.sharepoint_service import SharePointService
from backend.services.entra_auth import get_access_token

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/sharepoint", tags=["SharePoint"])


class ListFilesRequest(BaseModel):
    """Request para listar arquivos"""
    empresa_id: Optional[str] = None
    limite: int = 100


class FileInfo(BaseModel):
    """Informações de arquivo do SharePoint"""
    id: str
    nome: str
    tamanho: int
    criado: datetime
    modificado: datetime
    url: str


@router.get("/status")
async def get_sharepoint_status():
    """
    Retorna status da integração SharePoint
    """
    try:
        token = await get_access_token()
        service = SharePointService(token)
        return {"configured": True, "site_url": service.site_url}
    except Exception as e:
        return {"configured": False, "message": str(e)}


@router.post("/recibos", response_model=List[FileInfo])
async def listar_recibos(request: ListFilesRequest):
    """
    Lista recibos disponíveis no SharePoint
    """
    try:
        token = await get_access_token()
        service = SharePointService(token)
        recibos = service.listar_recibos(empresa_id=request.empresa_id, limite=request.limite)

        return [
            FileInfo(
                id=f["id"],
                nome=f["nome"],
                tamanho=f["tamanho"],
                criado=f["criado"],
                modificado=f["modificado"],
                url=f["url"]
            )
            for f in recibos
        ]
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/recibos/{nome_arquivo}")
async def obter_metadados_recibo(nome_arquivo: str):
    """
    Obtém metadados de um recibo específico
    """
    try:
        token = await get_access_token()
        service = SharePointService(token)
        return service.obter_metadados_recibo(nome_arquivo)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/recibos/{nome_arquivo}/download")
async def baixar_recibo(nome_arquivo: str):
    """
    Baixa o conteúdo de um recibo
    """
    try:
        token = await get_access_token()
        service = SharePointService(token)
        return service.baixar_recibo(nome_arquivo)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/empresas")
async def listar_empresas():
    """
    Lista empresas disponíveis no SharePoint
    """
    try:
        token = await get_access_token()
        service = SharePointService(token)
        return service.listar_empresas()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/robots/ingestion/status")
async def get_ingestion_robot_status():
    """
    Retorna status do robô de ingestão
    """
    from motor.motor_asyncio import AsyncIOMotorClient
    from backend.robots.ingestion_robot import DocumentIngestionRobot

    mongo_url = os.environ.get("MONGO_URL")
    db_name = os.environ.get("DB_NAME", "consultslt_db")

    client = AsyncIOMotorClient(mongo_url)
    db = client[db_name]

    robot = DocumentIngestionRobot(db)
    status = await robot.get_status()
    client.close()

    return status


@router.post("/robots/ingestion/run")
async def run_ingestion_once(background_tasks: BackgroundTasks):
    """
    Executa o robô de ingestão uma vez (manualmente)
    """
    from motor.motor_asyncio import AsyncIOMotorClient
    from backend.robots.ingestion_robot import DocumentIngestionRobot

    mongo_url = os.environ.get("MONGO_URL")
    db_name = os.environ.get("DB_NAME", "consultslt_db")

    async def run_robot():
        client = AsyncIOMotorClient(mongo_url)
        db = client[db_name]
        robot = DocumentIngestionRobot(db)
        result = await robot.run_once()
        client.close()
        return result

    background_tasks.add_task(run_robot)

    return {
        "status": "started",
        "message": "Robô de ingestão iniciado em background"
    }
