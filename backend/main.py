from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from backend import auth, documents, admin

app = FastAPI(title="Zero Trust Access System")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router, prefix="/auth")
app.include_router(documents.router, prefix="/documents")
app.include_router(admin.router, prefix="/admin")

@app.get("/health")
def health():
    return {"status": "ok"}
