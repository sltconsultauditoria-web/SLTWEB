from pydantic import BaseModel, Field
from typing import Optional, List

class ObrigacoesCreate(BaseModel):
    data: dict = Field(default_factory=dict)

class ObrigacoesUpdate(BaseModel):
    data: Optional[dict] = None
    ativo: Optional[bool] = True

class ObrigacoesSchema(ObrigacoesCreate):
    id: str
    ativo: bool = True
    data: Optional[dict] = None  # Tornar o campo 'data' opcional

class ObrigacaoListResponse(BaseModel):
    data: Optional[List[ObrigacoesSchema]] = None  # Tornar o campo 'data' opcional e uma lista de objetos ObrigacoesSchema
