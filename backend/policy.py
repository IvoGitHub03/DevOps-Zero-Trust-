import os
from fastapi import APIRouter
from backend.data_utils import read_json

router = APIRouter()

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
POLICIES_PATH = os.path.join(BASE_DIR, "data", "policies.json")


@router.post("/update-role")
def update_role():
    return {"msg": "Not implemented yet"}


def required_permission(action: str):
    policies = read_json(POLICIES_PATH)
    return policies["resources"].get(action, {}).get("required_permission")
