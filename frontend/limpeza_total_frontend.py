# salvar como limpeza_total_frontend.py
# executar: python limpeza_total_frontend.py

import os
import re
from pathlib import Path

BASE = Path(__file__).resolve().parent
SRC = BASE / "src"

print("=" * 70)
print("LIMPEZA TOTAL FRONTEND")
print("=" * 70)

# ==========================================================
# 1. GARANTIR src/services/api.js correto
# ==========================================================
services_dir = SRC / "services"
services_dir.mkdir(exist_ok=True)

api_service = services_dir / "api.js"

conteudo_api = '''import axios from "axios";

const api = axios.create({
  baseURL:
    process.env.REACT_APP_API_URL ||
    process.env.REACT_APP_BACKEND_URL ||
    "http://localhost:8000",
  headers: {
    "Content-Type": "application/json",
  },
});

api.interceptors.request.use((config) => {
  const token = localStorage.getItem("token");
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});

api.interceptors.response.use(
  (response) => response,
  (error) => {
    console.error("Erro API:", error?.message);
    return Promise.reject(error);
  }
);

export default api;
'''

api_service.write_text(conteudo_api, encoding="utf-8")
print("[OK] src/services/api.js recriado")

# ==========================================================
# 2. GARANTIR src/api.js proxy oficial
# ==========================================================
api_proxy = SRC / "api.js"
api_proxy.write_text(
    'export { default } from "./services/api";\n',
    encoding="utf-8"
)
print("[OK] src/api.js recriado")

# ==========================================================
# 3. APAGAR APIs DUPLICADAS ERRADAS
# ==========================================================
duplicados = [
    SRC / "config" / "api.js",
    SRC / "lib" / "api.js",
]

for arq in duplicados:
    if arq.exists():
        arq.unlink()
        print(f"[REMOVIDO] {arq}")

# ==========================================================
# 4. REMOVER IMPORT API DE COMPONENTES UI
# ==========================================================
ui_dir = SRC / "components" / "ui"

if ui_dir.exists():
    for arquivo in ui_dir.rglob("*.js*"):
        texto = arquivo.read_text(encoding="utf-8", errors="ignore")

        novo = re.sub(
            r'^.*import\s+API\s+from\s+["\'].*api.*["\'];?\s*$',
            '',
            texto,
            flags=re.MULTILINE
        )

        if novo != texto:
            arquivo.write_text(novo, encoding="utf-8")
            print(f"[LIMPO UI] {arquivo}")

# ==========================================================
# 5. PADRONIZAR IMPORTS NAS PAGES / COMPONENTS
# ==========================================================
pastas = [
    SRC / "pages",
    SRC / "components",
    SRC / "hooks",
    SRC / "lib"
]

for pasta in pastas:
    if pasta.exists():
        for arquivo in pasta.rglob("*.js*"):
            texto = arquivo.read_text(encoding="utf-8", errors="ignore")

            novo = texto

            # imports relativos para proxy oficial
            novo = re.sub(
                r'import\s+API\s+from\s+["\']\.\./api\.js["\'];?',
                'import API from "@/api";',
                novo
            )

            novo = re.sub(
                r'import\s+API\s+from\s+["\']\.\./\.\./api\.js["\'];?',
                'import API from "@/api";',
                novo
            )

            novo = re.sub(
                r'import\s+api\s+from\s+["\']\.\./services/api["\'];?',
                'import API from "@/api";',
                novo
            )

            if novo != texto:
                arquivo.write_text(novo, encoding="utf-8")
                print(f"[PADRONIZADO] {arquivo}")

# ==========================================================
# 6. RELATÓRIO FINAL
# ==========================================================
print("\n" + "=" * 70)
print("FINALIZADO")
print("=" * 70)
print("Mantido:")
print(" - src/services/api.js")
print(" - src/api.js")
print("")
print("Removido:")
print(" - src/config/api.js")
print(" - src/lib/api.js")
print("")
print("UI components limpos.")
print("Imports padronizados para:")
print('import API from "@/api";')
print("=" * 70)