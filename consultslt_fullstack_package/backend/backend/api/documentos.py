"""
Endpoints para gestão de Documentos - Versão Final Corrigida
"""

from fastapi import APIRouter, UploadFile, File, Form, HTTPException, Depends, Query
from typing import Optional, List
from datetime import datetime
import logging
import os
import sys

# Adiciona o diretório atual ao path para garantir que 'schemas' seja encontrado
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(os.path.dirname(current_dir))
if parent_dir not in sys.path:
    sys.path.append(parent_dir)
backend_dir = os.path.dirname(current_dir)
if backend_dir not in sys.path:
    sys.path.append(backend_dir)

from motor.motor_asyncio import AsyncIOMotorClient

# Importação robusta
try:
    from backend.schemas.documento import (
        TipoDocumento, StatusDocumento, DocumentoResponse, 
        DocumentoListResponse, DocumentoProcessamentoResult
    )
    from backend.services.documento_service import DocumentoService
except ImportError:
    try:
        from backend.schemas.documento import (
            TipoDocumento, StatusDocumento, DocumentoResponse, 
            DocumentoListResponse, DocumentoProcessamentoResult
        )
        from backend.services.documento_service import DocumentoService
    except ImportError as e:
        print(f"Erro crítico de importação: {e}")
        raise

logger = logging.getLogger(__name__)

# O router DEVE ser definido aqui para que o api/__init__.py o encontre
router = APIRouter(prefix="/documentos", tags=["Documentos"])

def get_db():
    mongo_url = os.environ.get("MONGO_URL", "mongodb://127.0.0.1:27017")
    db_name = os.environ.get("DB_NAME", "consultslt_db")
    client = AsyncIOMotorClient(mongo_url)
    return client[db_name]

def get_documento_service(db=Depends(get_db)) -> DocumentoService:
    return DocumentoService(db)

@router.post("/upload", response_model=DocumentoResponse)
async def upload_documento(
    file: UploadFile = File(...),
    empresa_id: Optional[str] = Form(None),
    tipo: TipoDocumento = Form(TipoDocumento.OUTRO),
    processar: bool = Form(True),
    service: DocumentoService = Depends(get_documento_service)
):
    try:
        content = await file.read()
        return await service.upload_documento(
            filename=file.filename,
            content=content,
            content_type=file.content_type or "application/octet-stream",
            empresa_id=empresa_id,
            tipo=tipo,
            processar_automaticamente=processar
        )
    except Exception as e:
        logger.error(f"Erro no upload: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/", response_model=DocumentoListResponse)
async def listar_documentos(
    empresa_id: Optional[str] = Query(None),
    pagina: int = Query(1, ge=1),
    por_pagina: int = Query(20, ge=1),
    service: DocumentoService = Depends(get_documento_service)
):
    result = mongo_list_to_dict_list(await service.listar_documentos(empresa_id=empresa_id, pagina=pagina, por_pagina=por_pagina))
    return DocumentoListResponse(**result)