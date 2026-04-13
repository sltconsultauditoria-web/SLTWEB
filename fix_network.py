import os

frontend_env = os.path.join("frontend", ".env")
backend_app = os.path.join("backend", "src", "app.js")

def fix_frontend_env():
    correct_line = "REACT_APP_API_URL=http://localhost:3000/api\n"
    if os.path.exists(frontend_env):
        with open(frontend_env, encoding="utf-8") as f:
            lines = f.readlines()
        # Remove linhas antigas e adiciona correta
        lines = [l for l in lines if not l.startswith("REACT_APP_API_URL")]
        lines.append(correct_line)
        with open(frontend_env, "w", encoding="utf-8") as f:
            f.writelines(lines)
        print(f"✔ Corrigido: {frontend_env}")
    else:
        with open(frontend_env, "w", encoding="utf-8") as f:
            f.write(correct_line)
        print(f"✔ Criado: {frontend_env}")

def fix_backend_cors():
    if os.path.exists(backend_app):
        with open(backend_app, encoding="utf-8") as f:
            content = f.read()
        if "cors()" not in content:
            new_content = content.replace(
                "const app = express();",
                "const app = express();\nconst cors = require('cors');\napp.use(cors());"
            )
            with open(backend_app, "w", encoding="utf-8") as f:
                f.write(new_content)
            print(f"✔ CORS habilitado em {backend_app}")
        else:
            print(f"ℹ️ CORS já habilitado em {backend_app}")

if __name__ == "__main__":
    fix_frontend_env()
    fix_backend_cors()
    print("✅ Configuração de rede corrigida. Reinicie backend e frontend.")
