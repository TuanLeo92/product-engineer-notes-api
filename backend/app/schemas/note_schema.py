from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime

class NoteCreate(BaseModel):
    title: str
    content: Optional[str]

class NoteResponse(BaseModel):
    id: int
    title: str
    content: Optional[str]
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

class DeleteResponse(BaseModel):
    message: str

class NoteListResponse(BaseModel):
    total: int
    items: list[NoteResponse]

    class Config:
        from_attributes = True


class ApiErrorPayload(BaseModel):
    code: str
    message: str


class EnvelopeNoteList(BaseModel):
    """Matches app.core.response.success_response(list of notes)."""

    success: bool
    data: List[NoteResponse]
    error: Optional[ApiErrorPayload] = None


class EnvelopeNote(BaseModel):
    """Matches success_response(single note ORM)."""

    success: bool
    data: NoteResponse
    error: Optional[ApiErrorPayload] = None


class EnvelopeDelete(BaseModel):
    """Matches success_response(DeleteResponse)."""

    success: bool
    data: DeleteResponse
    error: Optional[ApiErrorPayload] = None