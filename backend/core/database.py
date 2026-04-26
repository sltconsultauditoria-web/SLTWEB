
"""
Módulo de conexão com MongoDB - consultslt_db
Gerencia o ciclo de vida da conexão usando Motor (async)
"""

import os
import logging
from pathlib import Path
from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorDatabase

logger = logging.getLogger(__name__)

# Carrega .env se existir
try:
    from dotenv import load_dotenv
    _env_path = Path(__file__).parent.parent / ".env"
    if _env_path.exists():
        load_dotenv(_env_path)
except ImportError:
    pass

# Variáveis globais de conexão
_client: AsyncIOMotorClient | None = None
_db: AsyncIOMotorDatabase | None = None

# Aliases públicos
client: AsyncIOMotorClient | None = None
db: AsyncIOMotorDatabase | None = None


async def init_db():
    """
    Inicializa a conexão com o MongoDB.
    Deve ser chamada no evento de startup do FastAPI.
    """
    global _client, _db, client, db

    mongo_url = os.getenv("MONGO_URL", "mongodb://127.0.0.1:27017")
    database_name = os.getenv("MONGO_DB_NAME", os.getenv("DB_NAME", "consultslt_db"))

    logger.info(f"Conectando ao MongoDB: {mongo_url} / {database_name}")

    try:
        _client = AsyncIOMotorClient(
            mongo_url,
            serverSelectionTimeoutMS=5000,
            connectTimeoutMS=5000,
        )

        # Testa conexão
        await _client.admin.command("ping")

        _db = _client[database_name]

        # Sincroniza aliases públicos
        client = _client
        db = _db

        logger.info(f"✅ MongoDB conectado: {database_name}")

    except Exception as e:
        logger.error(f"❌ Falha ao conectar ao MongoDB: {e}")
        raise


async def close_db():
    """Fecha a conexão com o MongoDB."""
    global _client, client

    if _client:
        _client.close()
        client = None
        logger.info("MongoDB desconectado.")


def get_db() -> AsyncIOMotorDatabase:
    """
    Dependency para FastAPI:
    Uso: db: AsyncIOMotorDatabase = Depends(get_db)
    """
    if _db is None:
        raise RuntimeError(
            "Banco de dados não inicializado. "
            "Verifique se init_db() foi chamado no startup."
        )
    return _db


# 🔥 Alias para compatibilidade com código que usa get_database()
def get_database() -> AsyncIOMotorDatabase:
    """
    Alias compatível com código legado.
    """
    return get_db()