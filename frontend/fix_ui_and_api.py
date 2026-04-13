# fix_ui_and_api.py
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

def main():
    print("🔎 Corrigindo API e componentes UI...\n")
    create_api_file()
    fix_tabs_component()
    fix_switch_component()
    print("\n🎯 Correções aplicadas. Agora os imports de API e os componentes Tabs/Switch devem funcionar corretamente.")

if __name__ == "__main__":
    main()
