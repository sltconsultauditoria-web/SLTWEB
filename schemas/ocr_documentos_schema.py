from pydantic import BaseModel
from typing import Optional

class Ocr_documentosCreate(BaseModel):
    data: dict

class Ocr_documentosUpdate(BaseModel):
    data: Optional[dict]
    ativo: Optional[bool] = True

class Ocr_documentosSchema(Ocr_documentosCreate):
    id: str
    ativo: bool = True
