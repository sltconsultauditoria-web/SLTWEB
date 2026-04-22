import os

print("\n🚀 CONSULT SLT - PROJECT CLEANUP AUDIT\n")

ROOT = "../../"

# arquivos suspeitos
SUSPECT_KEYWORDS = [
    "audit",
    "diagnostico",
    "avaliar",
    "verificar",
    "mock",
    "test",
    "debug"
]

# pastas ignoradas
IGNORE = [
    "node_modules",
    "venv",
    ".git",
    "__pycache__",
    "build"
]

suspects = []
backups = []
node_code = []

for root, dirs, files in os.walk(ROOT):

    if any(x in root for x in IGNORE):
        continue

    for file in files:

        path = os.path.join(root, file)
        name = file.lower()

        # backups
        if "backup" in root.lower():
            backups.append(path)

        # scripts suspeitos
        for word in SUSPECT_KEYWORDS:

            if word in name:
                suspects.append(path)

        # nodejs code
        if file.endswith(".js") and "backend" in root:
            node_code.append(path)

print("\n🧪 SCRIPTS DE TESTE / AUDITORIA\n")

for f in suspects[:30]:
    print(" ", f)

print("\n📦 BACKUPS ENCONTRADOS\n")

for f in backups[:20]:
    print(" ", f)

print("\n⚠ POSSÍVEL CÓDIGO NODE NO BACKEND PYTHON\n")

for f in node_code[:20]:
    print(" ", f)

print("\n🏁 AUDITORIA FINALIZADA\n")