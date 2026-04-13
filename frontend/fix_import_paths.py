# fix_import_paths.py
import os

FRONTEND_SRC = r"C:\Users\admin-local\ServerApp\consultSLTweb\frontend\src"

def fix_api_imports():
    for root, _, files in os.walk(FRONTEND_SRC):
        for file in files:
            if file.endswith((".js", ".jsx")):
                path = os.path.join(root, file)
                with open(path, encoding="utf-8", errors="ignore") as f:
                    content = f.read()

                new_content = content
                # Corrige imports quebrados
                new_content = new_content.replace("import API from '../api.js'", "import API from '../api.js'")
                new_content = new_content.replace("import API from '../../api.js'", "import API from '../../api.js'")
                new_content = new_content.replace("import API from '../../../api.js'", "import API from '../../../api.js'")

                if new_content != content:
                    with open(path, "w", encoding="utf-8") as f:
                        f.write(new_content)
                    print(f"✅ Corrigido: {path}")

def main():
    print("🔎 Ajustando imports de API...\n")
    fix_api_imports()
    print("\n🎯 Imports corrigidos. Agora os componentes devem encontrar corretamente o arquivo api.js.")

if __name__ == "__main__":
    main()
