from backend.data_utils import read_json

ROLES_PATH = "backend/data/roles.json"

def role_has_permission(role: str, permission: str) -> bool:
    roles = read_json(ROLES_PATH)
    return permission in roles.get(role, [])
