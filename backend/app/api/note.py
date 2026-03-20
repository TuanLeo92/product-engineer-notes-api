from datetime import datetime, timezone
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.core.deps import get_db, get_current_user
from app.models.note import Note
from app.models.user import User
from app.schemas.note_schema import NoteCreate, NoteResponse

router = APIRouter(prefix="/notes", tags=["notes"])

def _ensure_updated_at(note: Note) -> None:
    """
    Older rows in the DB may have `updated_at` = NULL.
    Pydantic expects `updated_at` to be a real datetime, so we normalize it before returning.
    """
    if note.updated_at is None:
        # Prefer created_at if present; otherwise fall back to current time.
        note.updated_at = note.created_at or datetime.now(timezone.utc)

@router.post("/", response_model=NoteResponse)
def create_note(data: NoteCreate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    note = Note(title=data.title, content=data.content, user_id=current_user.id)

    db.add(note)
    db.commit()
    db.refresh(note)

    # Some existing DB rows/tables may not have updated_at defaults yet.
    # Ensure response validation passes.
    if note.updated_at is None:
        note.updated_at = datetime.now(timezone.utc)

    return note

@router.get("/", response_model=list[NoteResponse])
def get_notes(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    notes = db.query(Note).filter(Note.user_id == current_user.id).all()
    for n in notes:
        _ensure_updated_at(n)
    return notes

@router.get("/{note_id}", response_model=NoteResponse)
def get_note(note_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    note = db.query(Note).filter(Note.id == note_id, Note.user_id == current_user.id).first()
    if not note:
        raise HTTPException(status_code=404, detail="Note not found")
    _ensure_updated_at(note)
    return note

@router.put("/{note_id}", response_model=NoteResponse)
def update_note(note_id: int, data: NoteCreate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    note = db.query(Note).filter(Note.id == note_id, Note.user_id == current_user.id).first()
    if not note:
        raise HTTPException(status_code=404, detail="Note not found")
    
    note.title = data.title
    note.content = data.content
    note.updated_at = datetime.now(timezone.utc)
    db.commit()
    db.refresh(note)
    return note

@router.delete("/{note_id}", response_model=NoteResponse)
def delete_note(note_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    note = db.query(Note).filter(Note.id == note_id, Note.user_id == current_user.id).first()
    if not note:
        raise HTTPException(status_code=404, detail="Note not found")
    db.delete(note)
    db.commit()
    _ensure_updated_at(note)
    return note
