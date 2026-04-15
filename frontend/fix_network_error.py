import os

FRONTEND_API = r"C:\Users\admin-local\ServerApp\consultSLTweb\frontend\src\api.js"
BACKEND_MAIN = r"C:\Users\admin-local\ServerApp\consultSLTweb\backend\main_enterprise.py"

def fix_api_js():
    if os.path.exists(FRONTEND_API):
        with open(FRONTEND_API, encoding="utf-8") as f:
            content = f.read()

        # Ajusta baseURL para refletir o backend real
        new_content = """import axios from "axios";

const API = axios.create({
  baseURL: "http://localhost/SLTWEB/api" // ajustado para seu backend
});

export default API;
"""
        if content != new_content:
            with open(FRONTEND_API, "w", encoding="utf-8") as f:
                f.write(new_content)
            print(f"✅ Corrigido: {FRONTEND_API}")
        else:
            print("ℹ️ api.js já está ajustado")

def fix_backend_cors():
    if os.path.exists(BACKEND_MAIN):
        with open(BACKEND_MAIN, encoding="utf-8") as f:
            content = f.read()

        if "CORSMiddleware" not in content:
            cors_block = """
from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # ajuste se quiser restringir
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
"""
            new_content = content.replace("app = FastAPI(", "app = FastAPI(") + cors_block
            with open(BACKEND_MAIN, "w", encoding="utf-8") as f:
                f.write(new_content)
            print(f"✅ CORS adicionado em {BACKEND_MAIN}")
        else:
            print("ℹ️ CORS já configurado no backend")

def main():
    print("🔎 Corrigindo Network Error...\n")
    fix_api_js()
    fix_backend_cors()
    print("\n🎯 Correções aplicadas. Reinicie backend e frontend para testar.")

if __name__ == "__main__":
    main()
