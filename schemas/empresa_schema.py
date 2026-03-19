from pydantic import BaseModel
from typing import Optional

class EmpresaSchema(BaseModel):
    nome: str
    cnpj: str
    ativo: Optional[bool] = True
