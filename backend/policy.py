from backend.data_utils import read_json
from fastapi import APIRouter

router = APIRouter()

@router.post("/update-role")
def update_role():
    ...


POLICIES_PATH = "backend/data/policies.json"

def required_permission(action: str):
    policies = read_json(POLICIES_PATH)
    return policies["resources"].get(action, {}).get("required_permission")
def required_permission(action: str):
    policies = read_json(POLICIES_PATH)
    perm = policies["resources"].get(action, {}).get("required_permission")
    if perm is None:
        raise KeyError(f"Missing policy for action: {action}")
    return perm
def required_permission(action: str):
    policies = read_json(POLICIES_PATH)
    perm = policies["resources"].get(action, {}).get("required_permission")
    if perm is None:
        raise HTTPException(500, f"Policy missing for action '{action}'")
    return perm
