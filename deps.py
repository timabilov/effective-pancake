

from typing import Generator

from database import SessionLocal

def get_session() -> Generator:
    """Get db session"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
