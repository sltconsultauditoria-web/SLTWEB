from pydantic import BaseModel
from typing import Optional

class Obrigacoes_empresaBase(BaseModel):
    nome: Optional[str] = None

class Obrigacoes_empresaCreate(Obrigacoes_empresaBase):
    pass

class Obrigacoes_empresaResponse(Obrigacoes_empresaBase):
    id: str