import os
import re
from pathlib import Path

PROJECT_ROOT = "backend"


# =========================================================
# UTIL: leitura segura de arquivos
# =========================================================
def read_file(path):
    try:
        with open(path, "r", encoding="utf-8") as f:
            return f.read()
    except Exception as e:
        return f"__ERROR__: {e}"


# =========================================================
# ANALISADOR SIMPLES (SEM AST = MAIS SEGURO)
# =========================================================
def analyze_file(path, content):
    issues = []

    # ---------------------------
    # IMPORTS CRÍTICOS
    # ---------------------------
    if "import jwt" not in content and "pyjwt" not in content:
        issues.append("🚨 JWT não detectado")

    if "FastAPI" not in content:
        issues.append("⚠️ FastAPI não detectado")

    # ---------------------------
    # SEGURANÇA
    # ---------------------------
    if "allow_origins=[\"*\"]" in content:
        issues.append("🚨 CORS aberto (allow_origins='*')")

    if "password" in content and "bcrypt" not in content:
        issues.append("⚠️ Senhas possivelmente em texto puro")

    if "JWT_SECRET" in content and "os.getenv" not in content:
        issues.append("🚨 JWT_SECRET hardcoded")

    # ---------------------------
    # AUTENTICAÇÃO
    # ---------------------------
    if "@app.get" in content or "@app.post" in content:
        if "Depends" not in content:
            issues.append("🚨 Rotas possivelmente sem proteção (Depends ausente)")

    # ---------------------------
    # ENTRYPOINT
    # ---------------------------
    if "uvicorn" not in content and "__main__" not in content:
        issues.append("⚠️ Sem entrypoint de execução local")

    # ---------------------------
    # MONGO
    # ---------------------------
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

                if "__ERROR__" in content:
                    report[str(path)] = ["❌ erro ao ler arquivo"]
                    continue

                issues = analyze_file(path, content)

                if issues:
                    report[str(path)] = issues

    return report


# =========================================================
# SCORE SIMPLES (SEM RISCO)
# =========================================================
def calculate_score(report):
    total_issues = sum(len(v) for v in report.values())

    if total_issues == 0:
        return 100

    score = 100 - (total_issues * 3)

    if score < 0:
        score = 0

    return score


# =========================================================
# REPORT
# =========================================================
def run():
    print("\n======================================")
    print("🔍 SAFE BACKEND AUDITOR (READ ONLY)")
    print("======================================\n")

    report = scan_project()
    score = calculate_score(report)

    if not report:
        print("✅ Nenhum problema detectado")
        print("🏆 SCORE: 100/100")
        return

    for file, issues in report.items():
        print(f"\n📄 {file}")
        for i in issues:
            print(f"   {i}")

    print("\n======================================")
    print(f"📊 SECURITY SCORE: {score}/100")
    print("======================================\n")


if __name__ == "__main__":
    run()