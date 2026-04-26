from fastapi.security import HTTPBearer
from fastapi import Depends, HTTPException
from jose import JWTError
from app.core.security import decode_token

security = HTTPBearer()


def get_current_user(credentials=Depends(security)):
    token = credentials.credentials

    try:
        payload = decode_token(token)

        if payload.get("type") != "access":
            raise HTTPException(status_code=401, detail="Invalid token type")

        return payload

    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid or expired token")