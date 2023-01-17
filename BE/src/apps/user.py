from fastapi import APIRouter, Depends, HTTPException
from db.model import User
from pydantic import BaseModel
from typing import List
from sqlalchemy.orm import Session
from utils.deps import get_db

router = APIRouter(
    prefix="/user",
    tags=["user"],
    responses={404: {"description": "Not found"}},
)

class UserData(BaseModel):
    insta_id: str
    name: str
    followers_count : int
    follows_count : int
    biography : str = ""

class UserList(BaseModel):
    __root__: List[UserData]

@router.get("/get_all_user")
def get_all_user(session: Session = Depends(get_db)):
    users = session.query(User).all()
    return {"users": users}
    
@router.post("/save_user_direct")
def save_user_direct(user_data: UserData, session: Session = Depends(get_db)):
    try:
        new_user = User(insta_id=user_data.insta_id, name=user_data.name, followers_count=user_data.followers_count, follows_count=user_data.follows_count, biography=user_data.biography)
        session.add(new_user)
        response = session.commit()
    except Exception as e:
        print(e)
        raise HTTPException(status_code=500, detail="server error")
    return {"response": response}

def save_user(user_data: UserData, session: Session):
    try:
        new_user = User(insta_id=user_data.insta_id, name=user_data.name, followers_count=user_data.followers_count, follows_count=user_data.follows_count, biography=user_data.biography)
        session.add(new_user)
        response = session.commit()
    except Exception as e:
        print(e)
        raise HTTPException(status_code=500, detail="server error")
    return {"response": response}