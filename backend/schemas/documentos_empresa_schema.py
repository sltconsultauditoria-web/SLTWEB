from pydantic import BaseModel, Field
from typing import Optional

class Documentos_empresaCreate(BaseModel):
    data: dict = Field(default_factory=dict)

class Documentos_empresaUpdate(BaseModel):
    data: Optional[dict] = None
    ativo: Optional[bool] = True

class Documentos_empresaSchema(Documentos_empresaCreate):
    id: str
    ativo: bool = True
