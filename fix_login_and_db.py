from pymongo import MongoClient
from passlib.context import CryptContext

print("=" * 60)
print("FIX LOGIN + BANCO SLTWEB")
print("=" * 60)

# ------------------------------------------
# CONFIG
# ------------------------------------------
MONGO_URL = "mongodb://localhost:27017"
DB_NAME = "consultslt_db"

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

client = MongoClient(MONGO_URL)
db = client[DB_NAME]

usuarios = db["usuarios"]

# ------------------------------------------
# USUÁRIOS PARA CORRIGIR
# ------------------------------------------
users_to_fix = [
    ("admin@consultslt.com.br", "admin123"),
    ("william.lucas@sltconsult.com.br", "123456"),
    ("admin@empresa.com", "admin123"),
]

# ------------------------------------------
# UPDATE
# ------------------------------------------
for email, senha in users_to_fix:

    hashed = pwd_context.hash(senha)

    result = usuarios.update_one(
        {"email": email},
        {
            "$set": {
                "hashed_password": hashed,
                "is_active": True
            }
        }
    )

    if result.matched_count:
        print(f"✅ Atualizado: {email}")
    else:
        print(f"❌ Não encontrado: {email}")

print("\n✔ Senhas resetadas com sucesso")
print("👉 Teste agora o login no frontend")
print("=" * 60)