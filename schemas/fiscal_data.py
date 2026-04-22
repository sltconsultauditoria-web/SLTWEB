from pydantic import BaseModel
from typing import Optional

class Fiscal_dataBase(BaseModel):
    nome: Optional[str] = None

class Fiscal_dataCreate(Fiscal_dataBase):
    pass

class Fiscal_dataResponse(Fiscal_dataBase):
    id: str