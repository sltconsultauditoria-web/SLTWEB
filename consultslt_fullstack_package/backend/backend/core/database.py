# backend/core/database.py (VERSÃO FINAL E CORRETA)

import os
from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorDatabase
from fastapi import Depends, HTTPException

# Variáveis globais para armazenar a conexão e o banco de dados.
_client: AsyncIOMotorClient | None = None
_db: AsyncIOMotorDatabase | None = None

# --- LINHA REMOVIDA ---
# A linha abaixo causava o erro de importação circular e foi removida.
# # from backend.core.database import get_db # Removido 
# ----------------------

async def init_db() -> None:
    """
    Inicializa a conexão com o MongoDB.
    Esta função é chamada uma vez quando o servidor FastAPI inicia (via lifespan).
    """
    global _client, _db
    
    mongo_url = os.getenv("MONGO_URL", "mongodb://localhost:27017")
    database_name = os.getenv("MONGO_DB_NAME", "consultslt_db")
    
    try:
        print("INFO: Iniciando conexão com MongoDB...")
        print(f"INFO: URL: {mongo_url}")
        print(f"INFO: Database: {database_name}")
        
        _client = AsyncIOMotorClient(mongo_url)
        await _client.admin.command("ping")
        _db = _client[database_name]
        
        print("INFO: Conexão com MongoDB estabelecida com sucesso.")
    except Exception as e:
        print(f"ERROR: Falha ao conectar ao MongoDB: {e}")
        raise e

async def close_db() -> None:
    """
    Fecha a conexão com o MongoDB.
    Esta função é chamada uma vez quando o servidor FastAPI desliga (via lifespan).
    """
    global _client
    if _client:
        _client.close()
        print("INFO: Conexão com MongoDB encerrada.")

def get_db() -> AsyncIOMotorDatabase:
    """
    Dependência do FastAPI para injetar a instância do banco de dados nas rotas.
    """
    if _db is None:
        raise HTTPException(
            status_code=500,
            detail="Banco de dados não inicializado. Verifique a função init_db() no startup do servidor."
        )
    return _db
