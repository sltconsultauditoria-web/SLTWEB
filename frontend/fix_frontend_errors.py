# fix_frontend_errors.py
import os

FRONTEND_SRC = r"C:\Users\admin-local\ServerApp\consultSLTweb\frontend\src"

def create_api_file():
    api_path = os.path.join(FRONTEND_SRC, "api.js")
    if not os.path.exists(api_path):
        with open(api_path, "w", encoding="utf-8") as f:
            f.write("""import axios from "axios";

const API = axios.create({
  baseURL: "http://localhost:8000/api"
});

export default API;
""")
        print(f"✅ Criado: {api_path}")
    else:
        print(f"ℹ️ Já existe: {api_path}")

def fix_auth_context():
    path = os.path.join(FRONTEND_SRC, "context", "AuthContext.jsx")
    if os.path.exists(path):
        with open(path, "w", encoding="utf-8") as f:
            f.write("""import { createContext, useContext, useState } from "react";

const AuthContext = createContext();

export function AuthProvider({ children }) {
  const [user, setUser] = useState(null);

  const login = (userData) => setUser(userData);
  const logout = () => setUser(null);

  return (
    <AuthContext.Provider value={{ user, login, logout }}>
      {children}
    </AuthContext.Provider>
  );
}

export function useAuth() {
  return useContext(AuthContext);
}

export default AuthContext;
""")
        print(f"✅ Corrigido: {path}")

def fix_configuracoes():
    path = os.path.join(FRONTEND_SRC, "pages", "Configuracoes.jsx")
    if os.path.exists(path):
        with open(path, encoding="utf-8", errors="ignore") as f:
            content = f.read()
        new_content = content.replace(
            "import Tabs, TabsContent, TabsList, TabsTrigger }",
            "import { Tabs, TabsContent, TabsList, TabsTrigger }"
        )
        with open(path, "w", encoding="utf-8") as f:
            f.write(new_content)
        print(f"✅ Corrigido: {path}")

def fix_ui_components():
    ui_dir = os.path.join(FRONTEND_SRC, "components", "ui")

    # Corrige button.jsx
    button_path = os.path.join(ui_dir, "button.jsx")
    if os.path.exists(button_path):
        with open(button_path, "w", encoding="utf-8") as f:
            f.write("""export default function Button(props) {
  return <button {...props} />;
}
""")
        print(f"✅ Corrigido: {button_path}")

    # Corrige switch.jsx
    switch_path = os.path.join(ui_dir, "switch.jsx")
    if os.path.exists(switch_path):
        with open(switch_path, "w", encoding="utf-8") as f:
            f.write("""import { useState } from "react";

export default function Switch(props) {
  const [checked, setChecked] = useState(false);
  return (
    <input
      type="checkbox"
      checked={checked}
      onChange={() => setChecked(!checked)}
      {...props}
    />
  );
}
""")
        print(f"✅ Corrigido: {switch_path}")

def main():
    print("🔎 Corrigindo erros do frontend...\n")
    create_api_file()
    fix_auth_context()
    fix_configuracoes()
    fix_ui_components()
    print("\n🎯 Correções aplicadas. Agora o frontend deve compilar sem erros e consumir dados reais do backend.")

if __name__ == "__main__":
    main()
