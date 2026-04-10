from pydantic import BaseModel
from typing import Optional

class GuiasBase(BaseModel):
    nome: Optional[str] = None

class GuiasCreate(GuiasBase):
    pass

class GuiasResponse(GuiasBase):
    id: str