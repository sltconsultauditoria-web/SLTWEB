from motor.motor_asyncio import AsyncIOMotorClient
import asyncio

async def check_users():
    client = AsyncIOMotorClient("mongodb://localhost:27017")
    db = client["consultslt_db"]

    users = await db.users.find().to_list(100)
    if not users:
        print("Nenhum usuário encontrado na coleção 'users'.")
    else:
        print("Usuários encontrados:")
        for user in users:
            print(user)

if __name__ == "__main__":
    asyncio.run(check_users())