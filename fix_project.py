import os

frontend_dir = "frontend/src"
config_file = os.path.join(frontend_dir, "config", "api.js")

def ensure_api_config():
    os.makedirs(os.path.dirname(config_file), exist_ok=True)
    api_content = """import axios from "axios";

export const API = axios.create({
  baseURL: process.env.REACT_APP_API_URL
});
"""
    with open(config_file, "w", encoding="utf-8") as f:
        f.write(api_content)
    print(f"✔ Criado/atualizado: {config_file}")

def corrigir_imports():
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

                    # Corrigir imports para src/config/api.js
                    if "import { API } from" in new_content:
                        new_content = new_content.replace(
                            "import { API } from \"../config/api\"",
                            "import { API } from \"../config/api\""
                        ).replace(
                            "import { API } from \"../../config/api\"",
                            "import { API } from \"../config/api\""
                        )

                    # Corrigir uso incorreto de responseType
                    if "responseType:" in new_content and "API.get" not in new_content:
                        new_content = new_content.replace(
                            "responseType:", "await API.get(url, { responseType:"
                        )

                    if new_content != content:
                        with open(path, "w", encoding="utf-8") as f:
                            f.write(new_content)
                        print(f"✔ Corrigido: {path}")
                except Exception as e:
                    print(f"Erro ao processar {path}: {e}")

if __name__ == "__main__":
    ensure_api_config()
    corrigir_imports()
    print("✅ Projeto corrigido: imports ajustados, duplicações removidas e config/api.js criado.")
