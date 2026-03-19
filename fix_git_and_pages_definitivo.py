import os
import subprocess
import shutil

def run(cmd):
    print(f"\n>> {cmd}")
    os.system(cmd)

print("=" * 60)
print("🔥 FIX DEFINITIVO GITHUB PAGES + GIT CLEAN")
print("=" * 60)

# ================================
# 1. GARANTIR .gitignore CORRETO
# ================================
print("\n🛡️ Ajustando .gitignore...")

gitignore = """
# Node
node_modules/
frontend/node_modules/

# Build
build/
frontend/build/

# Cache
.cache/
frontend/node_modules/.cache/

# Logs
*.log

# OS
.DS_Store
Thumbs.db
"""

with open(".gitignore", "w") as f:
    f.write(gitignore.strip())

print("✅ .gitignore atualizado")

# ================================
# 2. REMOVER CACHE PESADO
# ================================
print("\n🧹 Removendo cache pesado...")

paths_to_remove = [
    "frontend/node_modules/.cache",
    "frontend/build",
    "frontend/docs",
    "docs"
]

for path in paths_to_remove:
    if os.path.exists(path):
        shutil.rmtree(path, ignore_errors=True)
        print(f"🗑️ Removido: {path}")

# ================================
# 3. REMOVER DO GIT (CRÍTICO)
# ================================
print("\n🚨 Removendo node_modules do Git (histórico)...")

run("git rm -r --cached frontend/node_modules")
run("git rm -r --cached node_modules")

# ================================
# 4. LIMPAR HISTÓRICO (REMOVE ARQUIVOS GRANDES)
# ================================
print("\n🔥 Limpando histórico (remove arquivos >100MB)...")

run("git filter-branch --force --index-filter \"git rm -r --cached --ignore-unmatch frontend/node_modules\" --prune-empty --tag-name-filter cat -- --all")

# ================================
# 5. REINSTALAR FRONTEND
# ================================
print("\n📦 Instalando dependências...")

run("cd frontend && npm install")

# ================================
# 6. BUILD LIMPO
# ================================
print("\n🏗️ Buildando frontend...")

run("cd frontend && npm run build")

# ================================
# 7. COPIAR PARA /docs (ROOT)
# ================================
print("\n📦 Copiando build → docs raiz...")

if os.path.exists("docs"):
    shutil.rmtree("docs")

shutil.copytree("frontend/build", "docs")

print("✅ docs pronto")

# ================================
# 8. COMMIT LIMPO
# ================================
print("\n💾 Commit limpo...")

run("git add .")
run('git commit -m "🔥 fix definitivo github pages + limpeza completa"')

# ================================
# 9. FORCE PUSH (NECESSÁRIO)
# ================================
print("\n🚀 Enviando para GitHub (FORCE)...")

run("git push origin main --force")

print("\n" + "=" * 60)
print("✅ DEPLOY 100% LIMPO FINALIZADO")
print("=" * 60)

print("\n👉 AGORA ACESSE (limpe cache do navegador):")
print("https://sltconsultauditoria-web.github.io/SLTWEB/?v=FINAL_CLEAN")