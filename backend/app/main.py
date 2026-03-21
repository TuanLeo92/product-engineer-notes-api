from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from app.core.deps import get_db
from app.core.database import Base, engine
from app.models import user, note

from app.api.auth import router as auth_router
from app.api.notes import router as note_router

app = FastAPI()

Base.metadata.create_all(bind=engine)

@app.get("/health")
def health(db: Session = Depends(get_db)):
    return {"status": "ok"}

app.include_router(auth_router)
app.include_router(note_router)