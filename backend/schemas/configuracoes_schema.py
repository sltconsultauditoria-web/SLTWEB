from pydantic import BaseModel
from typing import Optional

class ConfiguracoesCreate(BaseModel):
    data: dict

class ConfiguracoesUpdate(BaseModel):
    data: Optional[dict]
    ativo: Optional[bool] = True

class ConfiguracoesSchema(ConfiguracoesCreate):
    id: str
    ativo: bool = True
