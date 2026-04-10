from pathlib import Path
import re

print("\n🔎 AUDITORIA DE CAMPOS QUE PRECISAM DE MÁSCARA\n")

project_root = Path("../../")

patterns = {
    "CNPJ": r"cnpj",
    "CPF": r"cpf",
    "TELEFONE": r"telefone|phone|celular",
    "CEP": r"cep",
    "DATA": r"data|date",
    "VALOR": r"valor|total|preco|price",
    "IE": r"inscricao_estadual|ie",
}

files = []

files.extend(project_root.rglob("*.py"))
files.extend(project_root.rglob("*.js"))
files.extend(project_root.rglob("*.ts"))
files.extend(project_root.rglob("*.tsx"))

results = {}

for f in files:

    try:
        content = f.read_text(encoding="utf-8", errors="ignore").lower()
    except:
        continue

    for label, pattern in patterns.items():

        if re.search(pattern, content):

            if label not in results:
                results[label] = []

            results[label].append(str(f))

print("\n📊 RESULTADO\n")

for field, locations in results.items():

    print(f"\n⚠ Campo detectado: {field}")

    unique = list(set(locations))

    for loc in unique[:10]:
        print("   ", loc)

print("\n🏁 Auditoria finalizada\n")