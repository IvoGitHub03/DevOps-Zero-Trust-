from fastapi import FastAPI, Depends, HTTPException
from backend.security import verify_token
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from jose import jwt, JWTError

from backend.auth import router as auth_router
from backend.rbac import router as rbac_router
from backend.documents import router as docs_router
from backend.security import SECRET_KEY, ALGORITHM
from backend.policy import router as policy_router


# ---------------------------------------------------------
# Initialize app
# ---------------------------------------------------------
app = FastAPI(
    title="Zero Trust Access System",
    description="Backend with MFA, RBAC, Documents, Admin Panel",
    version="1.0.0"
)

# ---------------------------------------------------------
# Security (Bearer Token)
# ---------------------------------------------------------
security = HTTPBearer()


def verify_token(credentials: HTTPAuthorizationCredentials = Depends(security)):
    """
    Automatically validates token for protected endpoints.
    """
    token = credentials.credentials

    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload  # contains: sub (username), role (admin/user)
    except JWTError:
        raise HTTPException(status_code=403, detail="Invalid or expired token")


# ---------------------------------------------------------
# CORS
# ---------------------------------------------------------
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# ---------------------------------------------------------
# Public route
# ---------------------------------------------------------
@app.get("/health")
def health_check():
    return {"status": "ok"}


# ---------------------------------------------------------
# Protected test endpoint
# ---------------------------------------------------------
@app.get("/protected")
def protected_route(user=Depends(verify_token)):
    return {"message": "Access granted", "user": user}


# ---------------------------------------------------------
# Routers (some are public, some protected)
# ---------------------------------------------------------
app.include_router(auth_router, prefix="/auth", tags=["auth"])

# Protected routers — automatically require Bearer token
app.include_router(docs_router, prefix="", tags=["documents"], dependencies=[Depends(verify_token)])
app.include_router(policy_router, prefix="/admin", tags=["admin"], dependencies=[Depends(verify_token)])
app.include_router(rbac_router, prefix="/admin", tags=["admin"], dependencies=[Depends(verify_token)])
