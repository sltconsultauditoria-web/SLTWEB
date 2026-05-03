from pydantic import BaseModel, Field
from typing import Optional

class DocumentosCreate(BaseModel):
    data: dict = Field(default_factory=dict)

class DocumentosUpdate(BaseModel):
    data: Optional[dict] = None
    ativo: Optional[bool] = True

class DocumentosSchema(DocumentosCreate):
    id: str
    ativo: bool = True
