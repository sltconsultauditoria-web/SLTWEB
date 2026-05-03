import os
import re
import ast
from pathlib import Path
from collections import defaultdict

ROOT_DIR = "backend"

# ============================
# DETECÇÃO AVANÇADA (AST + REGEX)
# ============================

SECRET_PATTERNS = [
    r"SECRET",
    r"API_KEY",
    r"PASSWORD",
    r"TOKEN",
    r"JWT_SECRET",
    r"PRIVATE_KEY"
]

FASTAPI_IMPORTS = [
    "fastapi",
    "APIRouter",
    "FastAPI",
    "Depends"
]

JWT_IMPORTS = [
    "jwt",
    "PyJWT",
    "jose",
    "OAuth2PasswordBearer"
]


def read_file(file_path):
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            return f.read()
    except:
        return ""


def detect_secrets(content):
    return any(re.search(p, content) for p in SECRET_PATTERNS)


def detect_fastapi_ast(tree):
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            for n in node.names:
                if "fastapi" in n.name:
                    return True
        if isinstance(node, ast.ImportFrom):
            if node.module and "fastapi" in node.module:
                return True
    return False


def detect_jwt(content):
    return any(p.lower() in content.lower() for p in JWT_IMPORTS)


def detect_entrypoint(content):
    return "__name__ == \"__main__\"" in content or "uvicorn" in content


def detect_dependency_injection(content):
    return "Depends(" in content


# ============================
# ANALISADOR DE ARQUIVO
# ============================

def analyze_file(file_path):
    content = read_file(file_path)

    try:
        tree = ast.parse(content)
    except:
        tree = None

    findings = []

    # Secrets
    if detect_secrets(content):
        findings.append(("CRITICAL", "Secret hardcoded detectado"))

    # FastAPI
    if not (tree and detect_fastapi_ast(tree)):
        findings.append(("LOW", "FastAPI não detectado"))

    # JWT
    if not detect_jwt(content):
        findings.append(("HIGH", "JWT não implementado ou não detectado"))

    # Entry point
    if not detect_entrypoint(content):
        findings.append(("MEDIUM", "Sem entrypoint de execução local"))

    # Dependency Injection
    if "router" in file_path.lower() or "service" in file_path.lower():
        if not detect_dependency_injection(content):
            findings.append(("HIGH", "Possível ausência de dependency injection"))

    return findings


# ============================
# SCORE ENGINE (INTELIGENTE)
# ============================

WEIGHTS = {
    "CRITICAL": 25,
    "HIGH": 15,
    "MEDIUM": 8,
    "LOW": 3
}


def calculate_score(results):
    total_penalty = 0

    for file, findings in results.items():
        for level, _ in findings:
            total_penalty += WEIGHTS.get(level, 1)

    score = max(0, 100 - total_penalty)
    return score


# ============================
# SCANNER RECURSIVO
# ============================

def scan_project():
    results = defaultdict(list)

    for root, _, files in os.walk(ROOT_DIR):
        for file in files:
            if file.endswith(".py"):
                path = os.path.join(root, file)
                findings = analyze_file(path)

                if findings:
                    results[path] = findings

    return results


# ============================
# REPORT
# ============================

def print_report(results):
    print("\n======================================")
    print("🧠 SECOND VALIDATION AUDITOR V4")
    print("======================================\n")

    for file, findings in results.items():
        print(f"📄 {file}")
        for level, msg in findings:
            icon = "🚨" if level == "CRITICAL" else "⚠️"
            print(f"   {icon} [{level}] {msg}")
        print()

    score = calculate_score(results)

    print("======================================")
    print(f"📊 FINAL SECURITY SCORE: {score}/100")
    print("======================================")


# ============================
# MAIN
# ============================

if __name__ == "__main__":
    results = scan_project()
    print_report(results)