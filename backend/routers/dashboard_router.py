from fastapi import APIRouter, Depends
from backend.services.dashboard import DashboardService
from backend.core.database import get_database

router = APIRouter()


@router.get("/dashboard", tags=["Dashboard"])
async def get_dashboard_data(db=Depends(get_database)):
    """
    Rota para obter dados do dashboard com KPIs reais.
    Os KPIs são calculados a partir das coleções do MongoDB.
    """
    dashboard_service = DashboardService(db)

    # KPIs reais (coleções: empresas, alertas, obrigações etc.)
    kpis = await dashboard_service.calcular_kpis_atuais()

    # próximos vencimentos (obrigações)
    proximos = await dashboard_service.calcular_proximos_vencimentos()

    # monta resposta
    return {
        "data": {
            **kpis,
            "proximos_vencimentos": proximos
        }
    }