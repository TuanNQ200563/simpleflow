import jwt

from fastapi import Depends, Header, status, HTTPException
from jwt.exceptions import InvalidTokenError
from sqlalchemy import select
from sqlalchemy.orm import Session
from typing import Annotated

from backend.core.config import configs
from backend.domain.db import get_master_db
from backend.models.user import User

TOKEN_TYPE = {
    "ACCESS_TOKEN": "ACCESS_TOKEN",
}
ALGORITHM = "HS256"

def require_access_token(
    db: Session = Depends(get_master_db),
    authorization: Annotated[str | None, Header()] = None,
):
    if not authorization:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Authorization header is missing",
            headers={"WWW-Authenticate": "Bearer"},
        )

    token = authorization.replace("Bearer ", "")
    try:
        payload = jwt.decode(
            token, configs.SECRET_KEY, algorithms=[ALGORITHM]
        )
    except (InvalidTokenError):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token",
            headers={"WWW-Authenticate": "Bearer"},
        )

    token_type = payload.get("token_type")
    if token_type != TOKEN_TYPE["ACCESS_TOKEN"]:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token type",
            headers={"WWW-Authenticate": "Bearer"},
        )
        
    user = db.execute(
        select(User).where(User.username == payload.get("sub"))
    ).scalars().first()
    
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found",
            headers={"WWW-Authenticate": "Bearer"},
        )
        
    return user