from pydantic import BaseModel
from typing import Optional

class EmpresasCreate(BaseModel):
    razao_social: str
    cnpj: str
    nome_fantasia: Optional[str]
    regime: str
    ativo: Optional[bool] = True

class EmpresasUpdate(BaseModel):
    razao_social: Optional[str]
    cnpj: Optional[str]
    nome_fantasia: Optional[str]
    regime: Optional[str]
    ativo: Optional[bool] = True

class EmpresasSchema(EmpresasCreate):
    razao_social: Optional[str]
    nome_fantasia: Optional[str]
    regime: Optional[str]
    id: str
