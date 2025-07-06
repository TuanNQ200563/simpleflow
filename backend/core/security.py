from datetime import datetime, timedelta, timezone

import jwt
from passlib.context import CryptContext

from backend.core.config import settings

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def create_token(subject: str, token_type: str, expire_minutes: int) -> tuple[str, datetime]:
    expiration = datetime.now(timezone.utc) + timedelta(minutes=expire_minutes)
    to_encode = { "exp": expiration, "sub": subject, "token_type": token_type }
    encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
    return encoded_jwt, expiration


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)

