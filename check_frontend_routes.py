import os
import re
import json

BASE_DIR = os.getcwd()

print("\n==============================")
print("🔍 FRONTEND DIAGNOSTIC CHECK")
print("==============================")

# -------------------------
# FILE CHECK
# -------------------------
files = {
    "package.json": False,
    "src": False,
    "App.jsx": False,
    "main.jsx": False,
    "App.js": False,
    "main.js": False
}

for root, dirs, fs in os.walk(BASE_DIR):
    for f in fs:
        path = os.path.join(root, f)

        if f in files:
            files[f] = path

print("\n📁 Arquivos encontrados:")
for k, v in files.items():
    print(f"{k}: {v if v else '❌ não encontrado'}")

# -------------------------
# PACKAGE.JSON
# -------------------------
pkg_path = files["package.json"]

if pkg_path:
    print("\n📦 Verificando package.json...")

    with open(pkg_path, "r", encoding="utf-8") as f:
        pkg = json.load(f)

    deps = {
        **pkg.get("dependencies", {}),
        **pkg.get("devDependencies", {})
    }

    checks = {
        "react": "react" in deps,
        "react-dom": "react-dom" in deps,
        "react-router-dom": "react-router-dom" in deps,
        "vite": "vite" in deps or "vite" in str(deps),
        "tailwindcss": "tailwindcss" in deps
    }

    for k, v in checks.items():
        print(f"{k}: {'✅' if v else '❌'}")

# -------------------------
# FIND MAIN FILE
# -------------------------
main_file = files["main.jsx"] or files["main.js"]

if main_file:
    print("\n🚦 Verificando Router...")

    with open(main_file, "r", encoding="utf-8") as f:
        content = f.read()

    if "BrowserRouter" in content:
        print("✅ BrowserRouter encontrado")
    else:
        print("❌ BrowserRouter não encontrado")

    basename = re.findall(r'basename=["\'](.*?)["\']', content)
    if basename:
        print("✅ Basename:", basename[0])
    else:
        print("⚠️ Sem basename configurado")

# -------------------------
# FIND APP FILE
# -------------------------
app_file = files["App.jsx"] or files["App.js"]

if app_file:
    print("\n🛣 Verificando rotas...")

    with open(app_file, "r", encoding="utf-8") as f:
        content = f.read()

    routes = re.findall(r'path=["\'](.*?)["\']', content)

    if routes:
        print("Rotas encontradas:")
        for r in routes:
            print(" -", r)
    else:
        print("❌ Nenhuma rota encontrada")

    if "/SLTWEB" in routes:
        print("✅ Rota /SLTWEB existe")
    else:
        print("❌ Rota /SLTWEB não existe")

# -------------------------
# INDEX.HTML CHECK
# -------------------------
index_path = None

for root, dirs, fs in os.walk(BASE_DIR):
    for f in fs:
        if f == "index.html":
            index_path = os.path.join(root, f)

if index_path:
    print("\n🌐 Verificando index.html")

    with open(index_path, "r", encoding="utf-8") as f:
        html = f.read()

    if 'id="root"' in html:
        print("✅ div root encontrada")
    else:
        print("❌ div root não encontrada")

# -------------------------
# FINAL DIAGNOSIS
# -------------------------
print("\n==============================")
print("📋 POSSÍVEIS CAUSAS DA TELA BRANCA")
print("==============================")

print("""
1. Rota /SLTWEB não existe
2. BrowserRouter sem basename
3. App.jsx sem rotas válidas
4. Erro silencioso no componente LoginPage
5. React não montando no #root
6. Import quebrado
7. useEffect infinito no AuthContext
8. Axios travando renderização
""")

print("\n🚀 Execute:")
print("python check_frontend_routes.py")