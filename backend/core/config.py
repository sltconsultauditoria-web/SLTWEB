"""Configurações centralizadas do sistema ConsultSLT"""
import os
from pathlib import Path
from typing import Optional

try:
    from dotenv import load_dotenv
    _env_path = Path(__file__).parent.parent / ".env"
    if _env_path.exists():
        load_dotenv(_env_path)
except ImportError:
    pass


class Settings:
    """Configurações centralizadas da aplicação"""

    # MongoDB
    MONGO_URL: str = os.environ.get("MONGO_URL", "mongodb://127.0.0.1:27017")
    MONGO_DB_NAME: str = os.environ.get("MONGO_DB_NAME", os.environ.get("DB_NAME", "consultslt_db"))
    DB_NAME: str = MONGO_DB_NAME  # alias

    # JWT
    JWT_SECRET: str = os.environ.get("JWT_SECRET", "consultslt-secret-2026")
    JWT_ALGORITHM: str = os.environ.get("JWT_ALGORITHM", "HS256")
    JWT_EXPIRE_MINUTES: int = int(os.environ.get("JWT_EXPIRE_MINUTES", "1440"))

    # Azure AD / SharePoint
    AZURE_TENANT_ID: Optional[str] = os.environ.get("AZURE_TENANT_ID")
    AZURE_CLIENT_ID: Optional[str] = os.environ.get("AZURE_CLIENT_ID")
    AZURE_CLIENT_SECRET: Optional[str] = os.environ.get("AZURE_CLIENT_SECRET")
    SHAREPOINT_SITE_URL: Optional[str] = os.environ.get("SHAREPOINT_SITE_URL")
    SHAREPOINT_DRIVE_ID: Optional[str] = os.environ.get("SHAREPOINT_DRIVE_ID")

    # Armazenamento
    LOCAL_STORAGE_PATH: Path = Path(os.environ.get("LOCAL_STORAGE_PATH", "/tmp/uploads"))

    # Auto-start
    AUTO_START_INGESTION: bool = os.environ.get("AUTO_START_INGESTION", "false").lower() == "true"

    # CORS
    CORS_ORIGINS: str = os.environ.get(
        "CORS_ORIGINS",
        "http://localhost:3000,http://127.0.0.1:3000,http://192.168.5.162:3000"
    )

    @property
    def sharepoint_configured(self) -> bool:
        """Verifica se SharePoint está configurado"""
        return all([
            self.AZURE_TENANT_ID,
            self.AZURE_CLIENT_ID,
            self.AZURE_CLIENT_SECRET,
            self.SHAREPOINT_SITE_URL
        ])


settings = Settings()
