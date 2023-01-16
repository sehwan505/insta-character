from typing import Generator

from db.session import session

def get_db() -> Generator:
    db = session
    try:
        yield db
    finally:
        db.close()