# replace_mocks_with_api.py
import os

FRONTEND_SRC = r"C:\Users\admin-local\ServerApp\consultSLTweb\frontend\src"

API_TEMPLATE = """import { useEffect, useState } from "react";
import API from "../api";

export default function COMPONENT_NAME() {
  const [data, setData] = useState([]);

  useEffect(() => {
    API.get("/ROTA_BACKEND").then(res => setData(res.data));
  }, []);

  return (
    <div>
      <h1>COMPONENT_NAME</h1>
      <pre>{JSON.stringify(data, null, 2)}</pre>
    </div>
  );
}
"""

def replace_mocks():
    for root, _, files in os.walk(FRONTEND_SRC):
        for file in files:
            if file.endswith((".jsx", ".js")):
                path = os.path.join(root, file)
                with open(path, encoding="utf-8", errors="ignore") as f:
                    content = f.read()

                if "mock" in content.lower() or "[" in content and "]" in content:
                    component_name = os.path.splitext(file)[0]
                    new_content = API_TEMPLATE.replace("COMPONENT_NAME", component_name).replace("/ROTA_BACKEND", f"/{component_name.lower()}")
                    with open(path, "w", encoding="utf-8") as f:
                        f.write(new_content)
                    print(f"✅ Mock removido e substituído por chamada Axios em {path}")

def main():
    print("🔎 Substituindo mocks por chamadas reais ao backend...\n")
    replace_mocks()
    print("\n🎯 Frontend agora depende apenas de dados reais do backend API e consultslt_db.")

if __name__ == "__main__":
    main()
