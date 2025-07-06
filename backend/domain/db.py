from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from backend.core.config import settings

master_engine = create_engine(str(settings.SQLALCHEMY_DB_URL))
MasterSession = sessionmaker(autocommit=False, autoflush=False, bind=master_engine)