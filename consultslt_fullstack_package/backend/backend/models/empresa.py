from pydantic import BaseModel, Field, EmailStr, validator
from typing import Optional
from datetime import datetime
import re

# ==========================================
# Validação de CNPJ
# ==========================================

def validate_cnpj(cnpj: str) -> bool:
    cnpj = re.sub(r"[^\d]", "", cnpj)

    if len(cnpj) != 14 or cnpj == cnpj[0] * 14:
        return False

    def calculate_digit(cnpj, length):
        total = 0
        pos = length - 7
        for i in range(length):
            total += int(cnpj[i]) * pos
            pos -= 1
            if pos < 2:
                pos = 9
        result = total % 11
        return 0 if result < 2 else 11 - result

    digit1 = calculate_digit(cnpj, 12)
    digit2 = calculate_digit(cnpj, 13)

    return digit1 == int(cnpj[12]) and digit2 == int(cnpj[13])


# ==========================================
# ENUMS
# ==========================================

REGIMES = ["Simples Nacional", "Lucro Presumido", "MEI"]
STATUS = ["Ativo", "Inativo"]


# ==========================================
# Base
# ==========================================

class EmpresaBase(BaseModel):
    nome: str = Field(..., min_length=2)
    razao_social: str = Field(..., min_length=2)
    cnpj: str
    regime_tributario: str
    receita_bruta: float
    fator_r: Optional[float] = None
    status: str = "Ativo"

    @validator("cnpj")
    def validar_cnpj(cls, v):
        if not validate_cnpj(v):
            raise ValueError("CNPJ inválido")
        return re.sub(r"[^\d]", "", v)

    @validator("regime_tributario")
    def validar_regime(cls, v):
        if v not in REGIMES:
            raise ValueError(f"Regime deve ser um de {REGIMES}")
        return v

    @validator("status")
    def validar_status(cls, v):
        if v not in STATUS:
            raise ValueError(f"Status deve ser um de {STATUS}")
        return v


# ==========================================
# CREATE
# ==========================================

class EmpresaCreate(EmpresaBase):
    pass


# ==========================================
# UPDATE
# ==========================================

class EmpresaUpdate(BaseModel):
    nome: Optional[str]
    razao_social: Optional[str]
    regime_tributario: Optional[str]
    receita_bruta: Optional[float]
    fator_r: Optional[float]
    status: Optional[str]


# ==========================================
# RESPONSE
# ==========================================

class EmpresaResponse(EmpresaBase):
    id: str
    created_at: datetime
    updated_at: Optional[datetime]
