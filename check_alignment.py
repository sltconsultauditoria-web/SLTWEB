import os
import re

backend_dir = "backend/src"
frontend_dir = "frontend/src"

def listar_rotas_backend():
    rotas = []
    for root, _, files in os.walk(backend_dir):
        for file in files:
            if file.endswith(".js"):
                path = os.path.join(root, file)
                try:
                    with open(path, encoding="utf-8") as f:
                        content = f.read()
                    # Captura app.use("/api/...") e router.get/post("/...")
                    matches = re.findall(r'app\.use\([\'"](/api/[a-zA-Z0-9_/]+)', content)
                    matches += re.findall(r'router\.(get|post|put|delete)\([\'"](/api/[a-zA-Z0-9_/]+)', content)
                    rotas.extend([m if isinstance(m, str) else m[1] for m in matches])
                except Exception:
                    pass
    return set(rotas)

def listar_chamadas_frontend():
    chamadas = []
    for root, _, files in os.walk(frontend_dir):
        for file in files:
            if file.endswith((".js", ".jsx")):
                path = os.path.join(root, file)
                try:
                    with open(path, encoding="utf-8") as f:
                        content = f.read()
                    matches = re.findall(r'API\.(get|post|put|delete)\([\'"](/api/[a-zA-Z0-9_/]+)', content)
                    chamadas.extend([m[1] for m in matches])
                except Exception:
                    pass
    return set(chamadas)

if __name__ == "__main__":
    backend_rotas = listar_rotas_backend()
    frontend_chamadas = listar_chamadas_frontend()

    print("📌 Rotas expostas pelo backend:")
    for r in backend_rotas:
        print(" -", r)

    print("\n📌 Chamadas feitas pelo frontend:")
    for c in frontend_chamadas:
        print(" -", c)

    print("\n📊 Comparação:")
    faltando = frontend_chamadas - backend_rotas
    extras = backend_rotas - frontend_chamadas

    if faltando:
        print("❌ Chamadas do frontend sem rota correspondente no backend:")
        for f in faltando:
            print(" -", f)
    else:
        print("✅ Todas as chamadas do frontend têm rota correspondente.")

    if extras:
        print("ℹ️ Rotas no backend que não estão sendo chamadas pelo frontend:")
        for e in extras:
            print(" -", e)
    else:
        print("✅ Todas as rotas do backend estão sendo usadas pelo frontend.")
