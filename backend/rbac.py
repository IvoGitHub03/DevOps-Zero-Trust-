from backend.data_utils import read_json
from fastapi import APIRouter
from backend.data_utils import read_json

router = APIRouter()
ROLES_PATH = "backend/data/roles.json"

def role_has_permission(role: str, permission: str) -> bool:
    roles = read_json(ROLES_PATH)
    return permission in roles.get(role, [])


@router.get("/roles")
def list_roles():
    return read_json(ROLES_PATH)


ROLES_PATH = "backend/data/roles.json"

def role_has_permission(role: str, permission: str) -> bool:
    roles = read_json(ROLES_PATH)
    return permission in roles.get(role, [])
def role_has_permission(role: str, permission: str) -> bool:
    if permission is None:
        return False
    roles = read_json(ROLES_PATH)
    return permission in roles.get(role, [])
