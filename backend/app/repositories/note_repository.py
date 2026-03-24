from sqlalchemy.orm import Session
from sqlalchemy import or_
from datetime import datetime, timezone
from app.models.note import Note
from typing import Optional

class NoteRepository:

    def create(self, db: Session, user_id: int, title: str, content: Optional[str]) -> Note:
        note = Note(user_id=user_id, title=title, content=content)
        db.add(note)
        db.commit()
        db.refresh(note)
        self._ensure_updated_at(note)
        return note

    def get_all(self, db: Session, user_id: int):
        notes = db.query(Note).filter(Note.user_id == user_id).all()
        for note in notes:
            self._ensure_updated_at(note)
        return notes

    def get_by_id(self, db: Session, note_id: int, user_id: int):
        note = db.query(Note).filter(Note.id == note_id, Note.user_id == user_id).first()
        self._ensure_updated_at(note)
        return note

    def update(self, db: Session, note_id: int, user_id: int, title: str, content: Optional[str]) -> Optional[Note]:
        note = self.get_by_id(db, note_id, user_id)
        if note is None:
            return None
        note.title = title
        note.content = content
        note.updated_at = datetime.now(timezone.utc)
        db.commit()
        db.refresh(note)
        return note

    def delete(self, db: Session, note_id: int, user_id: int) -> bool:
        note = self.get_by_id(db, note_id, user_id)
        if note is None:
            return False
        db.delete(note)
        db.commit()
        return True

    def search(self, db: Session, user_id: int, query: Optional[str], page: int, page_size: int):
        def base_query():
            q = db.query(Note).filter(Note.user_id == user_id)
            if query:
                pattern = f"%{query}%"
                q = q.filter(or_(Note.title.ilike(pattern), Note.content.ilike(pattern)))
            return q

        total = base_query().count()
        items = (
            base_query()
            .order_by(Note.updated_at.desc())
            .offset((page - 1) * page_size)
            .limit(page_size)
            .all()
        )
        for n in items:
            self._ensure_updated_at(n)
        return total, items

    def _ensure_updated_at(self, note: Note) -> None:
        if note is None:
            return
        if note.updated_at is None:
            note.updated_at = note.created_at or datetime.now(timezone.utc)
