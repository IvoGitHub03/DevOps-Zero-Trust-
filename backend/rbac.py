import os
from fastapi import APIRouter
from backend.data_utils import read_json

router = APIRouter()

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
ROLES_PATH = os.path.join(BASE_DIR, "data", "roles.json")


def role_has_permission(role: str, permission: str) -> bool:
    roles = read_json(ROLES_PATH)
    return permission in roles.get(role, [])


@router.get("/roles")
def list_roles():
    return read_json(ROLES_PATH)
