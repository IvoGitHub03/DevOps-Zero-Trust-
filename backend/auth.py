from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from backend.data_utils import read_json
from backend.security import SECRET_KEY, ALGORITHM
from jose import jwt
import os

router = APIRouter()

# Absolute path to backend/data/users.json
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
USERS_PATH = os.path.join(BASE_DIR, "data", "users.json")

# ---------- Pydantic Models ----------
class LoginRequest(BaseModel):
    username: str
    password: str


class MfaRequest(BaseModel):
    username: str
    code: str


# ---------- LOGIN ----------
@router.post("/login")
def login(data: LoginRequest):
    username = data.username
    password = data.password

    users = read_json(USERS_PATH)

    for u in users:
        if u["username"] == username and u["password"] == password:
            return {
                "mfa_required": True,
                "username": username
            }

    raise HTTPException(status_code=401, detail="Invalid login")


# ---------- MFA VERIFY ----------
@router.post("/mfa")
def verify_mfa(data: MfaRequest):
    username = data.username
    code = data.code

    users = read_json(USERS_PATH)

    for u in users:
        if u["username"] == username and u["mfa_secret"] == code:

            token = jwt.encode({
                "sub": username,
                "role": u["role"]
            }, SECRET_KEY, algorithm=ALGORITHM)

            return {"token": token}

    raise HTTPException(status_code=401, detail="Invalid MFA code")

