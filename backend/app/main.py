from fastapi import FastAPI

from app.db import check_connection
from app.requests.routes import router as request_router

app = FastAPI()
app.include_router(request_router)


@app.get("/health")
def health():
    return {"status": "ok"}


@app.get("/health/db")
def health_db():
    try:
        check_connection()
    except Exception as exc:
        return {"status": "error", "detail": type(exc).__name__}
    return {"status": "ok"}
