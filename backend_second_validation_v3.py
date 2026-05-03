import os
import ast
import re
from collections import defaultdict

ROOT_DIR = "backend"

# ==============================
# RULES ENGINE
# ==============================

RULES = {
    "jwt_missing": {
        "pattern": r"jwt|PyJWT|encode\(",
        "severity": "HIGH",
        "message": "JWT não implementado ou não detectado"
    },
    "fastapi_missing": {
        "import": "fastapi",
        "severity": "LOW",
        "message": "FastAPI não detectado no arquivo"
    },
    "hardcoded_secret": {
        "pattern": r"SECRET|PASSWORD|TOKEN\s*=\s*[\"'].*[\"']",
        "severity": "CRITICAL",
        "message": "Secret hardcoded detectado"
    },
    "cors_open": {
        "pattern": r"CORS.*allow_origins\s*=\s*\[\s*[\"']\*",
        "severity": "HIGH",
        "message": "CORS aberto em produção"
    },
    "plain_password": {
        "pattern": r"password\s*=\s*[\"'].*[\"']",
        "severity": "CRITICAL",
        "message": "Senha possivelmente em texto puro"
    },
    "mongo_no_try": {
        "pattern": r"MongoClient",
        "severity": "MEDIUM",
        "message": "Mongo sem tratamento de erro (verificar try/except)"
    },
    "missing_auth_dependency": {
        "pattern": r"Depends\(",
        "severity": "HIGH",
        "message": "Possível ausência de dependency injection de auth"
    }
}

# ==============================
# UTIL
# ==============================

def load_file(path):
    try:
        with open(path, "r", encoding="utf-8") as f:
            return f.read()
    except:
        return ""

def has_import(tree, module_name):
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            for n in node.names:
                if module_name in n.name:
                    return True
        if isinstance(node, ast.ImportFrom):
            if node.module and module_name in node.module:
                return True
    return False

def safe_ast(content):
    try:
        return ast.parse(content)
    except:
        return None

# ==============================
# ANALYSIS ENGINE
# ==============================

def analyze_file(path):
    content = load_file(path)
    tree = safe_ast(content)

    issues = []

    for rule_name, rule in RULES.items():

        # IMPORT RULES
        if "import" in rule:
            if rule["import"] == "fastapi":
                if not tree or not has_import(tree, "fastapi"):
                    issues.append((rule["severity"], rule["message"]))
            continue

        # PATTERN RULES
        if "pattern" in rule:
            if re.search(rule["pattern"], content, re.IGNORECASE):
                issues.append((rule["severity"], rule["message"]))

    return issues

# ==============================
# SCORE ENGINE
# ==============================

def score(severity):
    return {
        "CRITICAL": 25,
        "HIGH": 15,
        "MEDIUM": 8,
        "LOW": 3
    }.get(severity, 0)

# ==============================
# SCAN PROJECT
# ==============================

def scan_project():
    report = defaultdict(list)
    total_score = 100

    for root, _, files in os.walk(ROOT_DIR):
        for file in files:
            if file.endswith(".py"):
                path = os.path.join(root, file)
                issues = analyze_file(path)

                if issues:
                    for sev, msg in issues:
                        report[path].append((sev, msg))
                        total_score -= score(sev)

    return report, max(total_score, 0)

# ==============================
# OUTPUT FORMAT
# ==============================

def print_report(report, score):
    print("\n======================================")
    print("🧠 SECOND VALIDATION AUDITOR V3")
    print("======================================\n")

    for file, issues in report.items():
        print(f"📄 {file}")
        for sev, msg in issues:
            icon = "🚨" if sev == "CRITICAL" else "⚠️"
            print(f"   {icon} [{sev}] {msg}")
        print()

    print("======================================")
    print(f"📊 FINAL SECURITY SCORE: {score}/100")
    print("======================================")

# ==============================
# MAIN
# ==============================

if __name__ == "__main__":
    report, score_value = scan_project()
    print_report(report, score_value)