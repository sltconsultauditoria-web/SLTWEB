import re
from pathlib import Path

routers_dir = Path("../routers")

methods = ["get", "post", "put", "delete"]

print("\n🔎 AUDITORIA COMPLETA DO BACKEND\n")

routers = list(routers_dir.glob("*.py"))

total_endpoints = 0

for router_file in routers:

    if router_file.name == "__init__.py":
        continue

    name = router_file.stem

    content = router_file.read_text(encoding="utf-8")

    print(f"\n📦 Router: {name}")

    router_methods = {}

    for method in methods:

        pattern = f"@router.{method}"

        matches = re.findall(pattern, content)

        router_methods[method] = len(matches)

        total_endpoints += len(matches)

    for m, count in router_methods.items():

        if count > 0:
            print(f"   {m.upper():6} -> {count}")
        else:
            print(f"   {m.upper():6} -> ❌ ausente")

    crud_missing = []

    if router_methods["get"] == 0:
        crud_missing.append("GET")

    if router_methods["post"] == 0:
        crud_missing.append("POST")

    if router_methods["put"] == 0:
        crud_missing.append("PUT")

    if router_methods["delete"] == 0:
        crud_missing.append("DELETE")

    if crud_missing:
        print("   ⚠ CRUD incompleto:", ", ".join(crud_missing))
    else:
        print("   ✅ CRUD completo")

print("\n--------------------------------")

print(f"Routers analisados: {len(routers)-1}")
print(f"Total endpoints encontrados: {total_endpoints}")

print("\n🏁 Auditoria finalizada\n")