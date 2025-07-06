from backend.domain.db import MasterSession


def get_master_db():
    db = MasterSession()
    try:
        yield db
    finally:
        db.close()