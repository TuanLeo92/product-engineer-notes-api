from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.core.deps import get_db, get_current_user
from app.models.note import Note
from app.models.user import User
from app.schemas.note_schema import NoteCreate, NoteResponse, DeleteResponse, NoteListResponse

from app.services import note_service

from typing import Optional

router = APIRouter(prefix="/notes", tags=["notes"])


@router.post("/", response_model=NoteResponse)
def create_note(data: NoteCreate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    return note_service.create_note(db, data, current_user.id)

@router.get("/", response_model=list[NoteResponse])
def get_notes(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    return note_service.get_notes(db, current_user.id)

# Static paths must be registered BEFORE /{note_id}, otherwise "search" is parsed as an integer id → 422.
@router.get("/search", response_model=NoteListResponse)
def search_notes(
    query: Optional[str] = None,
    page: int = 1,
    page_size: int = 10,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return note_service.search_notes(db, current_user.id, query, page, page_size)

@router.get("/{note_id}", response_model=NoteResponse)
def get_note(note_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    note = note_service.get_note(db, note_id, current_user.id)
    if not note:
        raise HTTPException(status_code=404, detail="Note not found")
    return note

@router.put("/{note_id}", response_model=NoteResponse)
def update_note(note_id: int, data: NoteCreate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    note = note_service.update_note(db, note_id, current_user.id, data)
    if not note:
        raise HTTPException(status_code=404, detail="Note not found")
    return note

@router.delete("/{note_id}", response_model=DeleteResponse)
def delete_note(note_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    result = note_service.delete_note(db, note_id, current_user.id)
    if not result:
        raise HTTPException(status_code=404, detail="Note not found")
    return result
