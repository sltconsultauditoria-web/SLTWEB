from pydantic import BaseModel
from typing import Optional

class ObrigacoesCreate(BaseModel):
    data: dict

class ObrigacoesUpdate(BaseModel):
    data: Optional[dict]
    ativo: Optional[bool] = True

class ObrigacoesSchema(ObrigacoesCreate):
    id: str
    ativo: bool = True
