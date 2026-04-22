import os
import re

print("\n🚀 ENTERPRISE MASK AUDIT + FIXER\n")

ROOT_DIR = "../../"

IGNORE_DIRS = [
    "node_modules",
    "venv",
    "__pycache__",
    "backup",
    "archive",
    ".git"
]

MASK_FIELDS = {
    "cnpj": "CNPJ",
    "cpf": "CPF",
    "cep": "CEP",
    "telefone": "TELEFONE",
    "email": "EMAIL",
    "valor": "VALOR",
    "data": "DATA"
}

results = {k: [] for k in MASK_FIELDS}

# --------------------------------------
# scanner
# --------------------------------------

for root, dirs, files in os.walk(ROOT_DIR):

    if any(x in root.lower() for x in IGNORE_DIRS):
        continue

    for file in files:

        if not file.endswith((".py", ".js", ".ts", ".jsx", ".tsx")):
            continue

        path = os.path.join(root, file)

        try:

            with open(path, "r", encoding="utf8") as f:
                content = f.read().lower()

                for field in MASK_FIELDS:

                    if field in content:
                        results[field].append(path)

        except:
            pass


# --------------------------------------
# relatório
# --------------------------------------

print("\n📊 CAMPOS ENCONTRADOS\n")

for field, files in results.items():

    if not files:
        continue

    print(f"\n⚠ {MASK_FIELDS[field]} encontrado em:")

    for f in files[:10]:
        print("   ", f)


# --------------------------------------
# gerar util de máscaras
# --------------------------------------

frontend_mask_file = "../../frontend/src/utils/masks.js"

mask_code = """

export const masks = {

  cnpj: "99.999.999/9999-99",

  cpf: "999.999.999-99",

  cep: "99999-999",

  telefone: "(99) 99999-9999"

}

export function formatMoney(value){

  return new Intl.NumberFormat("pt-BR",{
    style:"currency",
    currency:"BRL"
  }).format(value)

}

export function formatDate(date){

  return new Date(date).toLocaleDateString("pt-BR")

}
"""

os.makedirs(os.path.dirname(frontend_mask_file), exist_ok=True)

with open(frontend_mask_file, "w", encoding="utf8") as f:
    f.write(mask_code)

print("\n✔ arquivo criado:")
print(frontend_mask_file)


# --------------------------------------
# gerar sanitizer backend
# --------------------------------------

backend_sanitizer = "../../backend/utils/sanitizer.py"

sanitizer_code = """

import re

def clean_cnpj(cnpj):
    return re.sub(r"\\D","",cnpj)

def clean_cpf(cpf):
    return re.sub(r"\\D","",cpf)

def clean_cep(cep):
    return re.sub(r"\\D","",cep)

def clean_phone(phone):
    return re.sub(r"\\D","",phone)

"""

os.makedirs(os.path.dirname(backend_sanitizer), exist_ok=True)

with open(backend_sanitizer, "w", encoding="utf8") as f:
    f.write(sanitizer_code)

print("\n✔ sanitizer backend criado:")
print(backend_sanitizer)

print("\n🏁 ENTERPRISE MASK SETUP FINALIZADO\n")