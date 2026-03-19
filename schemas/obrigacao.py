"""
Schemas Pydantic para Obrigações Fiscais
"""

from pydantic import BaseModel, Field, validator
from typing import Optional, List
from datetime import datetime, date
from enum import Enum


# ==========================================================
# ENUMS
# ==========================================================

class TipoObrigacao(str, Enum):
    """Tipos de obrigações fiscais"""
    DCTFWEB = "dctfweb"
    DAS = "das"
    DARF = "darf"
    ECD = "ecd"
    ECF = "ecf"
    SPED_FISCAL = "sped_fiscal"
    SPED_CONTRIBUICOES = "sped_contribuicoes"
    DIRF = "dirf"
    DCTF = "dctf"
    CERTIDAO = "certidao"
    OUTRO = "outro"


class StatusObrigacao(str, Enum):
    """Status da obrigação"""
    PENDENTE = "pendente"
    EM_ANDAMENTO = "em_andamento"
    CONCLUIDA = "concluida"
    ATRASADA = "atrasada"
    CANCELADA = "cancelada"


class PrioridadeObrigacao(str, Enum):
    """Prioridade da obrigação"""
    BAIXA = "baixa"
    NORMAL = "normal"
    ALTA = "alta"
    CRITICA = "critica"


# ==========================================================
# BASE
# ==========================================================

class ObrigacaoBase(BaseModel):
    """Schema base para obrigação"""

    tipo: TipoObrigacao = Field(..., description="Tipo da obrigação")
    empresa_id: str = Field(..., description="ID da empresa")
    cnpj: str = Field(..., description="CNPJ da empresa")

    ano: int = Field(..., ge=2000, le=2100, description="Ano da competência")
    mes: int = Field(..., ge=1, le=12, description="Mês da competência (1-12)")

    competencia: Optional[str] = Field(
        default=None,
        description="Período de competência (MM/YYYY)"
    )

    @validator("competencia", always=True)
    def gerar_competencia(cls, v, values):
        if v:
            return v
        if "mes" in values and "ano" in values:
            return f"{values['mes']:02d}/{values['ano']}"
        return v


# ==========================================================
# CREATE
# ==========================================================

class ObrigacaoCreate(ObrigacaoBase):
    """Schema para criação de obrigação"""

    valor: float = Field(default=0.0, ge=0)
    data_vencimento: Optional[date] = None
    observacoes: Optional[str] = None


# ==========================================================
# UPDATE
# ==========================================================

class ObrigacaoUpdate(BaseModel):
    """Schema para atualização de obrigação"""

    status: Optional[StatusObrigacao] = None
    valor: Optional[float] = Field(default=None, ge=0)
    valor_pago: Optional[float] = Field(default=None, ge=0)

    data_vencimento: Optional[date] = None
    data_pagamento: Optional[date] = None

    prioridade: Optional[PrioridadeObrigacao] = None
    observacoes: Optional[str] = None
    updated_at: Optional[datetime] = None


# ==========================================================
# RESPONSE
# ==========================================================

class ObrigacaoResponse(ObrigacaoBase):
    """Schema de resposta para obrigação"""

    id: str = Field(..., description="ID único da obrigação")

    status: StatusObrigacao = Field(default=StatusObrigacao.PENDENTE)
    prioridade: PrioridadeObrigacao = Field(default=PrioridadeObrigacao.NORMAL)

    # Valores
    valor: float = Field(default=0.0)
    valor_pago: float = Field(default=0.0)

    # Datas
    data_vencimento: Optional[date] = None
    data_pagamento: Optional[date] = None

    # Relacionamentos
    documento_ids: List[str] = Field(default_factory=list)
    empresa_nome: Optional[str] = None

    # Metadados
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: Optional[datetime] = None
    observacoes: Optional[str] = None

    class Config:
        from_attributes = True  # compatível com ORM / Pydantic v2


# ==========================================================
# LIST RESPONSE
# ==========================================================

class ObrigacaoListResponse(BaseModel):
    """Schema de resposta para lista paginada"""

    obrigacoes: List[ObrigacaoResponse]
    total: int
    pagina: int = 1
    por_pagina: int = 20