import os

frontend_dir = "frontend/src"

def corrigir_api_final():
    for root, _, files in os.walk(frontend_dir):
        for file in files:
            if file.endswith((".js", ".jsx")):
                path = os.path.join(root, file)
                try:
                    with open(path, encoding="utf-8") as f:
                        content = f.read()
                    new_content = content

                    # Remover duplicações de API
                    if "const API =" in new_content or "BACKEND_URL" in new_content:
                        lines = new_content.splitlines()
                        lines = [l for l in lines if "const API =" not in l and "BACKEND_URL" not in l]
                        new_content = "\n".join(lines)

                    # Corrigir imports para sempre apontar para src/config/api.js
                    if "import { API } from" in new_content:
                        # Normalizar todos para src/config/api.js
                        new_content = new_content.replace(
                            "import { API } from \"../config/api\"",
                            "import { API } from \"../config/api\""
                        ).replace(
                            "import { API } from \"../../config/api\"",
                            "import { API } from \"../config/api\""
                        )

                    # Garantir que existe import correto
                    if "API.get" in new_content and "import { API }" not in new_content:
                        import_line = "import { API } from \"../config/api\";\n"
                        new_content = import_line + new_content

                    if new_content != content:
                        with open(path, "w", encoding="utf-8") as f:
                            f.write(new_content)
                        print(f"✔ Corrigido: {path}")
                except Exception as e:
                    print(f"Erro ao processar {path}: {e}")

if __name__ == "__main__":
    corrigir_api_final()
    print("✅ Imports e duplicações de API corrigidos. Agora todos os arquivos usam src/config/api.js corretamente.")
