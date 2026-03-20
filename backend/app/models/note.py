from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from app.core.database import Base
from sqlalchemy.sql import func

class Note(Base):
    __tablename__ = "notes"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    title = Column(String, nullable=False)
    content = Column(String)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    # Ensure updated_at is not NULL on insert (so response validation passes)
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())