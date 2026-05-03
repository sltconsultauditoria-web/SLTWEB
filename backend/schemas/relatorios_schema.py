from pydantic import BaseModel, Field
from typing import Optional

class RelatoriosCreate(BaseModel):
    data: dict = Field(default_factory=dict)

class RelatoriosUpdate(BaseModel):
    data: Optional[dict] = None
    ativo: Optional[bool] = True

class RelatoriosSchema(RelatoriosCreate):
    id: str
    ativo: bool = True
