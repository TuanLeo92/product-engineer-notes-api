from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.core.deps import get_db, get_current_user
from app.models.user import User
from app.schemas.note_schema import (
    NoteCreate,
    NoteListResponse,
    EnvelopeDelete,
    EnvelopeNote,
    EnvelopeNoteList,
)

from app.services import note_service
from app.core.response import success_response
from typing import Optional

router = APIRouter(prefix="/notes", tags=["notes"])


@router.post("/", response_model=EnvelopeNote)
def create_note(data: NoteCreate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    note = note_service.create_note(db, data, current_user.id)
    return success_response(note)

@router.get("/", response_model=EnvelopeNoteList)
def get_notes(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    notes = note_service.get_notes(db, current_user.id)
    return success_response(notes)

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

@router.get("/{note_id}", response_model=EnvelopeNote)
def get_note(note_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    note = note_service.get_note(db, note_id, current_user.id)
    if not note:
        raise HTTPException(status_code=404, detail="Note not found")
    return success_response(note)

@router.put("/{note_id}", response_model=EnvelopeNote)
def update_note(note_id: int, data: NoteCreate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    note = note_service.update_note(db, note_id, current_user.id, data)
    if not note:
        raise HTTPException(status_code=404, detail="Note not found")
    return success_response(note)

@router.delete("/{note_id}", response_model=EnvelopeDelete)
def delete_note(note_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    result = note_service.delete_note(db, note_id, current_user.id)
    if not result:
        raise HTTPException(status_code=404, detail="Note not found")
    return success_response(result)
