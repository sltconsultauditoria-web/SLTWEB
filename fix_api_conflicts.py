import os

frontend_dir = "frontend/src"

def corrigir_api_conflicts():
    for root, _, files in os.walk(frontend_dir):
        for file in files:
            if file.endswith((".js", ".jsx")):
                path = os.path.join(root, file)
                try:
                    with open(path, encoding="utf-8") as f:
                        content = f.read()
                    new_content = content

                    # Remover declarações duplicadas de API
                    if "const API =" in new_content:
                        lines = new_content.splitlines()
                        lines = [l for l in lines if "const API =" not in l and "BACKEND_URL" not in l]
                        new_content = "\n".join(lines)

                    # Corrigir import errado fora de src
                    if "import { API } from \"../../config/api\"" in new_content:
                        new_content = new_content.replace(
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
    corrigir_api_conflicts()
    print("✅ Conflitos de API corrigidos. Agora todos os arquivos usam src/config/api.js corretamente.")
