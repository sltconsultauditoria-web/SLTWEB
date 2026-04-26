from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime
from enum import Enum

class TipoCertidao(str, Enum):
    FGTS = "FGTS"
    RECEITA_FEDERAL = "Receita Federal"
    ESTADUAL = "Estadual"
    MUNICIPAL = "Municipal"

class StatusCertidao:
    VALIDA = "Válida"
    VENCIDA = "Vencida"
    PROXIMA_VENCER = "Próxima a vencer"

class CertidaoCreate(BaseModel):
    empresa: str
    tipo: str
    numero: Optional[str] = None
    data_emissao: Optional[str] = None
    data_validade: Optional[str] = None
    status: str = StatusCertidao.VALIDA
    url: Optional[str] = None

class CertidaoUpdate(BaseModel):
    numero: Optional[str] = None
    data_emissao: Optional[str] = None
    data_validade: Optional[str] = None
    status: Optional[str] = None
    url: Optional[str] = None

class CertidaoResponse(CertidaoCreate):
    id: str
    created_at: datetime

class CertidaoListResponse(BaseModel):
    total: int
    certidoes: List[CertidaoResponse]