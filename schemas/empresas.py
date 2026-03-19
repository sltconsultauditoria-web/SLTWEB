from pydantic import BaseModel, EmailStr, Field
from typing import Optional
from datetime import datetime


class Endereco(BaseModel):
    logradouro: Optional[str] = None
    cidade: Optional[str] = None
    estado: Optional[str] = None
    cep: Optional[str] = None


class Contato(BaseModel):
    email: Optional[EmailStr] = None
    telefone: Optional[str] = None


class EmpresasBase(BaseModel):
    cnpj: str
    razaoSocial: str
    nomeFantasia: Optional[str] = None
    regimeTributario: Optional[str] = None
    status: str = "ativo"
    endereco: Optional[Endereco] = None
    contato: Optional[Contato] = None


class EmpresasCreate(EmpresasBase):
    pass


class EmpresasUpdate(BaseModel):
    razaoSocial: Optional[str] = None
    nomeFantasia: Optional[str] = None
    regimeTributario: Optional[str] = None
    status: Optional[str] = None
    endereco: Optional[Endereco] = None
    contato: Optional[Contato] = None
