from pydantic import computed_field
from pydantic_settings import BaseSettings

from sqlalchemy.engine import URL


class Settings(BaseSettings):
    DB_HOST: str
    DB_PORT: int
    DB_USER: str
    DB_PASS: str
    DB_NAME: str
    
    @computed_field
    @property
    def SQLALCHEMY_DB_URL(self) -> str:
        return URL(
            drivername="postgresql",
            username=self.DB_USER,
            password=self.DB_PASS,
            host=self.DB_HOST,
            port=self.DB_PORT,
            database=self.DB_NAME,
            query=[]
        ).render_as_string(False)
        
    SECRET_KEY: str
    ALGORITHM: str
    ACCESS_TOKEN_EXPIRE_MINUTES: int
    
    REDIS_HOST: str
    REDIS_PORT: int
    REDIS_DB: int
    
    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
    
    
settings = Settings()