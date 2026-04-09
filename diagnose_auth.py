import os
import sys
import bcrypt
import asyncio
from motor.motor_asyncio import AsyncIOMotorClient
from pathlib import Path

# ==============================================================================
# --- CONFIGURAÇÕES ---
# ==============================================================================
MONGO_URI = "mongodb://localhost:27017"
DB_NAME = "consultslt_db"
TEST_EMAIL = "william.lucas@sltconsult.com.br"
# Tente colocar aqui a senha que você está usando no frontend para testar
TEST_PASSWORD = "admin" 

# ==============================================================================
# --- DIAGNÓSTICO DE AUTENTICAÇÃO ---
# ==============================================================================

async def diagnose():
    print(f"\n🔍 INICIANDO DIAGNÓSTICO PROFUNDO DE AUTENTICAÇÃO SLTWEB\n")
    print(f"E-mail alvo: {TEST_EMAIL}")
    print("-" * 60)

    client = AsyncIOMotorClient(MONGO_URI)
    db = client[DB_NAME]

    # 1. Verificar Coleções
    collections = await db.list_collection_names()
    print(f"📂 Coleções encontradas no banco '{DB_NAME}': {collections}")

    # 2. Localizar Usuário
    user = None
    target_coll = ""
    for coll_name in ["usuarios", "users"]:
        if coll_name in collections:
            user = await db[coll_name].find_one({"email": TEST_EMAIL})
            if user:
                target_coll = coll_name
                break

    if not user:
        print(f"❌ ERRO: Usuário '{TEST_EMAIL}' não foi encontrado em NENHUMA coleção.")
        return

    print(f"✅ Usuário encontrado na coleção: '{target_coll}'")
    print(f"🆔 ID: {user.get('_id')}")
    print(f"📧 E-mail: {user.get('email')}")
    print(f"👤 Nome: {user.get('nome')}")

    # 3. Analisar Campo de Senha
    password_fields = ["senha_hash", "hashed_password", "password"]
    found_field = None
    hash_value = None

    for field in password_fields:
        if field in user:
            found_field = field
            hash_value = user[field]
            break

    if not found_field:
        print(f"❌ ERRO: Nenhum campo de senha ({password_fields}) foi encontrado no documento do usuário.")
        print(f"Campos disponíveis no documento: {list(user.keys())}")
        return

    print(f"✅ Campo de senha identificado: '{found_field}'")
    print(f"🔒 Valor do Hash (primeiros 10 caracteres): {str(hash_value)[:10]}...")

    # 4. Testar Verificação de Senha (BCRYPT)
    print(f"\n🛠️ TESTANDO VERIFICAÇÃO DE SENHA (BCRYPT)...")
    print(f"Testando com a senha plana: '{TEST_PASSWORD}'")
    
    try:
        if isinstance(hash_value, str):
            is_valid = bcrypt.checkpw(
                TEST_PASSWORD.encode("utf-8"),
                hash_value.encode("utf-8")
            )
            if is_valid:
                print(f"🎉 SUCESSO! A senha '{TEST_PASSWORD}' coincide com o hash do banco.")
            else:
                print(f"❌ FALHA: A senha '{TEST_PASSWORD}' NÃO coincide com o hash do banco.")
                print(f"💡 DICA: O hash no banco pode ter sido gerado com uma senha diferente ou outro algoritmo.")
        else:
            print(f"❌ ERRO: O valor do hash no banco não é uma string válida.")
    except Exception as e:
        print(f"🔥 ERRO AO EXECUTAR BCRYPT: {e}")

    # 5. Verificar Status e Permissões
    print(f"\n📋 STATUS E PERMISSÕES:")
    print(f"Ativo: {user.get('ativo', user.get('is_active', 'N/A'))}")
    print(f"Perfil: {user.get('perfil', user.get('role', 'N/A'))}")
    print(f"Permissões: {user.get('permissoes', [])}")

    print("\n" + "="*60)
    print("RESUMO DO DIAGNÓSTICO:")
    if found_field and hash_value:
        print(f"O backend deve estar configurado para ler o campo '{found_field}' na coleção '{target_coll}'.")
    print("="*60)

if __name__ == "__main__":
    asyncio.run(diagnose())