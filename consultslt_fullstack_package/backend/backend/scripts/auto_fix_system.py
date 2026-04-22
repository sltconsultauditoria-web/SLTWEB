import os
from pymongo import MongoClient

print("\n🚀 AUTO FIX CONSULT SLT SYSTEM\n")

ROOT = "../../"
ROUTER_DIR = "../../backend/routers"

# --------------------------------------------------
# MongoDB
# --------------------------------------------------

client = MongoClient("mongodb://localhost:27017")
db = client["consultslt_db"]

collections = db.list_collection_names()

print("\n📦 Coleções encontradas:")

for c in collections:
    print(" ", c)

# --------------------------------------------------
# Routers existentes
# --------------------------------------------------

routers = []

for file in os.listdir(ROUTER_DIR):

    if file.endswith(".py"):

        name = file.replace(".py","")

        if name != "__init__":
            routers.append(name)

print("\n⚙ Routers existentes:")

for r in routers:
    print(" ", r)

# --------------------------------------------------
# Criar routers faltantes
# --------------------------------------------------

print("\n🔧 Criando routers faltantes\n")

for col in collections:

    if col not in routers:

        path = f"{ROUTER_DIR}/{col}.py"

        print("Criando router:", col)

        code = f'''
from fastapi import APIRouter
from database import db

router = APIRouter(prefix="/api/{col}", tags=["{col}"])

@router.get("/")
async def listar():
    return list(db["{col}"].find({{}}, {{"_id":0}}))

@router.post("/")
async def criar(data: dict):
    db["{col}"].insert_one(data)
    return {{"status":"ok"}}
'''

        with open(path,"w",encoding="utf8") as f:
            f.write(code)

# --------------------------------------------------
# Remover router duplicado users
# --------------------------------------------------

users_path = f"{ROUTER_DIR}/users.py"

if os.path.exists(users_path):

    print("\n⚠ removendo router duplicado users.py")

    os.remove(users_path)

# --------------------------------------------------
# Criar router dashboard
# --------------------------------------------------

dashboard_path = f"{ROUTER_DIR}/dashboard.py"

print("\n📊 Criando router dashboard")

dashboard_code = '''
from fastapi import APIRouter
from database import db

router = APIRouter(prefix="/api/dashboard", tags=["dashboard"])

@router.get("/")
async def dashboard():

    empresas = db.empresas.count_documents({})
    alertas = db.alertas.count_documents({"lido":False})
    obrigacoes = db.obrigacoes_empresa.count_documents({"status":"pendente"})

    return {
        "empresas": empresas,
        "alertas": alertas,
        "obrigacoes_pendentes": obrigacoes
    }
'''

with open(dashboard_path,"w",encoding="utf8") as f:
    f.write(dashboard_code)

# --------------------------------------------------
# Criar índices Mongo
# --------------------------------------------------

print("\n📈 Criando índices Mongo\n")

important_fields = [
    "cnpj",
    "empresa_id",
    "created_at",
    "updated_at",
    "status"
]

for col in collections:

    collection = db[col]

    indexes = collection.index_information()

    existing = []

    for idx in indexes.values():

        if "key" in idx:

            for k in idx["key"]:
                existing.append(k[0])

    for field in important_fields:

        if field not in existing:

            try:

                collection.create_index(field)

                print(f"✔ índice criado: {col}.{field}")

            except:

                pass

print("\n🏁 AUTO FIX FINALIZADO\n")