import uuid

from pydantic import BaseModel


class UserIn(BaseModel):
    username: str
    password: str
    
    
class UserOut(BaseModel):
    id: uuid.UUID
    username: str
    github_username: str | None = None
    access_token: str