"""
Serviço de Autenticação via Entra ID (Azure AD)
Implementa OAuth 2.0 para integração com Microsoft Graph
"""

import os
import requests
import logging
from fastapi import HTTPException, status

logger = logging.getLogger(__name__)


class EntraIDAuthService:
    """Serviço de autenticação via Entra ID (Azure AD)"""

    def __init__(self):
        """Inicializa serviço com credenciais do Entra ID"""
        self.client_id = os.getenv("ENTRA_ID_CLIENT_ID")
        self.client_secret = os.getenv("ENTRA_ID_CLIENT_SECRET")
        self.tenant_id = os.getenv("ENTRA_ID_TENANT_ID")
        self.authority = os.getenv(
            "ENTRA_ID_AUTHORITY",
            f"https://login.microsoftonline.com/{self.tenant_id}"
        )
        self.redirect_uri = os.getenv("OAUTH_REDIRECT_URI")

        # Scopes necessários para SharePoint e Graph
        self.scopes = [
            "https://graph.microsoft.com/.default"
        ]

        if not all([self.client_id, self.client_secret, self.tenant_id]):
            raise ValueError("Credenciais do Entra ID não configuradas")

        logger.info(f"EntraIDAuthService inicializado para tenant {self.tenant_id}")

    def get_authorization_url(self, state: str = None) -> str:
        """
        Gera URL de autorização para redirecionar usuário ao Entra ID
        """
        params = {
            "client_id": self.client_id,
            "response_type": "code",
            "redirect_uri": self.redirect_uri,
            "scope": " ".join(self.scopes),
            "response_mode": "query",
            "prompt": "select_account"
        }
        if state:
            params["state"] = state

        auth_url = f"{self.authority}/oauth2/v2.0/authorize?"
        auth_url += "&".join([f"{k}={v}" for k, v in params.items()])
        return auth_url

    def get_token_from_code(self, code: str) -> dict:
        """
        Troca authorization code por access token
        """
        token_url = f"{self.authority}/oauth2/v2.0/token"
        data = {
            "client_id": self.client_id,
            "client_secret": self.client_secret,
            "code": code,
            "redirect_uri": self.redirect_uri,
            "grant_type": "authorization_code",
            "scope": " ".join(self.scopes)
        }
        response = requests.post(token_url, data=data, timeout=10)
        if response.status_code != 200:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Erro ao obter token: {response.text}"
            )
        return response.json()

    def get_client_credentials_token(self) -> str:
        """
        Obtém access token usando Client Credentials (para serviços backend)
        """
        token_url = f"{self.authority}/oauth2/v2.0/token"
        data = {
            "client_id": self.client_id,
            "client_secret": self.client_secret,
            "grant_type": "client_credentials",
            "scope": " ".join(self.scopes)
        }
        response = requests.post(token_url, data=data, timeout=10)
        if response.status_code != 200:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Erro ao obter token via client credentials: {response.text}"
            )
        token_response = response.json()
        return token_response.get("access_token")

    def get_user_info(self, access_token: str) -> dict:
        """
        Obtém informações do usuário autenticado via Graph
        """
        headers = {"Authorization": f"Bearer {access_token}"}
        response = requests.get("https://graph.microsoft.com/v1.0/me", headers=headers, timeout=10)
        if response.status_code != 200:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Erro ao obter informações do usuário"
            )
        return response.json()


# Função utilitária para uso direto nos endpoints
async def get_access_token() -> str:
    """
    Retorna access token válido para chamadas ao Graph
    """
    service = EntraIDAuthService()
    return service.get_client_credentials_token()
