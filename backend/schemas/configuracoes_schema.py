from pydantic import BaseModel, Field
from typing import Optional

class ConfiguracoesCreate(BaseModel):
    data: dict = Field(default_factory=dict)

class ConfiguracoesUpdate(BaseModel):
    data: Optional[dict] = None
    ativo: Optional[bool] = True

class ConfiguracoesSchema(ConfiguracoesCreate):
    id: str
    ativo: bool = True
