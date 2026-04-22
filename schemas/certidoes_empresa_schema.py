from pydantic import BaseModel
from typing import Optional

class Certidoes_empresaCreate(BaseModel):
    data: dict

class Certidoes_empresaUpdate(BaseModel):
    data: Optional[dict]
    ativo: Optional[bool] = True

class Certidoes_empresaSchema(Certidoes_empresaCreate):
    id: str
    ativo: bool = True
