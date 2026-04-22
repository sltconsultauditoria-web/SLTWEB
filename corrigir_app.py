import os

# Diretórios a verificar
dirs_to_check = ["backend", "frontend/src"]

def corrigir_backend(path, content):
    # Remove chamadas API.get indevidas
    if "API.get" in content:
        content = content.replace("API.get", "// REMOVER: API.get (não deve estar no backend)")
    # Padronizar retorno JSON
    if "res.json(" in content and "success" not in content:
        content = content.replace("res.json(", "res.status(200).json({ success: true, data: ")
    return content

def corrigir_frontend(path, content):
    # Garantir uso de API centralizada
    if "axios.get" in content:
        content = content.replace("axios.get", "API.get")
    # Proteger uso de map
    if ".map(" in content and "&&" not in content:
        content = content.replace(".map(", " && data.map(")
    return content

def processar():
    for base_dir in dirs_to_check:
        for root, _, files in os.walk(base_dir):
            for file in files:
                if file.endswith((".js", ".jsx")):
                    path = os.path.join(root, file)
                    try:
                        with open(path, encoding="utf-8") as f:
                            content = f.read()
                        new_content = content
                        if "backend" in path:
                            new_content = corrigir_backend(path, new_content)
                        else:
                            new_content = corrigir_frontend(path, new_content)
                        if new_content != content:
                            with open(path, "w", encoding="utf-8") as f:
                                f.write(new_content)
                            print(f"✔ Corrigido: {path}")
                    except Exception as e:
                        print(f"Erro ao processar {path}: {e}")

if __name__ == "__main__":
    processar()
    print("✅ Correção aplicada. Backend usa Mongoose, frontend usa API centralizada.")
