from pathlib import Path
import re

routers_dir = Path("../routers")

print("\n🔧 Corrigindo sintaxe dos routers\n")

fixed = 0

for file in routers_dir.glob("*.py"):

    if file.name == "__init__.py":
        continue

    content = file.read_text(encoding="utf-8")

    # Corrigir APIRouter quebrado
    content_new = re.sub(
        r"router\s*=\s*APIRouter\s*\([^)]*\)",
        "router = APIRouter()",
        content
    )

    # Corrigir linhas soltas com vírgula
    content_new = re.sub(r"^\s*,\s*$", "", content_new, flags=re.MULTILINE)

    if content != content_new:

        file.write_text(content_new, encoding="utf-8")

        print(f"✔ corrigido: {file.name}")
        fixed += 1

print(f"\nTotal corrigido: {fixed}")
print("\n🏁 Correção finalizada\n")