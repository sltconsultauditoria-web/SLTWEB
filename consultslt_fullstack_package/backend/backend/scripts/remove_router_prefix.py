import re
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
ROUTERS_DIR = BASE_DIR / "routers"

print("\n🔧 REMOVENDO PREFIXOS DOS ROUTERS\n")

count = 0

for file in ROUTERS_DIR.glob("*.py"):

    if file.name == "__init__.py":
        continue

    content = file.read_text(encoding="utf-8")

    new_content = re.sub(
        r'APIRouter\((.*?)prefix\s*=\s*["\'].*?["\'](.*?)\)',
        r'APIRouter(\1\2)',
        content,
        flags=re.S
    )

    if new_content != content:

        file.write_text(new_content, encoding="utf-8")
        print("✔ corrigido:", file.name)
        count += 1

print("\nTotal corrigido:", count)
print("\n🏁 Correção finalizada\n")