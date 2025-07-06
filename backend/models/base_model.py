import uuid

from sqlmodel import SQLModel, Field
from sqlalchemy.dialects.postgresql import UUID as PGUUID


class BaseModel(SQLModel):
    __abstract__ = True
    
    id: uuid.UUID = Field(
        sa_type=PGUUID(as_uuid=True),
        default_factory=uuid.uuid4,
        primary_key=True,
    )