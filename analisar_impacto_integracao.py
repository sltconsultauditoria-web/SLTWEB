# analisar_impacto_integracao.py
# ==========================================================
# ANALISA IMPACTO DAS CORREÇÕES ANTES DE ALTERAR O SISTEMA
#
# OBJETIVO:
# - Medir quantos arquivos frontend serão afetados
# - Quantas chamadas axios/fetch precisam mudar
# - Quantas rotas quebradas impactam telas
# - Verificar risco no backend
# - Verificar impacto no MongoDB
# - Gerar score BAIXO / MÉDIO / ALTO
#
# EXECUTAR:
# python analisar_impacto_integracao.py
# ==========================================================

import os
import re
import requests
from collections import defaultdict

BASE_DIR = r"C:\Users\admin-local\ServerApp\consultSLTweb"
FRONTEND = os.path.join(BASE_DIR, "frontend")
BACKEND_URL = "http://localhost:8000"

OK = "✅"
WARN = "⚠️"
ERRO = "❌"

print("=" * 90)
print("ANÁLISE DE IMPACTO DAS CORREÇÕES")
print("=" * 90)

# ======================================================
# 1. MAPEAR CHAMADAS FRONTEND
# ======================================================
print("\n[1] ANALISANDO FRONTEND...")

arquivos_afetados = set()
rotas_por_arquivo = defaultdict(list)
total_calls = 0

patterns = [
    r'axios\.(get|post|put|delete)\(["\']([^"\']+)["\']',
    r'fetch\(["\']([^"\']+)["\']',
    r'api\.(get|post|put|delete)\(["\']([^"\']+)["\']'
]

for root, dirs, files in os.walk(FRONTEND):
    for file in files:
        if file.endswith((".js", ".jsx", ".ts", ".tsx")):
            path = os.path.join(root, file)

            try:
                txt = open(path, encoding="utf-8").read()
            except:
                continue

            for p in patterns:
                achados = re.findall(p, txt)

                for a in achados:
                    rota = a[-1]

                    if rota.startswith("/"):
                        total_calls += 1
                        arquivos_afetados.add(path)
                        rotas_por_arquivo[path].append(rota)

print(f"{OK} Arquivos impactados: {len(arquivos_afetados)}")
print(f"{OK} Chamadas API encontradas: {total_calls}")

# ======================================================
# 2. TESTAR STATUS DAS ROTAS
# ======================================================
print("\n[2] TESTANDO ROTAS...")

rotas_unicas = set()

for arq in rotas_por_arquivo:
    for r in rotas_por_arquivo[arq]:
        rotas_unicas.add(r)

quebradas = []
ok_rotas = []

for rota in sorted(rotas_unicas):

    try:
        r = requests.get(BACKEND_URL + rota, timeout=4)

        if r.status_code in [200, 201, 204]:
            ok_rotas.append(rota)
        else:
            quebradas.append((rota, r.status_code))

    except:
        quebradas.append((rota, "OFFLINE"))

print(f"{OK} Rotas funcionando: {len(ok_rotas)}")
print(f"{ERRO} Rotas quebradas: {len(quebradas)}")

# ======================================================
# 3. IMPACTO POR TELA
# ======================================================
print("\n[3] IMPACTO POR TELA...")

for arq in sorted(rotas_por_arquivo):

    nome = os.path.basename(arq)
    total = len(rotas_por_arquivo[arq])

    falhas = 0

    for r in rotas_por_arquivo[arq]:
        for q in quebradas:
            if q[0] == r:
                falhas += 1

    risco = "BAIXO"

    if falhas >= 3:
        risco = "ALTO"
    elif falhas >= 1:
        risco = "MÉDIO"

    print(f"{nome:25} APIs:{total:<3} Falhas:{falhas:<3} Impacto:{risco}")

# ======================================================
# 4. SCORE GLOBAL
# ======================================================
print("\n[4] SCORE GLOBAL...")

score = 0

score += len(quebradas) * 2
score += len(arquivos_afetados)

if score <= 15:
    nivel = "BAIXO"
elif score <= 35:
    nivel = "MÉDIO"
else:
    nivel = "ALTO"

print(f"Score: {score}")
print(f"Impacto geral: {nivel}")

# ======================================================
# 5. RECOMENDAÇÃO
# ======================================================
print("\n[5] RECOMENDAÇÃO TÉCNICA")

if nivel == "BAIXO":
    print(f"{OK} Correção segura. Pode aplicar direto.")
elif nivel == "MÉDIO":
    print(f"{WARN} Fazer backup antes e corrigir módulo por módulo.")
else:
    print(f"{ERRO} Alto impacto. Corrigir primeiro ambiente de teste.")

# ======================================================
# 6. AÇÕES NECESSÁRIAS
# ======================================================
print("\n[6] O QUE SERÁ ALTERADO")

print("""
1. Centralizar Axios em src/services/api.js
2. Corrigir baseURL para /api
3. Ajustar rotas 404
4. Corrigir login GET -> POST
5. Criar endpoints faltantes no FastAPI
6. Validar collections MongoDB faltantes
7. Re-testar tudo
""")

print("=" * 90)