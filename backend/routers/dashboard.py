from fastapi import APIRouter, Depends, HTTPException
from backend.services.dashboard import DashboardService
from backend.core.database import get_database


# ==========================================================
# ROUTER
# ==========================================================

router = APIRouter(
    prefix="/dashboard",
    tags=["Dashboard"]
)


# ==========================================================
# DASHBOARD PRINCIPAL
# ==========================================================

@router.get("/")
async def get_dashboard_data(db=Depends(get_database)):
    """
    Retorna KPIs principais do dashboard.
    """
    try:
        dashboard_service = DashboardService(db)

        kpis = await dashboard_service.calcular_kpis_atuais()

        return {
            "success": True,
            "module": "dashboard",
            "data": kpis
        }

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Erro ao carregar dashboard: {str(e)}"
        )


# ==========================================================
# HEALTH DASHBOARD
# ==========================================================

@router.get("/health")
async def dashboard_health():
    """
    Health check do módulo dashboard.
    """
    return {
        "success": True,
        "module": "dashboard",
        "status": "online"
    }


# ==========================================================
# KPIS RAW
# ==========================================================

@router.get("/kpis")
async def get_dashboard_kpis(db=Depends(get_database)):
    """
    Retorna apenas os KPIs.
    """
    try:
        dashboard_service = DashboardService(db)

        kpis = await dashboard_service.calcular_kpis_atuais()

        return kpis

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Erro ao obter KPIs: {str(e)}"
        )