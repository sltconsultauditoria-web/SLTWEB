# fix_backend_database_imports.py
import os

BACKEND_SRC = r"C:\Users\admin-local\ServerApp\consultSLTweb\backend"

def ensure_get_database_function():
    db_path = os.path.join(BACKEND_SRC, "core", "database.py")
    with open(db_path, encoding="utf-8", errors="ignore") as f:
        content = f.read()

    if "def get_database" not in content:
        with open(db_path, "a", encoding="utf-8") as f:
            f.write("""

def get_database():
    \"\"\"Retorna o objeto de conexão com o banco MongoDB\"\"\"
    return database
""")
        print(f"✅ Função get_database adicionada em {db_path}")
    else:
        print(f"ℹ️ Função get_database já existe em {db_path}")

def main():
    print("🔎 Corrigindo backend...\n")
    ensure_get_database_function()
    print("\n🎯 Correção aplicada. O backend deve iniciar sem erro de importação.")

if __name__ == "__main__":
    main()
