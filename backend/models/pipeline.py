import uuid

from sqlmodel import Field
from sqlalchemy import String

from .base_model import BaseModel


class Pipeline(BaseModel, table=True):
    __tablename__ = "pipelines"
    
    name: str = Field(
        sa_type=String(255),
        nullable=False,
    )
    
    user_id: uuid.UUID = Field(
        foreign_key="users.id",
        nullable=False,
    )
    
    