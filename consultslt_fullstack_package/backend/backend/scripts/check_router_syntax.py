import py_compile
from pathlib import Path

routers_dir = Path("../routers")

print("\n🔎 Verificando sintaxe dos routers\n")

for file in routers_dir.glob("*.py"):

    try:
        py_compile.compile(file, doraise=True)
        print(f"✅ OK: {file.name}")

    except Exception as e:
        print(f"❌ ERRO: {file.name}")
        print(e)
        print()

print("🏁 Verificação finalizada")