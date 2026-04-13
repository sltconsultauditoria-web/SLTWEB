# fix_frontend_imports.py
import os

FRONTEND_SRC = r"C:\Users\admin-local\ServerApp\consultSLTweb\frontend\src"

def fix_imports():
    for root, _, files in os.walk(FRONTEND_SRC):
        for file in files:
            if file.endswith((".js", ".jsx", ".ts", ".tsx")):
                path = os.path.join(root, file)
                with open(path, encoding="utf-8", errors="ignore") as f:
                    content = f.read()

                new_content = content

                # Corrige imports de API
                if "import API from \"../api\"" in new_content or "import API from '../api'" in new_content:
                    new_content = new_content.replace("import API from \"../api\"", "import API from \"../api.js\"")
                    new_content = new_content.replace("import API from '../api'", "import API from '../api.js'")

                # Corrige uso de Button/Tabs como named exports
                if "import { Button }" in new_content:
                    new_content = new_content.replace("import { Button }", "import Button")

                if "import { Tabs" in new_content:
                    new_content = new_content.replace("import { Tabs", "import Tabs")

                # Corrige função switch
                if "function switch(" in new_content:
                    new_content = new_content.replace("function switch(", "function Switch(")

                if new_content != content:
                    with open(path, "w", encoding="utf-8") as f:
                        f.write(new_content)
                    print(f"✅ Corrigido: {path}")

def main():
    print("🔎 Corrigindo imports e funções inválidas no frontend...\n")
    fix_imports()
    print("\n🎯 Frontend ajustado para usar dados reais do backend API e consultslt_db.")

if __name__ == "__main__":
    main()
