from pydantic import BaseModel
from typing import Optional

class DocumentosCreate(BaseModel):
    data: dict

class DocumentosUpdate(BaseModel):
    data: Optional[dict]
    ativo: Optional[bool] = True

class DocumentosSchema(DocumentosCreate):
    id: str
    ativo: bool = True
