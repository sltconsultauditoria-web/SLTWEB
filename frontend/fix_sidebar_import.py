# fix_sidebar_import.py
import os

FRONTEND_SRC = r"C:\Users\admin-local\ServerApp\consultSLTweb\frontend\src"

def fix_sidebar_import():
    sidebar_path = os.path.join(FRONTEND_SRC, "components", "Layout", "Sidebar.jsx")
    if os.path.exists(sidebar_path):
        with open(sidebar_path, encoding="utf-8", errors="ignore") as f:
            content = f.read()

        new_content = content.replace("import API from '../api.js'", "import API from '../../api.js'")

        if new_content != content:
            with open(sidebar_path, "w", encoding="utf-8") as f:
                f.write(new_content)
            print(f"✅ Corrigido: {sidebar_path}")
        else:
            print(f"ℹ️ Nenhuma alteração necessária em {sidebar_path}")

def main():
    print("🔎 Ajustando import de API em Sidebar.jsx...\n")
    fix_sidebar_import()
    print("\n🎯 Import corrigido. Agora o Sidebar deve encontrar corretamente o arquivo api.js.")

if __name__ == "__main__":
    main()
