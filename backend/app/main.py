import asyncio
import logging
from contextlib import asynccontextmanager

from fastapi import FastAPI, HTTPException
from fastapi.requests import Request
from fastapi.responses import JSONResponse

from app.core.database import Base, engine
from app.core.response import error_response
from app.models import user, note

from app.api.auth import router as auth_router
from app.api.notes import router as note_router

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Do not run create_all at import time: uvicorn imports this module before binding $PORT.
    A slow/unreachable DB would block startup → Railway healthcheck sees 'service unavailable'.
    """
    try:
        def _create_tables():
            Base.metadata.create_all(bind=engine)

        await asyncio.to_thread(_create_tables)
    except Exception:
        logger.exception("create_all failed; API will still start (fix DATABASE_URL / Postgres)")
    yield


app = FastAPI(
    title="Notes API",
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_url="/openapi.json",
    lifespan=lifespan,
)


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