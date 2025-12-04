from fastapi import APIRouter, Depends, HTTPException
from backend.security import verify_jwt
from backend.rbac import role_has_permission
from backend.policy import required_permission
from backend.data_utils import read_json, write_json

router = APIRouter()
DOCS_PATH = "backend/data/documents.json"


def policy_check(user, action):
    role = user["role"]
    needed_perm = required_permission(action)

    if not role_has_permission(role, needed_perm):
        raise HTTPException(403, "Access denied")


@router.get("/")

def list_docs(user=Depends(verify_jwt)):
    policy_check(user, "documents:list")
    return read_json(DOCS_PATH)


@router.post("/documents/edit")
def edit_doc(data: dict, user=Depends(verify_jwt)):
    policy_check(user, "documents:edit")

    docs = read_json(DOCS_PATH)
    for d in docs:
        if d["id"] == data["id"]:
            d["title"] = data.get("title", d["title"])
            d["content"] = data.get("content", d["content"])
            write_json(DOCS_PATH, docs)
            return {"msg": "Updated"}

    raise HTTPException(404, "Not found")


@router.post("/documents/delete")
def delete_doc(data: dict, user=Depends(verify_jwt)):
    policy_check(user, "documents:delete")

    docs = read_json(DOCS_PATH)
    new_docs = [d for d in docs if d["id"] != data["id"]]

    if len(new_docs) == len(docs):
        raise HTTPException(404, "Not found")

    write_json(DOCS_PATH, new_docs)
    return {"msg": "Deleted"}
