from fastapi import APIRouter, HTTPException, Depends
from backend.core.database import get_db
from motor.motor_asyncio import AsyncIOMotorDatabase
from typing import List

router = APIRouter( tags=["e-CAC"])

@router.get("/pendencias/{cnpj}", response_model=dict)
async def consultar_pendencias(cnpj: str, db: AsyncIOMotorDatabase = Depends(get_db)):
    # Dados mockados atualizados
    return {
        "cnpj": cnpj,
        "pendencias": [
            {"descricao": "Pendência de IRPJ", "valor": 1500.00, "vencimento": "2026-03-15"},
            {"descricao": "Pendência de CSLL", "valor": 800.00, "vencimento": "2026-04-10"}
        ]
    }

@router.get("/certidoes/{cnpj}", response_model=dict)
async def consultar_certidoes(cnpj: str, db: AsyncIOMotorDatabase = Depends(get_db)):
    # Dados mockados atualizados
    return {
        "cnpj": cnpj,
        "certidoes": [
            {"tipo": "Certidão Negativa de Débitos", "validade": "2026-12-31"},
            {"tipo": "Certidão Positiva com Efeitos de Negativa", "validade": "2026-06-30"}
        ]
    }