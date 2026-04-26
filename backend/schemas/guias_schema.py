from pydantic import BaseModel
from typing import Optional

class GuiasCreate(BaseModel):
    data: dict

class GuiasUpdate(BaseModel):
    data: Optional[dict]
    ativo: Optional[bool] = True

class GuiasSchema(GuiasCreate):
    id: str
    ativo: bool = True
