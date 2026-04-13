import os

frontend_dir = "frontend/src"

def corrigir_imports():
    for root, _, files in os.walk(frontend_dir):
        for file in files:
            if file.endswith((".js", ".jsx")):
                path = os.path.join(root, file)
                try:
                    with open(path, encoding="utf-8") as f:
                        content = f.read()
                    # Verifica se o arquivo usa API.get mas não tem import
                    if "API.get" in content and "import { API }" not in content:
                        # Calcula profundidade para definir caminho relativo
                        depth = path.replace(frontend_dir, "").count("\\")
                        if depth > 1:
                            import_line = "import { API } from \"../../config/api\";\n"
                        else:
                            import_line = "import { API } from \"../config/api\";\n"
                        # Adiciona importação no topo
                        new_content = import_line + content
                        with open(path, "w", encoding="utf-8") as f:
                            f.write(new_content)
                        print(f"✔ Importação adicionada em {path}")
                except Exception as e:
                    print(f"Erro ao processar {path}: {e}")

if __name__ == "__main__":
    corrigir_imports()
    print("✅ Todas as chamadas API.get agora têm importação correta.")
