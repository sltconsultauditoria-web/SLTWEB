import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

REPLACEMENTS = {
    "from backend.schemas.": "from backend.schemas.",
    "from backend.repositories.": "from backend.repositories.",
    "from backend.core.": "from backend.core.",
    "from backend.models.": "from backend.models.",
}

def process_file(filepath):
    with open(filepath, "r", encoding="utf-8") as f:
        content = f.read()

    original = content

    for old, new in REPLACEMENTS.items():
        content = content.replace(old, new)

    if content != original:
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(content)
        print(f"✔ Corrigido: {filepath}")

def scan_directory(directory):
    for root, dirs, files in os.walk(directory):
        # Ignorar venv e analysis
        if "venv" in root or "analysis" in root or "backup" in root:
            continue

        for file in files:
            if file.endswith(".py"):
                process_file(os.path.join(root, file))


if __name__ == "__main__":
    scan_directory(BASE_DIR)
    print("\n✅ Imports corrigidos com sucesso.")
