from fastapi import APIRouter, HTTPException
from bson import ObjectId
from backend.core.database import get_db
from backend.utils.mongo_serializer import serialize_mongo
from pydantic import BaseModel
from typing import Optional

router = APIRouter(tags=["Obrigações"])


class ObrigacaoCreate(BaseModel):
    nome: str
    descricao: Optional[str] = None


@router.get("/")
async def listar_obrigacoes():
    db = get_db()
    obrigacoes = await db.obrigacoes.find().to_list(1000)

    # Adicionar campos esperados pelo frontend com valores padrão
    for obrigacao in obrigacoes:
        obrigacao.setdefault("status", "pendente")
        obrigacao.setdefault("prioridade", "normal")
        obrigacao.setdefault("empresa", "Empresa Desconhecida")
        obrigacao.setdefault("tipo", obrigacao.get("nome", "Tipo Desconhecido"))
        obrigacao.setdefault("vencimento", "2026-12-31")

    return serialize_mongo(obrigacoes)


@router.get("/{obrigacao_id}")
async def obter_obrigacao(obrigacao_id: str):
    db = get_db()

    if not ObjectId.is_valid(obrigacao_id):
        raise HTTPException(status_code=400, detail="ID inválido")

    obrigacao = await db.obrigacoes.find_one({"_id": ObjectId(obrigacao_id)})

    if not obrigacao:
        raise HTTPException(status_code=404, detail="Obrigação não encontrada")

    return serialize_mongo(obrigacao)


@router.post("/")
async def criar_obrigacao(payload: ObrigacaoCreate):
    db = get_db()

    result = await db.obrigacoes.insert_one(payload.dict())
    nova = await db.obrigacoes.find_one({"_id": result.inserted_id})

    return serialize_mongo(nova)


@router.put("/{obrigacao_id}")
async def atualizar_obrigacao(obrigacao_id: str, payload: ObrigacaoCreate):
    db = get_db()

    if not ObjectId.is_valid(obrigacao_id):
        raise HTTPException(status_code=400, detail="ID inválido")

    result = await db.obrigacoes.update_one(
        {"_id": ObjectId(obrigacao_id)},
        {"$set": payload.dict()}
    )

    if result.matched_count == 0:
        raise HTTPException(status_code=404, detail="Obrigação não encontrada")

    atualizada = await db.obrigacoes.find_one({"_id": ObjectId(obrigacao_id)})
    return serialize_mongo(atualizada)


@router.delete("/{obrigacao_id}")
async def deletar_obrigacao(obrigacao_id: str):
    db = get_db()

    if not ObjectId.is_valid(obrigacao_id):
        raise HTTPException(status_code=400, detail="ID inválido")

    result = await db.obrigacoes.delete_one({"_id": ObjectId(obrigacao_id)})

    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Obrigação não encontrada")

    return {"message": "Obrigação removida com sucesso"}