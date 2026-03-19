from pydantic import BaseModel
from typing import Optional

class ConfiguracoesBase(BaseModel):
    nome: Optional[str] = None

class ConfiguracoesCreate(ConfiguracoesBase):
    pass

class ConfiguracoesResponse(ConfiguracoesBase):
    id: str