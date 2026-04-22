from motor.motor_asyncio import AsyncIOMotorClient

async def suggest_indexes():
    client = AsyncIOMotorClient("mongodb://localhost:27017")
    db = client["consultslt_db"]

    suggestions = {
        "users": ["email"],
        "usuarios": ["email", "perfil"],
        "relatorios": ["ativo"],
        "relatorios_gerados": ["data_criacao"],
        "tipos_documentos": ["nome"],
        "tipos_obrigacoes": ["nome"],
        "tipos_relatorios": ["nome"]
    }

    for collection, fields in suggestions.items():
        for field in fields:
            print(f"Sugestão: Criar índice em '{field}' na coleção '{collection}'")

if __name__ == "__main__":
    import asyncio
    asyncio.run(suggest_indexes())