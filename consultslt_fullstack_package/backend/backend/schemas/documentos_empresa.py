from pydantic import BaseModel
from typing import Optional

class Documentos_empresaBase(BaseModel):
    nome: Optional[str] = None

class Documentos_empresaCreate(Documentos_empresaBase):
    pass

class Documentos_empresaResponse(Documentos_empresaBase):
    id: str