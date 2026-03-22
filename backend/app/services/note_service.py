from sqlalchemy.orm import Session
from sqlalchemy import or_
from datetime import datetime, timezone
from typing import Optional

from app.models.note import Note
from app.schemas.note_schema import DeleteResponse, NoteCreate

def create_note(db: Session, data: NoteCreate, user_id: int) -> Note:
    new_note = Note(title=data.title, content=data.content, user_id=user_id)
    db.add(new_note)
    db.commit()
    db.refresh(new_note)
    _ensure_updated_at(new_note)
    return new_note

def get_notes(db: Session, user_id: int) -> list[Note]:
    notes = db.query(Note).filter(Note.user_id == user_id).all()
    for n in notes:
        _ensure_updated_at(n)
    return notes

def get_note(db: Session, note_id: int, user_id: int) -> Optional[Note]:
    existing_note = db.query(Note).filter(Note.id == note_id, Note.user_id == user_id).first()
    if existing_note is None:
        return None
    _ensure_updated_at(existing_note)
    return existing_note

def update_note(db: Session, note_id: int, user_id: int, data: NoteCreate) -> Optional[Note]:
    existing_note = db.query(Note).filter(Note.id == note_id, Note.user_id == user_id).first()
    if existing_note is None:
        return None
    existing_note.title = data.title
    existing_note.content = data.content
    existing_note.updated_at = datetime.now(timezone.utc)
    db.commit()
    db.refresh(existing_note)
    return existing_note

def delete_note(db: Session, note_id: int, user_id: int) -> Optional[DeleteResponse]:
    existing_note = db.query(Note).filter(Note.id == note_id, Note.user_id == user_id).first()
    if existing_note is None:
        return None
    _ensure_updated_at(existing_note)
    db.delete(existing_note)
    db.commit()
    return DeleteResponse(message="Note deleted successfully")

def _notes_search_base_query(db: Session, user_id: int, query: Optional[str]):
    q = db.query(Note).filter(Note.user_id == user_id)
    if query:
        pattern = f"%{query}%"
        q = q.filter(or_(Note.title.ilike(pattern), Note.content.ilike(pattern)))
    return q


def search_notes(
    db: Session,
    user_id: int,
    query: Optional[str],
    page: int,
    page_size: int,
) -> dict:
    # Build twice: some SQLAlchemy versions alter the query after `.count()`.
    total = _notes_search_base_query(db, user_id, query).count()
    notes = (
        _notes_search_base_query(db, user_id, query)
        .order_by(Note.updated_at.desc())
        .offset((page - 1) * page_size)
        .limit(page_size)
        .all()
    )
    for n in notes:
        _ensure_updated_at(n)

    return {"items": notes, "total": total}

def _ensure_updated_at(note: Note) -> None:
    """
    Older rows in the DB may have `updated_at` = NULL.
    Pydantic expects `updated_at` to be a real datetime, so we normalize it before returning.
    """
    if note is None:
        return
    if note.updated_at is None:
        # Prefer created_at if present; otherwise fall back to current time.
        note.updated_at = note.created_at or datetime.now(timezone.utc)
