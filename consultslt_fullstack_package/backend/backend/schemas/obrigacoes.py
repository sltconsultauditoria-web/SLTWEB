from pydantic import BaseModel
from typing import Optional

class ObrigacoesBase(BaseModel):
    nome: Optional[str] = None

class ObrigacoesCreate(ObrigacoesBase):
    pass

class ObrigacoesResponse(ObrigacoesBase):
    id: str