from fastapi import Depends, HTTPException
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from jose import jwt
from sqlalchemy.orm import Session
from typing import Optional

from app.core.security import ALGORITHM, SECRET_KEY
from app.core.database import SessionLocal
from app.models.user import User

bearer_scheme = HTTPBearer(auto_error=False)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def get_current_user(
    session: Session = Depends(get_db),
    credentials: Optional[HTTPAuthorizationCredentials] = Depends(bearer_scheme),
):
    if credentials is None:
        raise HTTPException(status_code=401, detail="Not authenticated")

    token = credentials.credentials

    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id = payload.get("sub")
    except Exception:
        raise HTTPException(status_code=401, detail="Invalid token")

    if user_id is None:
        raise HTTPException(status_code=401, detail="Invalid token")

    user = session.get(User, user_id)
    if user is None:
        raise HTTPException(status_code=401, detail="User not found")

    return user