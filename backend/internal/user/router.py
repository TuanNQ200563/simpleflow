from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.orm import Session

from backend.core.config import settings
from backend.core.security import create_token
from backend.models.user import User
from backend.middleware.db import get_master_db

from .schema import UserIn, UserOut


router = APIRouter()


@router.post("/login", response_model=UserOut)
async def login(user: UserIn, db: Session = Depends(get_master_db)):
    try:
        query = select(User).where(
            User.username == user.username,
            User.password == user.password,
        )
        result = db.execute(query).scalars().first()
        if not result:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid username or password"
            )
        return UserOut(
            id=result.id,
            username=result.username,
            github_username=result.github_username,
            access_token=create_token(
                subject=result.username,
                token_type="ACCESS_TOKEN",
                expire_minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES,
            )
        )
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))
    
    
