import os

routers_dir = "backend/routers"

crud_templates = {
    "create": """@app.post("/api/{resource}/create")
def create_{resource}(item: dict):
    session = db_session()
    obj = {Resource}(**item)
    session.add(obj)
    session.commit()
    return {{"success": True, "id": obj.id}}""",

    "read": """@app.get("/api/{resource}/read")
def read_{resource}():
    session = db_session()
    items = session.query({Resource}).all()
    return [i.to_dict() for i in items]""",

    "update": """@app.put("/api/{resource}/update/{id}")
def update_{resource}(id: int, item: dict):
    session = db_session()
    obj = session.query({Resource}).get(id)
    for k, v in item.items():
        setattr(obj, k, v)
    session.commit()
    return {{"success": True}}""",

    "delete": """@app.delete("/api/{resource}/delete/{id}")
def delete_{resource}(id: int):
    session = db_session()
    obj = session.query({Resource}).get(id)
    session.delete(obj)
    session.commit()
    return {{"success": True}}"""
}

def padronizar_crud():
    for root, _, files in os.walk(routers_dir):
        for file in files:
            if file.endswith(".py") and file != "__init__.py":
                path = os.path.join(root, file)
                resource = file.replace(".py", "")
                Resource = resource.capitalize()  # Ex.: empresas -> Empresas

                try:
                    with open(path, encoding="utf-8") as f:
                        content = f.read()

                    new_content = content
                    for metodo, template in crud_templates.items():
                        rota = f"/api/{resource}/{metodo}"
                        if rota not in new_content:
                            stub = "\n\n" + template.format(resource=resource, Resource=Resource)
                            new_content += stub

                    if new_content != content:
                        with open(path, "w", encoding="utf-8") as f:
                            f.write(new_content)
                        print(f"✔ CRUD conectado ao banco em {path}")
                except Exception as e:
                    print(f"Erro ao processar {path}: {e}")

if __name__ == "__main__":
    padronizar_crud()
    print("✅ CRUD padronizado e conectado ao consultslt_db")
