import asyncio
import bcrypt
import logging
from motor.motor_asyncio import AsyncIOMotorClient

# --- CONFIGURAÇÕES ---
MONGO_URI = "mongodb://localhost:27017"
DB_NAME = "consultslt_db"

# --- LISTA DE USUÁRIOS E SENHAS PADRÃO ---
USERS_TO_SYNC = [
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

def hash_password(password: str) -> str:
    """Gera o hash da senha usando bcrypt compatível com FastAPI."""
    return bcrypt.hashpw(
        password.encode("utf-8"),
        bcrypt.gensalt(12)
    ).decode("utf-8")

def verify_password(password: str, hashed_password: str) -> bool:
    """Verifica se a senha plana coincide com o hash do banco."""
    try:
        return bcrypt.checkpw(
            password.encode("utf-8"),
            hashed_password.encode("utf-8")
        )
    except Exception:
        return False

async def sync_users():
    print(f"\n🔄 INICIANDO SINCRONIZAÇÃO DE USUÁRIOS E SENHAS SLTWEB\n")
    print("-" * 70)

    client = AsyncIOMotorClient(MONGO_URI)
    db = client[DB_NAME]
    
    results = []

    for user_data in USERS_TO_SYNC:
        email = user_data["email"]
        plain_password = user_data["password"]
        
        # 1. Busca o usuário no banco (Coleção 'usuarios')
        user = await db.usuarios.find_one({"email": email})
        
        if not user:
            print(f"⚠️ AVISO: Usuário '{email}' não encontrado no banco. Criando agora...")
            # Criação do usuário caso não exista
            new_user = {
                "nome": user_data["nome"],
                "email": email,
                "hashed_password": hash_password(plain_password),
                "perfil": user_data["perfil"],
                "is_active": True,
                "ativo": True,
                "primeiro_login": user_data["primeiro_login"]
            }
            await db.usuarios.insert_one(new_user)
            print(f"✅ Usuário '{email}' criado com sucesso.")
            results.append({"email": email, "status": "CRIADO", "senha": plain_password})
            continue

        # 2. Verifica se a senha atual no banco é válida
        current_hash = user.get("hashed_password") or user.get("senha_hash") or user.get("password")
        
        if current_hash and verify_password(plain_password, current_hash):
            print(f"✅ OK: Senha do usuário '{email}' já está sincronizada.")
            results.append({"email": email, "status": "OK", "senha": plain_password})
        else:
            print(f"🔄 ATUALIZANDO: Senha do usuário '{email}' incorreta ou hash antigo. Sincronizando...")
            new_hash = hash_password(plain_password)
            await db.usuarios.update_one(
                {"email": email},
                {
                    "$set": {
                        "hashed_password": new_hash,
                        "perfil": user_data["perfil"],
                        "ativo": True,
                        "is_active": True,
                        "primeiro_login": user_data["primeiro_login"]
                    }
                }
            )
            print(f"✅ Senha do usuário '{email}' sincronizada com sucesso.")
            results.append({"email": email, "status": "SINCRONIZADO", "senha": plain_password})

    # Relatório Final
    print("\n" + "="*70)
    print(f"{'E-MAIL':<35} | {'STATUS':<15} | {'SENHA ATIVA'}")
    print("-" * 70)
    for res in results:
        print(f"{res['email']:<35} | {res['status']:<15} | {res['senha']}")
    print("="*70)
    print("\n💡 Agora todos os usuários acima podem logar no sistema com status 200 OK!")

if __name__ == "__main__":
    asyncio.run(sync_users())