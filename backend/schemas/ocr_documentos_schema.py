from pydantic import BaseModel, Field
from typing import Optional

class Ocr_documentosCreate(BaseModel):
    data: dict = Field(default_factory=dict)

class Ocr_documentosUpdate(BaseModel):
    data: Optional[dict] = None
    ativo: Optional[bool] = True

class Ocr_documentosSchema(Ocr_documentosCreate):
    id: str
    ativo: bool = True
