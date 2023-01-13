from fastapi import APIRouter, Depends, HTTPException
from db.model import User
from db.database import engineconn

engine = engineconn()
session = engine.sessionmaker()

router = APIRouter(
    prefix="/login",
    tags=["login"],
    responses={404: {"description": "Not found"}},
)

@router.get("/get_db")
def get_db():
    example = session.query(User).all()
    print(example)
    return 0
