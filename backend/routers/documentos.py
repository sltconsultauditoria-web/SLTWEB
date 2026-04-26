"""
Router de Documentos - /api/documentos
CRUD completo para documentos no MongoDB (consultslt_db.documentos)
"""
import logging
import uuid
import os
from datetime import datetime
from typing import List, Optional, Any
from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, Form
from fastapi.responses import FileResponse
from pydantic import BaseModel
from motor.motor_asyncio import AsyncIOMotorDatabase
from backend.core.database import get_db

logger = logging.getLogger(__name__)

router = APIRouter( tags=["Documentos"])

UPLOAD_DIR = os.getenv("UPLOAD_DIR", "/tmp/consultSLT_uploads")
os.makedirs(UPLOAD_DIR, exist_ok=True)


class DocumentoCreate(BaseModel):
    nome: Optional[str] = None
    tipo: Optional[str] = None
    empresa_id: Optional[str] = None
    cnpj: Optional[str] = None
    status: str = "pendente"
    dados: Optional[Any] = None


class DocumentoUpdate(BaseModel):
    nome: Optional[str] = None
    tipo: Optional[str] = None
    status: Optional[str] = None
    dados: Optional[Any] = None


class DocumentoResponse(BaseModel):
    id: str
    nome: Optional[str] = None
    tipo: Optional[str] = None
    empresa_id: Optional[str] = None
    cnpj: Optional[str] = None
    status: str = "pendente"
    file_path: Optional[str] = None
    dados: Optional[Any] = None
    ativo: bool = True
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True


def _s(doc):
    doc["id"] = str(doc.get("_id", doc.get("id", "")))
    doc.pop("_id", None)
    return doc


@router.get("/", response_model=List[DocumentoResponse])
async def listar_documentos(
    empresa_id: Optional[str] = None,
    status: Optional[str] = None,
    db: AsyncIOMotorDatabase = Depends(get_db)
):
    """Lista documentos com filtros."""
    filtro = {}
    if empresa_id:
        filtro["empresa_id"] = empresa_id
    if status:
        filtro["status"] = status
    try:
        items = await db["documentos"].find(filtro).to_list(200)
        return [_s(i) for i in items]
    except Exception as e:
        logger.error(f"Erro ao listar documentos: {e}")
        raise HTTPException(status_code=500, detail="Erro interno ao listar documentos")


@router.post("/", response_model=DocumentoResponse, status_code=201)
async def criar_documento(
    item: DocumentoCreate,
    db: AsyncIOMotorDatabase = Depends(get_db)
):
    """Cria um novo documento."""
    doc = item.dict()
    doc["id"] = str(uuid.uuid4())
    doc["ativo"] = True
    doc["created_at"] = datetime.utcnow()
    doc["updated_at"] = None
    await db["documentos"].insert_one(doc)
    doc.pop("_id", None)
    return doc


@router.post("/upload", response_model=DocumentoResponse, status_code=201)
async def upload_documento(
    arquivo: UploadFile = File(...),
    empresa_id: Optional[str] = Form(default=None),
    tipo: Optional[str] = Form(default=None),
    db: AsyncIOMotorDatabase = Depends(get_db)
):
    """Faz upload de um documento."""
    doc_id = str(uuid.uuid4())
    filename = f"{doc_id}_{arquivo.filename}"
    file_path = os.path.join(UPLOAD_DIR, filename)

    try:
        content = await arquivo.read()
        with open(file_path, "wb") as f:
            f.write(content)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao salvar arquivo: {e}")

    doc = {
        "id": doc_id,
        "nome": arquivo.filename,
        "tipo": tipo or "outro",
        "empresa_id": empresa_id,
        "status": "processando",
        "file_path": file_path,
        "ativo": True,
        "created_at": datetime.utcnow(),
        "updated_at": None
    }
    await db["documentos"].insert_one(doc)
    doc.pop("_id", None)
    return doc


@router.get("/{item_id}", response_model=DocumentoResponse)
async def obter_documento(
    item_id: str,
    db: AsyncIOMotorDatabase = Depends(get_db)
):
    """Obtém documento por ID."""
    item = await db["documentos"].find_one({"id": item_id})
    if not item:
        raise HTTPException(status_code=404, detail="Documento nao encontrado")
    return _s(item)


@router.get("/{item_id}/download")
async def download_documento(
    item_id: str,
    db: AsyncIOMotorDatabase = Depends(get_db)
):
    """Faz download de um documento."""
    item = await db["documentos"].find_one({"id": item_id})
    if not item:
        raise HTTPException(status_code=404, detail="Documento nao encontrado")
    file_path = item.get("file_path")
    if not file_path or not os.path.exists(file_path):
        raise HTTPException(status_code=404, detail="Arquivo nao encontrado no servidor")
    return FileResponse(file_path, filename=os.path.basename(file_path))


@router.put("/{item_id}", response_model=DocumentoResponse)
async def atualizar_documento(
    item_id: str,
    item: DocumentoUpdate,
    db: AsyncIOMotorDatabase = Depends(get_db)
):
    """Atualiza um documento."""
    u = item.dict(exclude_unset=True)
    u["updated_at"] = datetime.utcnow()
    r = await db["documentos"].update_one({"id": item_id}, {"$set": u})
    if r.matched_count == 0:
        raise HTTPException(status_code=404, detail="Documento nao encontrado")
    return _s(await db["documentos"].find_one({"id": item_id}))


@router.delete("/{item_id}")
async def deletar_documento(
    item_id: str,
    db: AsyncIOMotorDatabase = Depends(get_db)
):
    """Remove um documento."""
    r = await db["documentos"].delete_one({"id": item_id})
    if r.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Documento nao encontrado")
    return {"success": True, "deleted": True}
