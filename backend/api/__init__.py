from fastapi import APIRouter

api_router = APIRouter()

from .obrigacoes import router as obrigacoes_router
from .dashboard_metrics import router as dashboard_metrics_router
from .auditoria import router as auditoria_router
from .documentos import router as documentos_router

api_router.include_router(obrigacoes_router)
api_router.include_router(dashboard_metrics_router)
api_router.include_router(auditoria_router)
api_router.include_router(documentos_router, prefix="/api/documentos")
