#!/bin/bash

# ==========================================
# Dashboard Setup e Quick Start Script
# ==========================================

echo "🚀 Iniciando setup do Dashboard..."
echo ""

# Cores para output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# ==========================================
# 1. Verificar dependências
# ==========================================
echo -e "${BLUE}[1/4]${NC} Verificando dependências..."

# Python
if ! command -v python3 &> /dev/null; then
    echo -e "${RED}❌ Python3 não encontrado${NC}"
    exit 1
fi
echo -e "${GREEN}✅ Python3 encontrado${NC}"

# Node.js
if ! command -v node &> /dev/null; then
    echo -e "${RED}❌ Node.js não encontrado${NC}"
    exit 1
fi
echo -e "${GREEN}✅ Node.js encontrado${NC}"

# MongoDB
if ! command -v mongosh &> /dev/null; then
    echo -e "${YELLOW}⚠️  MongoDB não encontrado (pode estar rodando em segundo plano)${NC}"
else
    echo -e "${GREEN}✅ MongoDB encontrado${NC}"
fi

echo ""

# ==========================================
# 2. Instalar dependências Python (Backend)
# ==========================================
echo -e "${BLUE}[2/4]${NC} Configurando Backend..."

# Verificar se arquivo requirements.txt existe
if [ ! -f "backend/requirements.txt" ]; then
    echo -e "${YELLOW}⚠️  requirements.txt não encontrado${NC}"
else
    # Ativar venv se existir
    if [ -d "venv/bin" ]; then
        source venv/bin/activate
        echo -e "${GREEN}✅ Virtual env ativado${NC}"
    elif [ -d "venv/Scripts" ]; then
        source venv/Scripts/activate
        echo -e "${GREEN}✅ Virtual env ativado${NC}"
    fi
    
    # Instalar pacotes (se necessário)
    if ! python3 -c "import fastapi" 2>/dev/null; then
        echo "Instalando dependências Python..."
        # pip install -r backend/requirements.txt
        echo -e "${YELLOW}⚠️  Execute manualmente: pip install -r backend/requirements.txt${NC}"
    else
        echo -e "${GREEN}✅ Dependências Python já instaladas${NC}"
    fi
fi

echo ""

# ==========================================
# 3. Instalar dependências Frontend
# ==========================================
echo -e "${BLUE}[3/4]${NC} Configurando Frontend..."

if [ -f "frontend/package.json" ]; then
    cd frontend
    
    if [ ! -d "node_modules" ]; then
        echo "Instalando dependências npm..."
        npm install
        echo -e "${GREEN}✅ Dependências npm instaladas${NC}"
    else
        echo -e "${GREEN}✅ Dependências npm já instaladas${NC}"
    fi
    
    cd ..
else
    echo -e "${YELLOW}⚠️  package.json não encontrado${NC}"
fi

echo ""

# ==========================================
# 4. Instruções finais
# ==========================================
echo -e "${BLUE}[4/4]${NC} Instruções de inicialização..."
echo ""

echo -e "${YELLOW}Para iniciar o Dashboard, execute:${NC}"
echo ""

echo -e "${GREEN}Backend (Terminal 1):${NC}"
echo "  cd backend"
echo "  python -m uvicorn main_enterprise:app --reload"
echo ""

echo -e "${GREEN}Frontend (Terminal 2):${NC}"
echo "  cd frontend"
echo "  npm start"
echo ""

echo -e "${GREEN}Acessar Dashboard:${NC}"
echo "  http://localhost:3000/dashboard"
echo ""

echo -e "${YELLOW}Testes:${NC}"
echo "  pytest tests/test_dashboard.py -v"
echo ""

echo -e "${GREEN}✅ Setup completo!${NC}"
echo ""
