import sys
import logging
import importlib
import uuid
import traceback

from pathlib import Path
from contextlib import asynccontextmanager

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from starlette.middleware.base import BaseHTTPMiddleware


# ==========================================================
# PATH CONFIG
# ==========================================================

BASE_DIR = Path(__file__).resolve().parent.parent

if str(BASE_DIR) not in sys.path:
    sys.path.insert(0, str(BASE_DIR))


# ==========================================================
# LOGGING
# ==========================================================

LOG_FILE = BASE_DIR / "backend_debug.log"

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
    handlers=[
        logging.FileHandler(LOG_FILE, encoding="utf-8"),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger("consultslt.enterprise")


# ==========================================================
# DATABASE IMPORT (SAFE)
# ==========================================================

try:
    from backend.core.database import init_db, close_db
except Exception as e:
    logger.warning(f"⚠️ Falha ao importar database.py: {e}")

    async def init_db():
        logger.warning("⚠️ init_db() mock executado")

    async def close_db():
        logger.warning("⚠️ close_db() mock executado")


# ==========================================================
# LIFESPAN
# ==========================================================

@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("🚀 Starting Consult SLT Enterprise API")

    try:
        await init_db()
        logger.info("✅ Database connected")
    except Exception as e:
        logger.error(f"❌ Database connection failed: {e}")
        raise

    yield

    try:
        await close_db()
        logger.info("🛑 Application shutdown complete")
    except Exception as e:
        logger.error(f"❌ Error closing database: {e}")


# ==========================================================
# FASTAPI INIT
# ==========================================================

app = FastAPI(
    title="Consult SLT Web Enterprise",
    description="Enterprise Fiscal Management API",
    version="2.0.0",
    lifespan=lifespan
)


# ==========================================================
# CORS
# ==========================================================

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "http://127.0.0.1:3000",
        "http://localhost:5173",
        "http://127.0.0.1:5173",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ==========================================================
# REQUEST TRACE MIDDLEWARE
# ==========================================================

class RequestTracingMiddleware(BaseHTTPMiddleware):

    async def dispatch(self, request: Request, call_next):
        request_id = str(uuid.uuid4())
        request.state.request_id = request_id

        logger.info(
            f"[REQ] {request.method} {request.url.path} | id={request_id}"
        )

        response = await call_next(request)
        response.headers["X-Request-ID"] = request_id

        return response


app.add_middleware(RequestTracingMiddleware)


# ==========================================================
# GLOBAL ERROR HANDLER
# ==========================================================

@app.middleware("http")
async def global_exception_handler(request: Request, call_next):
    try:
        return await call_next(request)

    except Exception:
        logger.error(f"🔥 Error in {request.url.path}")
        logger.error(traceback.format_exc())

        return JSONResponse(
            status_code=500,
            content={
                "success": False,
                "error": "internal_server_error",
                "path": request.url.path,
                "request_id": getattr(request.state, "request_id", None)
            }
        )


# ==========================================================
# HEALTH ROUTES
# ==========================================================

@app.get("/", tags=["System"])
async def root():
    return {
        "success": True,
        "message": "Consult SLT Enterprise API Online"
    }


@app.get("/health", tags=["System"])
async def health():
    return {
        "success": True,
        "status": "healthy"
    }


@app.get("/health/details", tags=["System"])
async def health_details():
    return {
        "success": True,
        "app": "Consult SLT Enterprise",
        "version": "2.0.0"
    }


# ==========================================================
# AUTO LOAD ROUTERS
# ==========================================================

ROUTERS_DIR = Path(__file__).parent / "routers"
loaded = 0
failed = 0

if ROUTERS_DIR.exists():

    for router_file in ROUTERS_DIR.glob("*.py"):

        if router_file.name.startswith("__"):
            continue

        module_name = f"backend.routers.{router_file.stem}"

        try:
            module = importlib.import_module(module_name)

            if not hasattr(module, "router"):
                logger.warning(f"⚠️ Sem objeto router: {module_name}")
                continue

            app.include_router(module.router)

            loaded += 1
            logger.info(f"✅ Loaded router: {module_name}")

        except Exception as e:
            failed += 1
            logger.error(
                f"❌ Failed loading router {module_name}: {str(e)}"
            )

else:
    logger.warning("⚠️ Pasta backend/routers não encontrada")


logger.info(f"📦 Routers loaded: {loaded}")
logger.info(f"📦 Routers failed: {failed}")


# ==========================================================
# MANUAL EXTRA ROUTERS
# ==========================================================

try:
    from backend.routers.dashboard_router import router as dashboard_router
    app.include_router(dashboard_router)
    logger.info("✅ dashboard_router loaded manually")
except Exception as e:
    logger.warning(f"⚠️ dashboard_router not loaded: {e}")


# ==========================================================
# STARTUP SUMMARY
# ==========================================================

@app.on_event("startup")
async def startup_summary():
    logger.info("=" * 60)
    logger.info("🚀 Consult SLT Enterprise Running")
    logger.info("📍 Swagger: http://localhost:8000/docs")
    logger.info("📍 ReDoc  : http://localhost:8000/redoc")
    logger.info("=" * 60)


# ==========================================================
# DEV SERVER
# ==========================================================

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        "backend.main_enterprise:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )