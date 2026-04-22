from pymongo import MongoClient
from pprint import pprint

MONGO_URL = "mongodb://localhost:27017"

client = MongoClient(MONGO_URL)

SOURCE_DB = "consult_slt"
TARGET_DB = "consultslt_db"

print("\n=== DATABASES ===")

dbs = client.list_database_names()

for db in dbs:
    print(db)

print("\n=== ANALISANDO DATABASES ===")

source = client[SOURCE_DB]
target = client[TARGET_DB]

source_collections = source.list_collection_names()
target_collections = target.list_collection_names()

print("\n=== COLLECTIONS consult_slt ===")

for col in sorted(source_collections):

    count = source[col].count_documents({})

    print(f"{col} -> {count}")

print("\n=== COLLECTIONS consultslt_db ===")

for col in sorted(target_collections):

    count = target[col].count_documents({})

    print(f"{col} -> {count}")

print("\n=== COLLECTIONS FALTANDO NO consultslt_db ===")

missing = set(source_collections) - set(target_collections)

for col in missing:

    print(col)

print("\n=== COLLECTIONS EXTRAS consultslt_db ===")

extra = set(target_collections) - set(source_collections)

for col in extra:

    print(col)

print("\n=== COMPARANDO COUNTS ===")

common = set(source_collections).intersection(target_collections)

for col in sorted(common):

    s = source[col].count_documents({})
    t = target[col].count_documents({})

    if s != t:

        print(f"{col}")

        print(f" consult_slt -> {s}")

        print(f" consultslt_db -> {t}")

print("\n=== ANALISE USUARIOS ===")

users = target["usuarios"].find_one()

if users:

    print("\nCampos encontrados:")

    for k in users.keys():

        print(k)

print("\n=== INDEXES usuarios ===")

indexes = target["usuarios"].index_information()

pprint(indexes)

print("\n=== RECOMENDAÇÕES ===")

print("""

1 manter apenas consultslt_db

2 migrar collections faltantes

3 criar index email usuarios

4 remover campos password plain

5 garantir hashed_password

6 validar perfil admin

7 criar unique index email

""")

print("\n=== AUDITORIA FINALIZADA ===")