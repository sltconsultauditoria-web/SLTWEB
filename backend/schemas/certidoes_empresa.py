from pydantic import BaseModel
from typing import Optional

class Certidoes_empresaBase(BaseModel):
    nome: Optional[str] = None

class Certidoes_empresaCreate(Certidoes_empresaBase):
    pass

class Certidoes_empresaResponse(Certidoes_empresaBase):
    id: str