"""
Endpoints da API - Versão Corrigida
Centraliza e exporta todos os routers da aplicação
"""
from fastapi import APIRouter

# Importação das rotas individuais
try:
    from .health import router as health_router
    from .sharepoint import router as sharepoint_router
    from .documentos import router as documentos_router
    from .obrigacoes import router as obrigacoes_router
    from .robots import router as robots_router
    from .fiscal import router as fiscal_router
    from .auditoria import router as auditoria_router
    from .ocr import router as ocr_router
except ImportError as e:
    # Log de erro para ajudar a identificar qual arquivo de rota está falhando
    print(f"Erro ao importar rotas em api/__init__.py: {e}")
    raise

# Criação do roteador principal da API
api_router = APIRouter()

# Inclusão de todas as rotas no roteador principal
api_router.include_router(health_router, prefix="/health", tags=["Health"])
api_router.include_router(sharepoint_router, prefix="/sharepoint", tags=["SharePoint"])
api_router.include_router(documentos_router, prefix="/documentos", tags=["Documentos"])
api_router.include_router(obrigacoes_router, prefix="/obrigacoes", tags=["Obrigações"])
api_router.include_router(robots_router, prefix="/robots", tags=["Robots"])
api_router.include_router(fiscal_router, prefix="/fiscal", tags=["Fiscal"])
api_router.include_router(auditoria_router, prefix="/auditoria", tags=["Auditoria"])
api_router.include_router(ocr_router, prefix="/ocr", tags=["OCR"])

# Exportação explícita para o main_enterprise.py
__all__ = [
    'api_router',
    'health_router',
    'sharepoint_router',
    'documentos_router',
    'obrigacoes_router',
    'robots_router',
    'fiscal_router',
    'auditoria_router',
    'ocr_router'
]