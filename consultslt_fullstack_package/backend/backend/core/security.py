
from jose import jwt
from datetime import datetime, timedelta
from passlib.context import CryptContext

SECRET = "SUPER_SECRET_KEY"
ALGORITHM = "HS256"

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash_password(p):
    return pwd_context.hash(p)

def verify_password(p, h):
    return pwd_context.verify(p, h)

def create_token(data: dict):
    data["exp"] = datetime.utcnow() + timedelta(hours=12)
    return jwt.encode(data, SECRET, algorithm=ALGORITHM)
