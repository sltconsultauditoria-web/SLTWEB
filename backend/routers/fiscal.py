"""Router Fiscal - /api/fiscal"""
import logging, uuid
from datetime import datetime
from typing import List, Optional, Any
from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from motor.motor_asyncio import AsyncIOMotorDatabase
from backend.core.database import get_db

logger = logging.getLogger(__name__)
router = APIRouter( tags=["Fiscal"])

class SimplesNacionalRequest(BaseModel):
    cnpj: Optional[str] = None
    empresa_id: Optional[str] = None
    receita_bruta_12m: float
    receita_bruta_mes: float
    folha_salarios: Optional[float] = None
    anexo: str = "III"
    competencia: Optional[str] = None

class FatorRRequest(BaseModel):
    cnpj: Optional[str] = None
    empresa_id: Optional[str] = None
    folha_salarios_12m: float
    receita_bruta_12m: float

class FiscalIrisCreate(BaseModel):
    empresa_id: Optional[str] = None
    cnpj: Optional[str] = None
    tipo: Optional[str] = None
    dados: Optional[Any] = None

class FiscalIrisUpdate(BaseModel):
    tipo: Optional[str] = None
    dados: Optional[Any] = None

class FiscalIrisResponse(BaseModel):
    id: str
    empresa_id: Optional[str] = None
    cnpj: Optional[str] = None
    tipo: Optional[str] = None
    dados: Optional[Any] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    class Config: from_attributes = True

def _s(doc): doc["id"] = str(doc.get("_id", doc.get("id",""))); doc.pop("_id",None); return doc

@router.post("/calcular/simples-nacional")
async def calcular_simples_nacional(dados: SimplesNacionalRequest, db: AsyncIOMotorDatabase = Depends(get_db)):
    rb12 = dados.receita_bruta_12m; rb_mes = dados.receita_bruta_mes
    tabelas = {
        "I": [(180000,0.04,0),(360000,0.073,5940),(720000,0.095,13860),(1800000,0.107,22500),(3600000,0.143,87300),(4800000,0.19,378000)],
        "III": [(180000,0.06,0),(360000,0.112,9360),(720000,0.135,17640),(1800000,0.16,35640),(3600000,0.21,125640),(4800000,0.33,648000)],
    }
    tabela = tabelas.get(dados.anexo, tabelas["III"])
    aliquota_nominal = 0.06; deducao = 0
    for limite, aliq, ded in tabela:
        if rb12 <= limite: aliquota_nominal = aliq; deducao = ded; break
    aliquota_efetiva = ((rb12 * aliquota_nominal) - deducao) / rb12 if rb12 > 0 else 0
    valor_das = rb_mes * aliquota_efetiva
    return {"success": True, "cnpj": dados.cnpj, "competencia": dados.competencia,
            "receita_bruta_mes": rb_mes, "receita_bruta_12m": rb12, "anexo": dados.anexo,
            "aliquota_nominal": round(aliquota_nominal*100,2), "aliquota_efetiva": round(aliquota_efetiva*100,4),
            "valor_das": round(valor_das,2), "calculado_em": datetime.utcnow().isoformat()}

@router.post("/calcular/fator-r")
async def calcular_fator_r(dados: FatorRRequest):
    fator_r = dados.folha_salarios_12m / dados.receita_bruta_12m if dados.receita_bruta_12m > 0 else 0
    enquadramento = "Anexo III" if fator_r >= 0.28 else "Anexo V"
    return {"success": True, "cnpj": dados.cnpj, "folha_salarios_12m": dados.folha_salarios_12m,
            "receita_bruta_12m": dados.receita_bruta_12m, "fator_r": round(fator_r,4),
            "fator_r_percentual": round(fator_r*100,2), "enquadramento": enquadramento,
            "calculado_em": datetime.utcnow().isoformat()}

@router.get("/ecac/certidoes/{cnpj}")
async def consultar_certidoes_ecac(cnpj: str, db: AsyncIOMotorDatabase = Depends(get_db)):
    cnpj_limpo = "".join(filter(str.isdigit, cnpj))
    certidoes = await db["certidoes"].find({"cnpj": cnpj_limpo}).to_list(20)
    return {"success": True, "cnpj": cnpj_limpo, "certidoes": [_s(c) for c in certidoes],
            "consultado_em": datetime.utcnow().isoformat()}

@router.get("/ecac/pendencias/{cnpj}")
async def consultar_pendencias_ecac(cnpj: str, db: AsyncIOMotorDatabase = Depends(get_db)):
    cnpj_limpo = "".join(filter(str.isdigit, cnpj))
    debitos = await db["debitos"].find({"cnpj": cnpj_limpo, "status": "em_aberto"}).to_list(20)
    return {"success": True, "cnpj": cnpj_limpo, "pendencias": [_s(d) for d in debitos],
            "consultado_em": datetime.utcnow().isoformat()}

@router.get("/iris", response_model=List[FiscalIrisResponse])
async def listar_iris(db: AsyncIOMotorDatabase = Depends(get_db)):
    items = await db["fiscal_iris"].find({"deletedAt": None}).to_list(100)
    return [_s(i) for i in items]

@router.post("/iris", response_model=FiscalIrisResponse, status_code=201)
async def criar_iris(item: FiscalIrisCreate, db: AsyncIOMotorDatabase = Depends(get_db)):
    doc = item.dict(); doc["id"] = str(uuid.uuid4()); doc["created_at"] = datetime.utcnow()
    doc["updated_at"] = datetime.utcnow(); doc["deletedAt"] = None
    await db["fiscal_iris"].insert_one(doc); doc.pop("_id", None); return doc

@router.get("/iris/{item_id}", response_model=FiscalIrisResponse)
async def obter_iris(item_id: str, db: AsyncIOMotorDatabase = Depends(get_db)):
    item = await db["fiscal_iris"].find_one({"id": item_id, "deletedAt": None})
    if not item: raise HTTPException(404, "Item nao encontrado")
    return _s(item)

@router.put("/iris/{item_id}", response_model=FiscalIrisResponse)
async def atualizar_iris(item_id: str, item: FiscalIrisUpdate, db: AsyncIOMotorDatabase = Depends(get_db)):
    u = item.dict(exclude_unset=True); u["updated_at"] = datetime.utcnow()
    r = await db["fiscal_iris"].update_one({"id": item_id}, {"$set": u})
    if r.matched_count == 0: raise HTTPException(404, "Item nao encontrado")
    return _s(await db["fiscal_iris"].find_one({"id": item_id}))

@router.delete("/iris/{item_id}")
async def deletar_iris(item_id: str, db: AsyncIOMotorDatabase = Depends(get_db)):
    r = await db["fiscal_iris"].update_one({"id": item_id}, {"$set": {"deletedAt": datetime.utcnow()}})
    if r.matched_count == 0: raise HTTPException(404, "Item nao encontrado")
    return {"success": True}
