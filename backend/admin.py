from fastapi import APIRouter, Depends, HTTPException
from backend.security import verify_jwt
from backend.rbac import role_has_permission
from backend.policy import required_permission
from backend.data_utils import read_json, write_json

router = APIRouter()
USERS_PATH = "backend/data/users.json"

def policy_check(user, action):
    role = user["role"]
    needed_perm = required_permission(action)
    if not role_has_permission(role, needed_perm):
        raise HTTPException(403, "Access denied")

@router.get("/users")
def list_users(user=Depends(verify_jwt)):
    policy_check(user, "admin:users")
    return read_json(USERS_PATH)

@router.post("/update-role")
def update_role(data: dict, user=Depends(verify_jwt)):
    policy_check(user, "admin:users")

    username = data["username"]
    new_role = data["role"]

    users = read_json(USERS_PATH)
    updated = False

    for u in users:
        if u["username"] == username:
            u["role"] = new_role
            updated = True

    if not updated:
        raise HTTPException(404, "User not found")

    write_json(USERS_PATH, users)
    return {"msg": "Role updated"}
