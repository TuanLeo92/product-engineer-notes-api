from sqlalchemy.orm import Session
from app.repositories.note_repository import NoteRepository
from app.schemas.note_schema import NoteCreate, NoteResponse, DeleteResponse
from typing import Optional
from app.models.note import Note

repository = NoteRepository()

def create_note(db: Session, data: NoteCreate, user_id: int) -> Note:
    return repository.create(db, user_id, data.title, data.content)

def get_notes(db: Session, user_id: int) -> list[Note]:
    return repository.get_all(db, user_id)

def get_note(db: Session, note_id: int, user_id: int) -> Optional[Note]:
    return repository.get_by_id(db, note_id, user_id)

def update_note(db: Session, note_id: int, user_id: int, data: NoteCreate) -> Optional[Note]:
    return repository.update(db, note_id, user_id, data.title, data.content)

def delete_note(db: Session, note_id: int, user_id: int) -> Optional[DeleteResponse]:
    if repository.delete(db, note_id, user_id):
        return DeleteResponse(message="Note deleted successfully")
    return None

def search_notes(
    db: Session,
    user_id: int,
    query: Optional[str],
    page: int,
    page_size: int,
) -> dict:
    # Build twice: some SQLAlchemy versions alter the query after `.count()`.
    total, items = repository.search(db, user_id, query, page, page_size)
    return {"items": items, "total": total}