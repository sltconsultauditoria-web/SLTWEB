from pydantic import BaseModel
from typing import Optional

class Tipos_documentosCreate(BaseModel):
    data: dict

class Tipos_documentosUpdate(BaseModel):
    data: Optional[dict]
    ativo: Optional[bool] = True

class Tipos_documentosSchema(Tipos_documentosCreate):
    id: str
    ativo: bool = True
