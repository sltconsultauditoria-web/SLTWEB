# validar_hotfix_alertas_obrigacoes.py
# CONSULTSLTWEB - VALIDAÇÃO FINAL APÓS HOTFIX
# Verifica se /api/alertas e /api/obrigacoes voltaram 200

import requests
import json
from datetime import datetime

BASE_URL = "http://localhost:8000"

ENDPOINTS = [
    "/health",
    "/api/dashboard",
    "/api/alertas",
    "/api/obrigacoes",
]

resultado = {
    "data": str(datetime.now()),
    "checks": {},
    "score": 0,
    "status": ""
}

print("=" * 100)
print("VALIDAÇÃO FINAL HOTFIX CONSULTSLTWEB")
print("=" * 100)

ok = 0

for ep in ENDPOINTS:
    try:
        r = requests.get(BASE_URL + ep, timeout=10)
        status = r.status_code

        if status == 200:
            print(f"✅ {ep} -> 200")
            ok += 1
            resultado["checks"][ep] = {"ok": True, "status": 200}
        else:
            print(f"❌ {ep} -> {status}")
            resultado["checks"][ep] = {"ok": False, "status": status}

    except Exception as e:
        print(f"❌ {ep} -> erro: {str(e)}")
        resultado["checks"][ep] = {"ok": False, "erro": str(e)}

score = int((ok / len(ENDPOINTS)) * 100)
resultado["score"] = score

if score == 100:
    resultado["status"] = "SISTEMA TOTALMENTE FUNCIONAL"
elif score >= 90:
    resultado["status"] = "QUASE PERFEITO"
else:
    resultado["status"] = "AINDA REQUER AJUSTES"

arquivo = "relatorio_hotfix_final.json"

with open(arquivo, "w", encoding="utf-8") as f:
    json.dump(resultado, f, indent=4, ensure_ascii=False)

print("\n" + "=" * 100)
print("RESULTADO FINAL")
print("=" * 100)
print(f"Score: {score}/100")
print(resultado["status"])
print(f"Relatório salvo em: {arquivo}")
print("=" * 100)