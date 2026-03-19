import os
import asyncio
from motor.motor_asyncio import AsyncIOMotorClient
from dotenv import load_dotenv

# 🔥 Carrega o .env explicitamente
load_dotenv(dotenv_path=os.path.join(os.getcwd(), ".env"))

MONGO_URI = os.getenv("MONGO_URI")
DB_NAME = os.getenv("MONGO_DB")

if not MONGO_URI or not DB_NAME:
    raise RuntimeError(
        f"❌ Variáveis de ambiente inválidas:\n"
        f"MONGO_URI={MONGO_URI}\n"
        f"MONGO_DB={DB_NAME}"
    )

TARGET_COLLECTIONS = [
    "users",
    "usuarios",
    "empresas",
    "documentos_empresa",
    "certidoes_empresa",
    "obrigacoes_empresa",
    "fiscal",
    "fiscal_data",
    "debitos",
    "guias",
    "certidoes",
    "tipos_certidoes",
    "tipos_documentos",
    "tipos_obrigacoes",
    "dashboard_metrics",
    "relatorios",
    "relatorios_gerados",
    "alertas",
    "auditoria",
    "ocr_documentos",
    "robots",
    "status_checks",
    "configuracoes",
]

async def main():
    print(f"\n🔌 Conectando em: {MONGO_URI}")
    print(f"📦 Banco alvo: {DB_NAME}\n")

    client = AsyncIOMotorClient(MONGO_URI)
    db = client[DB_NAME]

    existing = await db.list_collection_names()

    for col in TARGET_COLLECTIONS:
        if col in existing:
            print(f"✔ Já existe: {col}")
        else:
            await db.create_collection(col)
            print(f"✅ Criada: {col}")

    print("\n🎯 Collections validadas com sucesso")

if __name__ == "__main__":
    asyncio.run(main())
