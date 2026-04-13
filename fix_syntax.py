import os

frontend_dir = "frontend/src"

def fix_api_js():
    api_path = os.path.join(frontend_dir, "config", "api.js")
    correct_content = """import axios from "axios";

export const API = axios.create({
  baseURL: process.env.REACT_APP_API_URL
});
"""
    with open(api_path, "w", encoding="utf-8") as f:
        f.write(correct_content)
    print(f"✔ Corrigido: {api_path}")

def fix_documentos_jsx():
    doc_path = os.path.join(frontend_dir, "pages", "Documentos.jsx")
    if os.path.exists(doc_path):
        with open(doc_path, encoding="utf-8") as f:
            content = f.read()
        # Corrigir trecho incorreto de responseType
        if "responseType:" in content and "try {" in content:
            new_content = content.replace(
                "try {\n        responseType: 'blob',\n      });",
                """try {
    const response = await API.get(`/documentos/${id}`, {
      responseType: 'blob'
    });
"""
            )
            with open(doc_path, "w", encoding="utf-8") as f:
                f.write(new_content)
            print(f"✔ Corrigido: {doc_path}")

if __name__ == "__main__":
    fix_api_js()
    fix_documentos_jsx()
    print("✅ Correções aplicadas em api.js e Documentos.jsx")
