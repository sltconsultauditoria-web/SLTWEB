import sys
import os

# ===============================
# Ajusta o PYTHONPATH para a raiz do projeto
# ===============================
BASE_DIR = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "..")
)

if BASE_DIR not in sys.path:
    sys.path.insert(0, BASE_DIR)

# ===============================
# Agora os imports funcionam
# ===============================
from backend.main_enterprise import app

# ===============================
# Mapeamento das rotas
# ===============================
print("\n📌 ROTAS REGISTRADAS NA API:\n")

for route in app.routes:
    methods = ",".join(route.methods)
    print(f"{methods:15} {route.path}")

print("\n✅ Mapeamento concluído com sucesso\n")
