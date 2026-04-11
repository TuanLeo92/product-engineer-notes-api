from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
import os

DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://notes_user:notes_password@db:5432/notes_db")
# Railway / Heroku sometimes provide postgres:// — SQLAlchemy expects postgresql://
if DATABASE_URL.startswith("postgres://"):
    DATABASE_URL = DATABASE_URL.replace("postgres://", "postgresql://", 1)

_connect_args = {}
if DATABASE_URL.startswith("postgresql"):
    _connect_args["connect_timeout"] = 10

engine = (
    create_engine(DATABASE_URL, pool_pre_ping=True, connect_args=_connect_args)
    if _connect_args
    else create_engine(DATABASE_URL, pool_pre_ping=True)
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()   