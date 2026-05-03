from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class BaseSchema(BaseModel):
    nome: Optional[str] = None
    ativo: bool = True
    criado_em: datetime | None = None

class CreateSchema(BaseSchema):
    pass

class UpdateSchema(BaseSchema):
    pass
