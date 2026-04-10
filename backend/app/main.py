from fastapi import FastAPI
from app.core.database import Base, engine
from app.models import user, note

from app.api.auth import router as auth_router
from app.api.notes import router as note_router

from app.core.response import success_response, error_response
from fastapi import HTTPException
from fastapi.responses import JSONResponse
from fastapi.requests import Request

import logging

app = FastAPI(
    title="Notes API",
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_url="/openapi.json",
)

Base.metadata.create_all(bind=engine)


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@app.get("/", include_in_schema=False)
def root():
    """Public URL often has no path; point clients at interactive docs."""
    return {
        "message": "Notes API",
        "docs": "/docs",
        "redoc": "/redoc",
        "openapi": "/openapi.json",
        "health": "/health",
    }


@app.get("/health")
def health():
    """Liveness for Railway: do not hit DB here (DB issues caused flaky deploys / 502)."""
    return {"status": "ok"}

app.include_router(auth_router)
app.include_router(note_router)

@app.exception_handler(HTTPException)
async def http_exception_handler(request: Request, exc: HTTPException):
    return JSONResponse(status_code=exc.status_code, content=error_response("HTTP_ERROR", exc.detail))

@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    logger.error(f"An unexpected error occurred: {exc}")
    return JSONResponse(status_code=500, content=error_response("INTERNAL_SERVER_ERROR", "An unexpected error occurred"))