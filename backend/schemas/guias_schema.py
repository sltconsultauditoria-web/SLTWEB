from pydantic import BaseModel, Field
from typing import Optional

class GuiasCreate(BaseModel):
    data: dict = Field(default_factory=dict)

class GuiasUpdate(BaseModel):
    data: Optional[dict] = None
    ativo: Optional[bool] = True

class GuiasSchema(GuiasCreate):
    id: str
    ativo: bool = True
