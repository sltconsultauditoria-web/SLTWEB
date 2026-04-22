"""
API Fiscal (Paridade IRIS)
Endpoints para cálculos fiscais, certidões e integração e-CAC
"""

from fastapi import APIRouter, HTTPException, Depends, Query
from typing import Optional, List
from pydantic import BaseModel, Field
from datetime import datetime
import logging
import os

from motor.motor_asyncio import AsyncIOMotorClient

from services.fiscal_calculation_service import FiscalCalculationService
from services.ecac_service import ecac_service

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/fiscal", tags=["Fiscal (IRIS)"])


def get_db():
    """Dependência para obter conexão MongoDB"""
    mongo_url = os.environ.get("MONGO_URL")
    db_name = os.environ.get("DB_NAME", "sltdctfweb")
    client = AsyncIOMotorClient(mongo_url)
    return client[db_name]


def get_fiscal_service(db=Depends(get_db)) -> FiscalCalculationService:
    return FiscalCalculationService(db)


# === Schemas ===

class SimplesNacionalRequest(BaseModel):
    cnpj: str = Field(..., description="CNPJ da empresa")
    periodo: str = Field(..., description="Período de referência (YYYY-MM)")
    receita_bruta_12m: float = Field(..., gt=0, description="Receita Bruta Acumulada 12 meses")
    receita_mensal: float = Field(..., gt=0, description="Receita do mês")
    anexo: str = Field(default="anexo_iii", description="Anexo do Simples Nacional")
    empresa_id: Optional[str] = None


class FatorRRequest(BaseModel):
    cnpj: str = Field(..., description="CNPJ da empresa")
    periodo: str = Field(..., description="Período de referência (YYYY-MM)")
    folha_salarios_12m: float = Field(..., gt=0, description="Folha de salários 12 meses")
    receita_bruta_12m: float = Field(..., gt=0, description="Receita Bruta 12 meses")
    empresa_id: Optional[str] = None


class SimulacaoEconomiaRequest(BaseModel):
    cnpj: str
    receita_bruta_12m: float
    receita_mensal: float
    folha_atual_12m: float


# === Endpoints de Cálculo Fiscal ===

@router.post("/calcular/simples-nacional")
async def calcular_simples_nacional(
    request: SimplesNacionalRequest,
    service: FiscalCalculationService = Depends(get_fiscal_service)
):
    """
    Calcula o DAS do Simples Nacional
    
    - Aplica tabelas atualizadas da LC 123/2006
    - Considera Fator R se disponível
    - Verifica sublimite estadual
    """
    try:
        resultado = await service.processar_simples_nacional(
            cnpj=request.cnpj,
            periodo=request.periodo,
            receita_bruta_12m=request.receita_bruta_12m,
            receita_mensal=request.receita_mensal,
            anexo=request.anexo,
            empresa_id=request.empresa_id
        )
        return resultado
    except Exception as e:
        logger.error(f"Erro no cálculo Simples Nacional: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/calcular/fator-r")
async def calcular_fator_r(
    request: FatorRRequest,
    service: FiscalCalculationService = Depends(get_fiscal_service)
):
    """
    Calcula o Fator R (Folha/Receita)
    
    - Determina enquadramento Anexo III ou V
    - Fator R >= 28%: Anexo III (alíquotas menores)
    - Fator R < 28%: Anexo V (alíquotas maiores)
    """
    try:
        resultado = await service.processar_fator_r(
            cnpj=request.cnpj,
            periodo=request.periodo,
            folha_salarios_12m=request.folha_salarios_12m,
            receita_bruta_12m=request.receita_bruta_12m,
            empresa_id=request.empresa_id
        )
        return resultado
    except Exception as e:
        logger.error(f"Erro no cálculo Fator R: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/simular/economia-fator-r")
async def simular_economia_fator_r(
    request: SimulacaoEconomiaRequest,
    service: FiscalCalculationService = Depends(get_fiscal_service)
):
    """
    Simula economia potencial ao otimizar o Fator R
    
    Compara cenário atual vs cenário otimizado (Fator R >= 28%)
    """
    try:
        resultado = await service.simular_economia_fator_r(
            cnpj=request.cnpj,
            receita_bruta_12m=request.receita_bruta_12m,
            receita_mensal=request.receita_mensal,
            folha_atual_12m=request.folha_atual_12m
        )
        return resultado
    except Exception as e:
        logger.error(f"Erro na simulação: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/historico/{cnpj}")
async def obter_historico_fiscal(
    cnpj: str,
    tipo: Optional[str] = Query(default=None, description="Tipo: simples_nacional, fator_r"),
    limit: int = Query(default=12, ge=1, le=50),
    service: FiscalCalculationService = Depends(get_fiscal_service)
):
    """
    Obtém histórico de cálculos fiscais
    """
    historico = await service.obter_historico_fiscal(cnpj, tipo, limit)
    return {"historico": historico, "total": len(historico)}


# === Endpoints e-CAC ===

@router.get("/ecac/certidoes/{cnpj}")
async def consultar_certidoes_ecac(cnpj: str):
    """
    Consulta certidões via e-CAC (SIMULADO)
    
    Retorna status de:
    - CND Federal (RFB/PGFN)
    - CRF (FGTS)
    - CND Estadual (SEFAZ)
    - CND Municipal
    
    **NOTA**: Implementação atual é MOCK/SIMULAÇÃO.
    Integração real requer certificado digital A1/A3.
    """
    try:
        certidoes = ecac_service.consultar_certidoes(cnpj)
        return {
            "status": "SUCESSO",
            "cnpj": cnpj,
            "data_consulta": datetime.utcnow().isoformat(),
            "certidoes": certidoes
        }
    except Exception as e:
        logger.error(f"Erro na consulta e-CAC: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/ecac/pendencias/{cnpj}")
async def consultar_pendencias_ecac(cnpj: str):
    """
    Consulta pendências fiscais via e-CAC (SIMULADO)
    
    Verifica:
    - Malha fiscal
    - Dívida ativa
    - Pendências CADIN
    - Parcelamentos em atraso
    - Declarações pendentes
    """
    try:
        pendencias = ecac_service.consultar_pendencias(cnpj)
        return {
            "status": "SUCESSO",
            **pendencias
        }
    except Exception as e:
        logger.error(f"Erro na consulta de pendências: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/ecac/simples-nacional/{cnpj}")
async def consultar_simples_nacional_ecac(cnpj: str):
    """
    Consulta histórico do Simples Nacional via e-CAC (SIMULADO)
    
    Retorna:
    - Faturamento dos últimos 12 meses
    - DAS devidos e pagos
    - Anexo atual
    - Pendências PGDAS
    """
    try:
        dados = ecac_service.consultar_simples_nacional(cnpj)
        return {
            "status": "SUCESSO",
            **dados
        }
    except Exception as e:
        logger.error(f"Erro na consulta Simples Nacional: {e}")
        raise HTTPException(status_code=500, detail=str(e))
