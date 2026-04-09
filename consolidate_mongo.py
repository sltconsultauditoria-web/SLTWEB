from pymongo import MongoClient

client = MongoClient("mongodb://localhost:27017")

old_db = client["consult_slt"]
new_db = client["consultslt_db"]

mapping = {

    "auditoria":"auditorias",
    "ocr":"ocr_documentos",
    "dashboard":"dashboard_metrics",
    "health":"health_check",
    "auth":"usuarios_backup",
    "auth_entra":"usuarios_backup",
    "sharepoint":"sharepoint_status",
    "obrigacoes_fiscais":"obrigacoes"

}

print("\n=== CONSOLIDAÇÃO INICIADA ===\n")

for old_name,new_name in mapping.items():

    if old_name not in old_db.list_collection_names():

        continue

    docs = list(old_db[old_name].find())

    if not docs:

        continue

    print(f"Migrando {old_name} -> {new_name}")

    for d in docs:

        d.pop("_id",None)

    new_db[new_name].insert_many(docs)

    print(f"{len(docs)} registros migrados")

print("\n=== CONSOLIDAÇÃO FINALIZADA ===")