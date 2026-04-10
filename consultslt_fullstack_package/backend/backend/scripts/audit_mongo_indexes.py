from pymongo import MongoClient

print("\n🔎 AUDITORIA DE ÍNDICES MONGODB\n")

MONGO_URL = "mongodb://localhost:27017"
DB_NAME = "consultslt_db"

client = MongoClient(MONGO_URL)
db = client[DB_NAME]

# campos que normalmente precisam de índice
CRITICAL_FIELDS = [
    "cnpj",
    "cpf",
    "empresa_id",
    "usuario_id",
    "data",
    "created_at",
    "updated_at",
    "status",
]

collections = db.list_collection_names()

print(f"\n📦 Total de coleções: {len(collections)}\n")

for col in collections:

    print("--------------------------------------------------")
    print(f"\n📂 Coleção: {col}")

    collection = db[col]

    indexes = list(collection.list_indexes())

    print(f"\nÍndices existentes: {len(indexes)}")

    indexed_fields = []

    for idx in indexes:

        name = idx["name"]
        keys = idx["key"]

        fields = list(keys.keys())

        indexed_fields.extend(fields)

        print(f"   {name} -> {fields}")

    # verificar campos críticos
    sample = collection.find_one()

    if not sample:
        print("\n⚠ coleção vazia")
        continue

    missing = []

    for field in CRITICAL_FIELDS:

        if field in sample and field not in indexed_fields:
            missing.append(field)

    if missing:

        print("\n⚠ campos importantes sem índice:")

        for m in missing:
            print(f"   {m}")

    else:
        print("\n✅ índices principais OK")

print("\n🏁 Auditoria finalizada\n")