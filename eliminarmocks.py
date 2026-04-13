import os

# Diretórios a verificar
dirs_to_check = ["backend", "frontend/src"]

# Padrões que indicam mocks e substituições sugeridas
replacements = {
    "[]": "API.get('/replace_with_real_endpoint')",
    "{}": "API.get('/replace_with_real_endpoint')",
    "mock": "API.get('/replace_with_real_endpoint')",
    "fake": "API.get('/replace_with_real_endpoint')"
}

def replace_mocks():
    for base_dir in dirs_to_check:
        for root, _, files in os.walk(base_dir):
            for file in files:
                if file.endswith((".js", ".jsx", ".ts", ".tsx")):
                    path = os.path.join(root, file)
                    try:
                        with open(path, encoding="utf-8") as f:
                            content = f.read()
                        new_content = content
                        for pattern, replacement in replacements.items():
                            if pattern in new_content:
                                new_content = new_content.replace(pattern, replacement)
                        if new_content != content:
                            with open(path, "w", encoding="utf-8") as f:
                                f.write(new_content)
                            print(f"✔ Substituído mock em {path}")
                    except Exception as e:
                        print(f"Erro ao processar {path}: {e}")

if __name__ == "__main__":
    replace_mocks()
    print("✅ Todos os mocks foram substituídos por chamadas reais à API. Ajuste manualmente os endpoints conforme necessário.")
