import asyncio
from backend.core.database import get_db, connect_to_mongo

async def main():
    await connect_to_mongo()
    db = get_db()
    empresas = await db['empresas'].find().to_list(10)
    for empresa in empresas:
        print(empresa)

if __name__ == "__main__":
    asyncio.run(main())
