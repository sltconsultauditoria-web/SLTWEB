# check_frontend_mocks.py
import os

FRONTEND_SRC = r"C:\Users\admin-local\ServerApp\consultSLTweb\frontend\src"

def find_mock_data():
    mock_files = []
    for root, _, files in os.walk(FRONTEND_SRC):
        for file in files:
            if file.endswith((".js", ".jsx", ".ts", ".tsx")):
                path = os.path.join(root, file)
                with open(path, encoding="utf-8", errors="ignore") as f:
                    content = f.read()

                    # Verifica se há dados mockados
                    if "mock" in content.lower() or "const " in content and "[" in content and "]" in content:
                        mock_files.append(path)
    return mock_files

def main():
    print("🔎 Verificando dados mockados no frontend...\n")
    mock_files = find_mock_data()
    if not mock_files:
        print("✅ Nenhum dado mockado encontrado. O frontend já depende apenas do backend.")
    else:
        print("⚠️ Arquivos com dados mockados encontrados:")
        for f in mock_files:
            print(" -", f)

        print("\nSugestão de substituição por chamadas reais ao backend:")
        print("""import axios from "axios";

const API = axios.create({ baseURL: "http://localhost:8000/api" });

// Exemplo de uso:
export async function getEmpresas() {
    const res = await API.get("/empresas");
    return res.data;
}""")

if __name__ == "__main__":
    main()
