# fix_backend_all.py
import os

BACKEND_SRC = r"C:\Users\admin-local\ServerApp\consultSLTweb\backend"

def ensure_get_database():
    db_path = os.path.join(BACKEND_SRC, "core", "database.py")
    with open(db_path, encoding="utf-8", errors="ignore") as f:
        content = f.read()
    if "def get_database" not in content:
        with open(db_path, "a", encoding="utf-8") as f:
            f.write("""

def get_database():
    \"\"\"Retorna o objeto de conexão com o banco consultslt_db\"\"\"
    return database
""")
        print(f"✅ Função get_database adicionada em {db_path}")
    else:
        print("ℹ️ Função get_database já existe")

def ensure_app_defined():
    main_path = os.path.join(BACKEND_SRC, "main_enterprise.py")
    if os.path.exists(main_path):
        with open(main_path, encoding="utf-8", errors="ignore") as f:
            content = f.read()
        if "app = FastAPI()" not in content:
            new_content = f"""from fastapi import FastAPI
from backend.api import api_router

app = FastAPI()
app.include_router(api_router, prefix="/api")

""" + content
            with open(main_path, "w", encoding="utf-8") as f:
                f.write(new_content)
            print(f"✅ app definido em {main_path}")
        else:
            print("ℹ️ app já definido em main_enterprise.py")

def main():
    print("🔎 Corrigindo backend...\n")
    ensure_get_database()
    ensure_app_defined()
    print("\n🎯 Correções aplicadas. O backend deve iniciar sem erros de importação ou NameError.")

if __name__ == "__main__":
    main()
