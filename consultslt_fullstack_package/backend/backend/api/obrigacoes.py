"""
Endpoints para gestão de Obrigações Fiscais
"""

from fastapi import APIRouter, HTTPException, Depends, Query
from backend.db.utils import mongo_list_to_dict_list
from typing import Optional, List
from datetime import date
import logging
import os
from motor.motor_asyncio import AsyncIOMotorClient

from backend.schemas.obrigacao import (
    TipoObrigacao,
    StatusObrigacao,
    ObrigacaoCreate,
    ObrigacaoUpdate,
    ObrigacaoResponse,
    ObrigacaoListResponse
)
from backend.services.obrigacao_service import ObrigacaoService

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/obrigacoes", tags=["Obrigações"])

def get_db():
    """Dependência para obter conexão com MongoDB."""
    mongo_url = os.environ.get("MONGO_URL")
    db_name = os.environ.get("DB_NAME", "sltdctfweb")
    client = AsyncIOMotorClient(mongo_url)
    return client[db_name]

def get_obrigacao_service(db=Depends(get_db)) -> ObrigacaoService:
    """Dependência para injetar o serviço de obrigações."""
    return ObrigacaoService(db)

@router.post("/", response_model=ObrigacaoResponse, status_code=201)
async def criar_obrigacao(
    dados: ObrigacaoCreate,
    service: ObrigacaoService = Depends(get_obrigacao_service)
):
    """Cria uma nova obrigação fiscal para uma empresa."""
    return await service.criar_obrigacao(dados)

@router.get("/", response_model=List[ObrigacaoResponse])
async def listar_obrigacoes(
    empresa_id: Optional[str] = Query(default=None),
    tipo: Optional[TipoObrigacao] = Query(default=None),
    status: Optional[StatusObrigacao] = Query(default=None),
    cnpj: Optional[str] = Query(default=None),
    data_inicio: Optional[date] = Query(default=None),
    data_fim: Optional[date] = Query(default=None),
    pagina: int = Query(default=1, ge=1),
    por_pagina: int = Query(default=20, ge=1, le=100),
    service: ObrigacaoService = Depends(get_obrigacao_service)
):
    """
    Lista obrigações com filtros e paginação.
    Retorna uma lista direta de obrigações para compatibilidade.
    """
    logger.debug(f"Listando obrigações com filtros: {locals()}")
    try:
        result = await service.listar_obrigacoes(
            empresa_id=empresa_id,
            tipo=tipo,
            status=status,
            cnpj=cnpj,
            data_inicio=data_inicio,
            data_fim=data_fim,
            pagina=pagina,
            por_pagina=por_pagina
        )
        # Extrai a lista do resultado do serviço para corresponder ao response_model
        obrigacoes_list = result.get("obrigacoes", [])
        return obrigacoes_list
    except Exception as e:
        logger.error(f"Erro ao listar obrigações: {e}")
        raise HTTPException(status_code=500, detail="Erro interno ao listar obrigações.")

@router.get("/proximos-vencimentos", response_model=List[ObrigacaoResponse])
async def obter_proximos_vencimentos(
    dias: int = Query(default=30, ge=1, le=365),
    empresa_id: Optional[str] = Query(default=None),
    service: ObrigacaoService = Depends(get_obrigacao_service)
):
    """Obtém uma lista de obrigações com vencimento nos próximos N dias."""
    return await service.obter_proximos_vencimentos(dias=dias, empresa_id=empresa_id)

@router.get("/{obrigacao_id}", response_model=ObrigacaoResponse)
async def obter_obrigacao(
    obrigacao_id: str,
    service: ObrigacaoService = Depends(get_obrigacao_service)
):
    """Obtém os detalhes de uma obrigação fiscal específica."""
    obrigacao = await service.obter_obrigacao(obrigacao_id)
    if not obrigacao:
        raise HTTPException(status_code=404, detail="Obrigação não encontrada")
    return obrigacao

@router.put("/{obrigacao_id}", response_model=ObrigacaoResponse)
async def atualizar_obrigacao(
    obrigacao_id: str,
    dados: ObrigacaoUpdate,
    service: ObrigacaoService = Depends(get_obrigacao_service)
):
    """Atualiza uma obrigação fiscal existente."""
    obrigacao = await service.atualizar_obrigacao(obrigacao_id, dados)
    if not obrigacao:
        raise HTTPException(status_code=404, detail="Obrigação não encontrada")
    return obrigacao

@router.delete("/{obrigacao_id}", status_code=200)
async def deletar_obrigacao(
    obrigacao_id: str,
    service: ObrigacaoService = Depends(get_obrigacao_service)
):
    """Deleta uma obrigação fiscal do sistema."""
    sucesso = await service.deletar_obrigacao(obrigacao_id)
    if not sucesso:
        raise HTTPException(status_code=404, detail="Obrigação não encontrada")
    return {"message": "Obrigação deletada com sucesso"}

@router.post("/atualizar-atrasados", status_code=200)
async def atualizar_obrigacoes_atrasadas(
    service: ObrigacaoService = Depends(get_obrigacao_service)
):
    """Verifica e atualiza o status de obrigações vencidas para 'Atrasada'."""
    count = await service.atualizar_status_atrasados()
    return {"message": f"{count} obrigações atualizadas para 'Atrasada'."}
