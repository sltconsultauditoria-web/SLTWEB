import os
import json

BASE = os.getcwd()

def find_main_package():
    for root, dirs, files in os.walk(BASE):
        if "node_modules" in root:
            continue

        if "package.json" in files:
            return os.path.join(root, "package.json")

    return None

pkg = find_main_package()

print("\n===================")
print("DIAGNÓSTICO REAL")
print("===================")

if pkg:
    print("package.json:", pkg)

    with open(pkg, "r", encoding="utf-8") as f:
        data = json.load(f)

    deps = {
        **data.get("dependencies", {}),
        **data.get("devDependencies", {})
    }

    for item in [
        "react",
        "react-dom",
        "react-router-dom",
        "tailwindcss",
        "vite"
    ]:
        print(item, "✅" if item in deps else "❌")

else:
    print("package.json não encontrado")

print("\nROTAS CORRETAS:")
print("/")
print("/login")
print("/dashboard")

print("\nSe acessar /SLTWEB dará tela branca.")