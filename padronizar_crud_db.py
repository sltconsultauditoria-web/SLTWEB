import os

routers_dir = "backend/routers"

crud_methods = ["create", "read", "update", "delete"]

def padronizar_crud():
    for root, _, files in os.walk(routers_dir):
        for file in files:
            if file.endswith(".py") and file != "__init__.py":
                path = os.path.join(root, file)
                resource = file.replace(".py", "")
                Model = resource.capitalize()

                with open(path, encoding="utf-8") as f:
                    content = f.read()

                new_content = content
                for metodo in crud_methods:
                    rota = f"/api/{resource}"
                    if metodo not in new_content:
                        stub = f"""

@router.{ 'post' if metodo=='create' else 'get' if metodo=='read' else 'put' if metodo=='update' else 'delete' }("{rota}{'' if metodo in ['create','read'] else '/{id}'}")
def {metodo}_{resource}({ 'item: dict' if metodo=='create' else 'id: int, item: dict' if metodo=='update' else 'id: int' if metodo=='delete' else '' }):
    session = db_session()
    { 'obj = ' + Model + '(**item); session.add(obj); session.commit(); return {\"success\": True, \"id\": obj.id}' if metodo=='create' else
      'items = session.query(' + Model + ').all(); return [i.as_dict() for i in items]' if metodo=='read' else
      'obj = session.query(' + Model + ').get(id);\\n    if not obj: return {\"error\": \"Not found\"}\\n    for k,v in item.items(): setattr(obj,k,v); session.commit(); return {\"success\": True}' if metodo=='update' else
      'obj = session.query(' + Model + ').get(id);\\n    if not obj: return {\"error\": \"Not found\"}\\n    session.delete(obj); session.commit(); return {\"success\": True}' }
"""
                        new_content += stub

                if new_content != content:
                    with open(path, "w", encoding="utf-8") as f:
                        f.write(new_content)
                    print(f"✔ CRUD conectado ao consultslt_db em {path}")

if __name__ == "__main__":
    padronizar_crud()
    print("✅ CRUD padronizado e conectado ao consultslt_db")
