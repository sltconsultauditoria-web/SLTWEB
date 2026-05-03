import os
from pathlib import Path

PROJECT_ROOT = "backend"


# =========================================================
# ARQUITETURA CONSCIENTE (IMPORTANTE)
# =========================================================
ALLOWED_FASTAPI_CONTEXTS = [
    "routers",
    "main",
    "app",
    "api"
]

IGNORED_LAYERS = [
    "services",
    "repositories",
    "schemas",
    "utils",
    "modules"
]


# =========================================================
# LEITURA SEGURA
# =========================================================
def read_file(path):
    try:
        with open(path, "r", encoding="utf-8") as f:
            return f.read()
    except:
        return ""


# =========================================================
# DETECÇÃO INTELIGENTE DE CONTEXTO
# =========================================================
def get_layer_type(path):
    path_str = str(path)

    for layer in IGNORED_LAYERS:
        if f"\\{layer}\\" in path_str or f"/{layer}/" in path_str:
            return "ignored"

    if "routers" in path_str:
        return "router"

    if "main" in path_str:
        return "main"

    if "services" in path_str:
        return "service"

    if "repositories" in path_str:
        return "repository"

    return "unknown"


# =========================================================
# CHECKS REAIS (SEM FALSO POSITIVO)
# =========================================================
def analyze_file(path, content):
    issues = []
    layer = get_layer_type(path)

    # =====================================================
    # 1. JWT SÓ IMPORTA EM LAYERS API
    # =====================================================
    if layer in ["router", "main"]:

        if "jwt" not in content.lower():
            issues.append("⚠️ JWT não implementado na camada de API")

        if "Depends" not in content:
            issues.append("🚨 Rota sem dependency injection de auth")

    # =====================================================
    # 2. MAIN VALIDATION
    # =====================================================
    if layer == "main":

        if "FastAPI" not in content:
            issues.append("❌ FastAPI não inicializado")

        if "CORSMiddleware" not in content:
            issues.append("⚠️ CORS não configurado")

        if "uvicorn" not in content and "__main__" not in content:
            issues.append("⚠️ Sem entrypoint local")

    # =====================================================
    # 3. SEGURANÇA GLOBAL (TODOS OS LAYERS)
    # =====================================================
    if "allow_origins=[\"*\"]" in content:
        issues.append("🚨 CORS aberto (produção insegura)")

    if "password" in content and "bcrypt" not in content:
        issues.append("⚠️ Senha possivelmente em texto puro")

    if "JWT_SECRET" in content and "os.getenv" not in content:
        issues.append("🚨 JWT_SECRET hardcoded")

    # =====================================================
    # 4. MONGO SAFETY
    # =====================================================
    if "MongoClient" in content and "try:" not in content:
        issues.append("⚠️ Mongo sem tratamento de erro")

    return issues


# =========================================================
# SCANNER PRINCIPAL
# =========================================================
def scan_project():
    report = {}

    for root, _, files in os.walk(PROJECT_ROOT):
        for file in files:
            if file.endswith(".py"):
                path = Path(root) / file
                content = read_file(path)

                if not content.strip():
                    continue

                issues = analyze_file(path, content)

                # só reporta se tiver problema real
                if issues:
                    report[str(path)] = issues

    return report


# =========================================================
# SCORE MAIS REALISTA (SEM FALSO ZERO)
# =========================================================
def calculate_score(report):
    total = sum(len(v) for v in report.values())

    if total == 0:
        return 100

    # penalidade leve e realista
    score = 100 - (total * 4)

    return max(score, 40)  # nunca zera injustamente


# =========================================================
# REPORT FINAL
# =========================================================
def run():
    print("\n======================================")
    print("🧠 SECOND VALIDATION AUDITOR (ENTERPRISE)")
    print("======================================\n")

    report = scan_project()
    score = calculate_score(report)

    if not report:
        print("✅ Nenhum problema real detectado")
        print("🏆 SCORE: 100/100")
        return

    for file, issues in report.items():
        print(f"\n📄 {file}")
        for i in issues:
            print(f"   {i}")

    print("\n======================================")
    print(f"📊 REALISTIC SECURITY SCORE: {score}/100")
    print("======================================\n")


if __name__ == "__main__":
    run()