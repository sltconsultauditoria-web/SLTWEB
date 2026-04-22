from pydantic import BaseModel
from typing import Optional

class Documentos_empresaCreate(BaseModel):
    data: dict

class Documentos_empresaUpdate(BaseModel):
    data: Optional[dict]
    ativo: Optional[bool] = True

class Documentos_empresaSchema(Documentos_empresaCreate):
    id: str
    ativo: bool = True
