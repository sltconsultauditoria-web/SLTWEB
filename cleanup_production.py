from pymongo import MongoClient
from datetime import datetime

client = MongoClient("mongodb://localhost:27017")

old_db = client["consult_slt"]
db = client["consultslt_db"]

print("\n==============================")
print("🚀 LIMPEZA PRODUÇÃO INICIADA")
print("==============================\n")

# ==========================================
# 1. CONSOLIDAÇÃO
# ==========================================

mapping = {
    "auditoria": "auditorias",
    "ocr": "ocr_documentos",
    "dashboard": "dashboard_metrics",
    "health": "health_check",
    "sharepoint": "sharepoint_status",
    "obrigacoes_fiscais": "obrigacoes"
}

for old, new in mapping.items():

    if old not in old_db.list_collection_names():
        continue

    docs = list(old_db[old].find())

    if not docs:
        continue

    print(f"🔄 Migrando {old} -> {new}")

    for d in docs:
        d.pop("_id", None)

    db[new].insert_many(docs)

    print(f"✅ {len(docs)} registros migrados")

# ==========================================
# 2. LIMPEZA USUARIOS
# ==========================================

print("\n🔧 Corrigindo usuários...\n")

usuarios = list(db["usuarios"].find())

for u in usuarios:

    update = {}

    # padronização
    if "ativo" in u:
        update["is_active"] = u["ativo"]

    if "role" in u:
        update["perfil"] = u["role"]

    # remover campos errados
    remove_fields = [
        "password",
        "password_hash",
        "username",
        "role",
        "ativo"
    ]

    for f in remove_fields:
        if f in u:
            update[f] = None

    # garantir campos
    if "is_active" not in u:
        update["is_active"] = True

    if "primeiro_login" not in u:
        update["primeiro_login"] = False

    if "created_at" not in u:
        update["created_at"] = datetime.utcnow()

    if update:
        db["usuarios"].update_one(
            {"_id": u["_id"]},
            {
                "$set": {
                    k: v for k, v in update.items() if v is not None
                },
                "$unset": {
                    k: "" for k, v in update.items() if v is None
                }
            }
        )

print("✅ Usuários corrigidos")

# ==========================================
# 3. VALIDAR HASH SENHA
# ==========================================

print("\n🔐 Validando senhas...")

invalid_users = db["usuarios"].count_documents({
    "hashed_password": {"$exists": False}
})

if invalid_users > 0:
    print(f"⚠️ {invalid_users} usuários sem senha hash")

print("✅ Verificação concluída")

# ==========================================
# 4. INDEXES
# ==========================================

print("\n📌 Criando índices...")

db["usuarios"].create_index("email", unique=True)

print("✅ Índice email criado")

# ==========================================
# 5. ADMIN DEFAULT
# ==========================================

print("\n👑 Verificando admin...")

admin = db["usuarios"].find_one({"email": "admin@empresa.com"})

if not admin:

    db["usuarios"].insert_one({
        "nome": "Administrador",
        "email": "admin@empresa.com",
        "hashed_password": "$2b$12$78cVzhSFnNOub4oA1uq9N.zx6zUIRKX98JLyANowdtkyCZMja8v3e",
        "perfil": "admin",
        "is_active": True,
        "primeiro_login": True,
        "created_at": datetime.utcnow()
    })

    print("✅ Admin criado")
else:
    print("✔ Admin já existe")

# ==========================================
# 6. REMOVER DATABASES ANTIGOS
# ==========================================

print("\n🧹 Limpando databases...")

if "consult_slt" in client.list_database_names():
    client.drop_database("consult_slt")
    print("🗑 consult_slt removido")

if "test" in client.list_database_names():
    client.drop_database("test")
    print("🗑 test removido")

# ==========================================
# 7. STATUS FINAL
# ==========================================

print("\n📊 STATUS FINAL:\n")

for col in db.list_collection_names():

    count = db[col].count_documents({})

    print(f"{col} -> {count}")

print("\n==============================")
print("✅ SISTEMA PRONTO PARA PRODUÇÃO")
print("==============================\n")