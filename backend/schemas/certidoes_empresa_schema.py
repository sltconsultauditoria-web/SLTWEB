from pydantic import BaseModel, Field
from typing import Optional

class Certidoes_empresaCreate(BaseModel):
    data: dict = Field(default_factory=dict)

class Certidoes_empresaUpdate(BaseModel):
    data: Optional[dict] = None
    ativo: Optional[bool] = True

class Certidoes_empresaSchema(Certidoes_empresaCreate):
    id: str
    ativo: bool = True
