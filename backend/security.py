from fastapi import HTTPException, Header
from jose import jwt

SECRET_KEY = "super-secret-key"
ALGORITHM = "HS256"

def decode_token(token: str):
    try:
        return jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    except Exception:
        return None

def verify_jwt(authorization: str | None = Header(None)):
    if not authorization:
        raise HTTPException(403, "Missing token")

    token = authorization.replace("Bearer ", "")
    data = decode_token(token)

    if not data:
        raise HTTPException(403, "Invalid token")

    return data   # { "sub": username, "role": role }
from fastapi import Depends, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from jose import jwt, JWTError
from backend.security import SECRET_KEY, ALGORITHM

security = HTTPBearer()

def verify_token(credentials: HTTPAuthorizationCredentials = Depends(security)):
    token = credentials.credentials
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except JWTError:
        raise HTTPException(403, "Invalid or expired token")
