import uuid

from sqlmodel import Field
from sqlalchemy import String
from sqlalchemy.dialects.postgresql import UUID as PGUUID

from .base_model import BaseModel


class User(BaseModel, table=True):
    __tablename__ = "users"
    
    username: str = Field(
        sa_type=String(255),
        unique=True,
        index=True,
        nullable=False,
    )
    
    password: str = Field(
        sa_type=String(255),
        nullable=False,
    )
    
    github_username: str | None = Field(
        sa_type=String(255),
        nullable=True,
    )
    
    github_token: str | None = Field(
        sa_type=String(255),
        nullable=True,
    )