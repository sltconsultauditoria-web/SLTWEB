"""
API de Auditoria Fiscal (Paridade Kolossus)
Endpoints para auditoria SPED e cruzamento fiscal
"""

from fastapi import APIRouter, HTTPException, Depends, Query, UploadFile, File, Form
from backend.db.utils import mongo_list_to_dict_list
from typing import Optional, List
import logging
import os
from motor.motor_asyncio import AsyncIOMotorClient
from backend.services.auditoria_service import AuditoriaService

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/auditoria", tags=["Auditoria Fiscal (Kolossus)"])

def get_db():
    """Dependência para obter conexão com MongoDB."""
    mongo_url = os.environ.get("MONGO_URL")
    db_name = os.environ.get("DB_NAME", "sltdctfweb")
    client = AsyncIOMotorClient(mongo_url)
    return client[db_name]

def get_auditoria_service(db=Depends(get_db)) -> AuditoriaService:
    """Dependência para injetar o serviço de auditoria."""
    return AuditoriaService(db)

@router.post("/executar", status_code=202)
async def executar_auditoria(
    cnpj: str = Form(..., description="CNPJ da empresa"),
    periodo: str = Form(..., description="Período (YYYY-MM)"),
    tipo: str = Form(default="sped_fiscal", description="Tipo: sped_fiscal ou sped_contribuicoes"),
    empresa_id: Optional[str] = Form(default=None),
    arquivo: UploadFile = File(..., description="Arquivo SPED (.txt)"),
    service: AuditoriaService = Depends(get_auditoria_service)
):
    """
    Submete um arquivo SPED para execução de uma auditoria completa.
    A auditoria é processada em segundo plano.
    """
    try:
        import tempfile
        
        with tempfile.NamedTemporaryFile(delete=False, suffix=".txt") as tmp:
            content = await arquivo.read()
            tmp.write(content)
            tmp_path = tmp.name
        
        # Aqui você poderia, por exemplo, enfileirar a tarefa em um background worker
        # Por enquanto, vamos executar diretamente, mas o status 202 (Accepted) indica isso.
        resultado = await service.executar_auditoria_sped(
            cnpj=cnpj,
            periodo=periodo,
            tipo=tipo,
            arquivo_path=tmp_path,
            empresa_id=empresa_id
        )
        
        return resultado
        
    except Exception as e:
        logger.error(f"Erro ao submeter auditoria: {e}")
        raise HTTPException(status_code=500, detail=f"Erro ao processar o arquivo de auditoria: {e}")

@router.get("/", response_model=dict)
async def listar_auditorias(
    cnpj: Optional[str] = Query(default=None),
    empresa_id: Optional[str] = Query(default=None),
    tipo: Optional[str] = Query(default=None),
    limit: int = Query(default=20, ge=1, le=100),
    service: AuditoriaService = Depends(get_auditoria_service)
):
    """
    Lista as auditorias realizadas, com opção de filtros.
    """
    logger.debug("Iniciando listagem de auditorias")
    try:
        auditorias = await service.listar_auditorias(
            cnpj=cnpj, empresa_id=empresa_id, tipo=tipo, limit=limit
        )
        return {"auditorias": auditorias, "total": len(auditorias)}
    except Exception as e:
        logger.error(f"Erro ao listar auditorias: {e}")
        raise HTTPException(status_code=500, detail="Erro interno ao listar auditorias.")

@router.get("/estatisticas")
async def obter_estatisticas_conformidade(
    cnpj: Optional[str] = Query(default=None),
    empresa_id: Optional[str] = Query(default=None),
    service: AuditoriaService = Depends(get_auditoria_service)
):
    """
    Obtém estatísticas consolidadas de conformidade fiscal.
    """
    return await service.obter_estatisticas_conformidade(
        cnpj=cnpj,
        empresa_id=empresa_id
    )

@router.get("/{auditoria_id}")
async def obter_auditoria(
    auditoria_id: str,
    service: AuditoriaService = Depends(get_auditoria_service)
):
    """
    Obtém os detalhes completos de um relatório de auditoria específico.
    """
    auditoria = await service.obter_auditoria(auditoria_id)
    if not auditoria:
        raise HTTPException(status_code=404, detail="Auditoria não encontrada")
    
    # A conversão aqui é crucial, pois o serviço retorna um objeto do banco
    return mongo_list_to_dict_list([auditoria])[0]