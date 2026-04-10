"""Endpoints para gestão de Alertas"""

from fastapi import APIRouter, HTTPException, Depends, Query
from backend.db.utils import mongo_list_to_dict_list
from typing import Optional, List
import logging
import os
from motor.motor_asyncio import AsyncIOMotorClient
from datetime import datetime
import uuid

from backend.schemas.alerta import (
    AlertaCreate,
    AlertaUpdate,
    AlertaResponse,
    AlertaListResponse,
    TipoAlerta,
    StatusAlerta,
    PrioridadeAlerta
)

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/alertas", tags=["Alertas"])

def get_db():
    """Dependência para obter conexão com MongoDB."""
    mongo_url = os.environ.get("MONGO_URL")
    db_name = os.environ.get("DB_NAME", "consultslt")
    client = AsyncIOMotorClient(mongo_url)
    return client[db_name]

@router.post("/", response_model=AlertaResponse, status_code=201)
async def criar_alerta(dados: AlertaCreate, db=Depends(get_db)):
    """Cria um novo alerta no sistema."""
    alerta_dict = dados.model_dump()
    alerta_dict["id"] = str(uuid.uuid4())
    alerta_dict["status"] = StatusAlerta.PENDENTE
    alerta_dict["created_at"] = datetime.utcnow()
    alerta_dict["updated_at"] = datetime.utcnow()
    
    await db.alertas.insert_one(alerta_dict)
    return AlertaResponse(**alerta_dict)

@router.get("/", response_model=List[AlertaResponse])
async def listar_alertas(
    tipo: Optional[TipoAlerta] = Query(default=None),
    status: Optional[StatusAlerta] = Query(default=None),
    prioridade: Optional[PrioridadeAlerta] = Query(default=None),
    empresa_id: Optional[str] = Query(default=None),
    pagina: int = Query(default=1, ge=1),
    por_pagina: int = Query(default=20, ge=1, le=100),
    db=Depends(get_db)
):
    """
    Lista alertas com base em filtros e paginação.
    Este endpoint retorna uma lista direta de alertas.
    """
    try:
        filtro = {}
        if tipo:
            filtro["tipo"] = tipo
        if status:
            filtro["status"] = status
        if prioridade:
            filtro["prioridade"] = prioridade
        if empresa_id:
            filtro["empresa_id"] = empresa_id

        logger.debug(f"Filtro aplicado para alertas: {filtro}")

        skip = (pagina - 1) * por_pagina
        cursor = db.alertas.find(filtro).skip(skip).limit(por_pagina)
        
        alertas_do_banco = await cursor.to_list(length=por_pagina)
        
        # Converte a lista de documentos do MongoDB para um formato compatível com JSON
        return mongo_list_to_dict_list(alertas_do_banco)

    except Exception as e:
        logger.error(f"Erro ao listar alertas: {e}")
        raise HTTPException(status_code=500, detail="Erro interno ao processar a solicitação de alertas.")

@router.get("/{alerta_id}", response_model=AlertaResponse)
async def obter_alerta(alerta_id: str, db=Depends(get_db)):
    """Obtém os detalhes de um alerta específico pelo seu ID."""
    try:
        alerta = await db.alertas.find_one({"id": alerta_id})
        if not alerta:
            logger.warning(f"Alerta com ID {alerta_id} não encontrado.")
            raise HTTPException(status_code=404, detail="Alerta não encontrado")
        
        # A conversão é necessária para transformar ObjectId em string
        return mongo_list_to_dict_list([alerta])[0]
    except Exception as e:
        logger.error(f"Erro ao obter alerta com ID {alerta_id}: {e}")
        raise HTTPException(status_code=500, detail="Erro interno ao processar a solicitação.")

@router.put("/{alerta_id}", response_model=AlertaResponse)
async def atualizar_alerta(alerta_id: str, dados: AlertaUpdate, db=Depends(get_db)):
    """Atualiza as informações de um alerta existente."""
    try:
        update_data = dados.model_dump(exclude_unset=True)
        if not update_data:
            logger.warning(f"Nenhum dado fornecido para atualização do alerta {alerta_id}.")
            raise HTTPException(status_code=400, detail="Nenhum dado fornecido para atualização.")
        
        update_data["updated_at"] = datetime.utcnow()
        
        result = await db.alertas.update_one({"id": alerta_id}, {"$set": update_data})
        if result.matched_count == 0:
            logger.warning(f"Alerta com ID {alerta_id} não encontrado para atualização.")
            raise HTTPException(status_code=404, detail="Alerta não encontrado para atualização.")
        
        alerta_atualizado = await db.alertas.find_one({"id": alerta_id})
        return mongo_list_to_dict_list([alerta_atualizado])[0]
    except Exception as e:
        logger.error(f"Erro ao atualizar alerta com ID {alerta_id}: {e}")
        raise HTTPException(status_code=500, detail="Erro interno ao processar a solicitação.")

@router.delete("/{alerta_id}", status_code=200)
async def deletar_alerta(alerta_id: str, db=Depends(get_db)):
    """Deleta um alerta do sistema."""
    result = await db.alertas.delete_one({"id": alerta_id})
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Alerta não encontrado para deleção.")
    return {"message": "Alerta deletado com sucesso"}

@router.post("/marcar-como-lido", status_code=200)
async def marcar_como_lido(alerta_ids: list[str], db=Depends(get_db)):
    """Marca um ou mais alertas como lidos."""
    result = await db.alertas.update_many(
        {"id": {"$in": alerta_ids}},
        {"$set": {"status": StatusAlerta.LIDO, "lido_em": datetime.utcnow(), "updated_at": datetime.utcnow()}}
    )
    return {"message": f"{result.modified_count} alertas marcados como lidos."}

@router.get("/debug/dados", response_model=list, include_in_schema=False)
async def debug_alertas(db=Depends(get_db)):
    """Endpoint de depuração para visualizar dados brutos da coleção 'alertas'."""
    try:
        dados = await db.alertas.find().limit(5).to_list(length=5)
        return mongo_list_to_dict_list(dados)
    except Exception as e:
        logger.error(f"Erro no endpoint de depuração de alertas: {e}")
        raise HTTPException(status_code=500, detail="Erro ao buscar dados para depuração.")