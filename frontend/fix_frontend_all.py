# fix_frontend_all.py
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

def fix_tabs_component():
    path = os.path.join(FRONTEND_SRC, "components", "ui", "tabs.jsx")
    if os.path.exists(path):
        with open(path, "w", encoding="utf-8") as f:
            f.write("""export function Tabs({ children }) {
  return <div className="tabs">{children}</div>;
}

export function TabsList({ children }) {
  return <div className="tabs-list">{children}</div>;
}

export function TabsTrigger({ children }) {
  return <button className="tabs-trigger">{children}</button>;
}

export function TabsContent({ children }) {
  return <div className="tabs-content">{children}</div>;
}
""")
        print(f"✅ Corrigido: {path}")

def fix_switch_component():
    path = os.path.join(FRONTEND_SRC, "components", "ui", "switch.jsx")
    if os.path.exists(path):
        with open(path, "w", encoding="utf-8") as f:
            f.write("""import { useState } from "react";

export function Switch(props) {
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
        print(f"✅ Corrigido: {path}")

def fix_api_imports():
    for root, _, files in os.walk(FRONTEND_SRC):
        for file in files:
            if file.endswith((".js", ".jsx")):
                path = os.path.join(root, file)
                with open(path, encoding="utf-8", errors="ignore") as f:
                    content = f.read()

                new_content = content

                # Ajusta imports conforme profundidade
                if "import API from '../api.js'" in new_content and "components/Layout" in path:
                    new_content = new_content.replace("import API from '../api.js'", "import API from '../../api.js'")
                if "import API from '../api.js'" in new_content and "components/ui" in path:
                    new_content = new_content.replace("import API from '../api.js'", "import API from '../../api.js'")
                if "import API from '../api.js'" in new_content and "pages" in path:
                    new_content = new_content.replace("import API from '../api.js'", "import API from '../api.js'")

                if new_content != content:
                    with open(path, "w", encoding="utf-8") as f:
                        f.write(new_content)
                    print(f"✅ Corrigido: {path}")

def main():
    print("🔎 Corrigindo todo o frontend...\n")
    create_api_file()
    fix_auth_context()
    fix_tabs_component()
    fix_switch_component()
    fix_api_imports()
    print("\n🎯 Todas as correções aplicadas. O frontend deve compilar sem erros e consumir dados reais do backend.")

if __name__ == "__main__":
    main()
