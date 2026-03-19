from pydantic import BaseModel
from typing import Optional

class RelatoriosCreate(BaseModel):
    data: dict

class RelatoriosUpdate(BaseModel):
    data: Optional[dict]
    ativo: Optional[bool] = True

class RelatoriosSchema(RelatoriosCreate):
    id: str
    ativo: bool = True
