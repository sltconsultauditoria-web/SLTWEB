from backend.core.database import get_db
from backend.utils.auth_utils import hash_password
import asyncio

users = [
    {
        "nome": "Administrador Padrão",
        "email": "admin@empresa.com",
        "password": "admin123",
        "perfil": "ADMIN",
        "primeiro_login": True
    },
    {
        "nome": "William Lucas",
        "email": "william.lucas@sltconsult.com.br",
        "password": "slt@2024",
        "perfil": "ADMIN",
        "primeiro_login": False
    },
    {
        "nome": "Super Administrador",
        "email": "admin@consultslt.com.br",
        "password": "Admin@123",
        "perfil": "SUPER_ADMIN",
        "primeiro_login": False
    }
]

async def seed_users():
    db = get_db()
    for user in users:
        existing_user = await db["users"].find_one({"email": user["email"]})
        if not existing_user:
            user["password"] = hash_password(user["password"])
            await db["users"].insert_one(user)
            print(f"Usuário {user['email']} inserido com sucesso.")
        else:
            print(f"Usuário {user['email']} já existe no banco de dados.")

if __name__ == "__main__":
    asyncio.run(seed_users())