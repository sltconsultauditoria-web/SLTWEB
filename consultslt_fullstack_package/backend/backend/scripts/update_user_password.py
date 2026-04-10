from motor.motor_asyncio import AsyncIOMotorClient
import asyncio

async def update_password():
    client = AsyncIOMotorClient("mongodb://localhost:27017")
    db = client["consultslt_db"]

    email = "admin@empresa.com"
    new_hashed_password = "$2b$12$.fkfnrkkxgm/O0mgDUBm0.K5X9eMfsn8aXGi5fmtOaAkvmSHUM582"

    result = await db.users.update_one(
        {"email": email},
        {"$set": {"password": new_hashed_password}}
    )

    if result.modified_count > 0:
        print(f"Senha atualizada com sucesso para o usuário: {email}")
    else:
        print(f"Falha ao atualizar a senha para o usuário: {email}")

if __name__ == "__main__":
    asyncio.run(update_password())