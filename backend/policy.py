from backend.data_utils import read_json

POLICIES_PATH = "backend/data/policies.json"

def required_permission(action: str):
    policies = read_json(POLICIES_PATH)
    return policies["resources"].get(action, {}).get("required_permission")
