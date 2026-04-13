import os

frontend_config = os.path.join("frontend", "src", "config", "api.js")
backend_app = os.path.join("backend", "src", "app.js")

def fix_frontend_baseurl():
    correct_content = """import axios from "axios";

export const API = axios.create({
  baseURL: "http://localhost:3000/api"
});
"""
    with open(frontend_config, "w", encoding="utf-8") as f:
        f.write(correct_content)
    print(f"✔ Frontend baseURL ajustado para usar /api")

def fix_backend_routes():
    if os.path.exists(backend_app):
        with open(backend_app, encoding="utf-8") as f:
            content = f.read()
        if "/api/" not in content:
            new_content = content.replace(
                "app.use(\"/empresas\", empresasRouter);",
                "app.use(\"/api/empresas\", empresasRouter);"
            ).replace(
                "app.use(\"/dashboard\", dashboardRouter);",
                "app.use(\"/api/dashboard\", dashboardRouter);"
            )
            with open(backend_app, "w", encoding="utf-8") as f:
                f.write(new_content)
            print(f"✔ Backend ajustado para usar prefixo /api")
        else:
            print("ℹ️ Backend já usa prefixo /api")

if __name__ == "__main__":
    fix_frontend_baseurl()
    fix_backend_routes()
    print("✅ Rotas alinhadas entre frontend e backend")
