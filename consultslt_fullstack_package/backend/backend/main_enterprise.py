import logging
import importlib
from pathlib import Path
from contextlib import asynccontextmanager

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from starlette.responses import JSONResponse

from backend.core.database import init_db, close_db

# ------------------------------------------------
# LOGGING (ESSENCIAL PARA O RESTO DO CÓDIGO)
# ------------------------------------------------
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(name)s - %(message)s"
)
logger = logging.getLogger("consult_slt")

# ------------------------------------------------
# LIFESPAN
# ------------------------------------------------
@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("🚀 Iniciando Consult SLT Web Enterprise...")
    try:
        await init_db()
        logger.info("✅ MongoDB conectado")
    except Exception as e:
        logger.error(f"❌ Falha ao conectar MongoDB: {e}")
    yield
    await close_db()
    logger.info("🛑 Aplicação finalizada")

# ------------------------------------------------
# APP
# ------------------------------------------------
app = FastAPI(
    title="Consult SLT Web Enterprise",
    description="API Enterprise - Gestão Fiscal e Empresarial",
    version="1.0.0",
    lifespan=lifespan
)

# ------------------------------------------------
# CORS
# ------------------------------------------------
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ------------------------------------------------
# ERROR HANDLER
# ------------------------------------------------
@app.middleware("http" )
async def log_exceptions(request: Request, call_next):
    try:
        return await call_next(request)
    except Exception:
        logger.exception("Erro na requisição")
        return JSONResponse(status_code=500, content={"detail": "Internal Server Error"})

# ------------------------------------------------
# ROOT
# ------------------------------------------------
@app.get("/", tags=["Health"])
async def root():
    return {"status": "online", "service": "Consult SLT Web Enterprise", "database": "MongoDB"}

# ------------------------------------------------
# AUTO LOAD ROUTERS (SEÇÃO CORRIGIDA)
# ------------------------------------------------
ROUTERS_PATH = Path(__file__).parent / "routers"
loaded_routers_count = 0

if ROUTERS_PATH.exists() and ROUTERS_PATH.is_dir():
    logger.info("🔎 Procurando por routers na pasta 'backend/routers'...")
    for file in sorted(ROUTERS_PATH.glob("*.py")):
        if file.name.startswith("__"):
            continue

        module_name = f"backend.routers.{file.stem}"
        try:
            module = importlib.import_module(module_name)
            if hasattr(module, "router"):
                prefix = f"/api/{file.stem}"
                
                # A correção principal: não forçar o 'tag'
                app.include_router(
                    module.router,
                    prefix=prefix
                )

                loaded_routers_count += 1
                logger.info(f"✅ Router '{file.stem}' carregado com sucesso no prefixo '{prefix}'")
        except Exception as e:
            logger.error(f"❌ Erro ao carregar o router '{module_name}': {e}")

logger.info(f"Total de routers carregados: {loaded_routers_count}")
# ------------------------------------------------

# ------------------------------------------------
# START SERVER
# ------------------------------------------------
if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main_enterprise:app", host="0.0.0.0", port=8000, reload=True)
