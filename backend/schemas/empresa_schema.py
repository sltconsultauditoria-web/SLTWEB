from pydantic import BaseModel, Field
from typing import Optional

class EmpresaSchema(BaseModel):
    nome: str
    cnpj: str
    ativo: Optional[bool] = True
