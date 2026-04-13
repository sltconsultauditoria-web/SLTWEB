import os

dirs_to_check = ["backend", "frontend/src"]

def scan_files():
    for base_dir in dirs_to_check:
        for root, _, files in os.walk(base_dir):
            for file in files:
                if file.endswith((".js", ".jsx")):
                    path = os.path.join(root, file)
                    try:
                        with open(path, encoding="utf-8") as f:
                            content = f.read()
                            if "API.get" in content and "frontend/src" not in path:
                                print(f"⚠️ {path} contém API.get (remover, não deve estar no backend)")
                    except Exception as e:
                        print(f"Erro ao ler {path}: {e}")

if __name__ == "__main__":
    scan_files()
