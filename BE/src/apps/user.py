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
    is_admin: bool
    name: str

class UserList(BaseModel):
    __root__: List[UserData]

@router.get("/get_all_user",  response_model=UserData)
def get_all_user(session: Session = Depends(get_db)):
    users = session.query(User).all()
    print(users)
    return {"users": UserList(users)}
    
@router.post("/save_user_direct")
def save_user_direct(user_data: UserData, session: Session = Depends(get_db)):
    try:
        new_user = User(insta_id=user_data.insta_id, is_admin=user_data.is_admin, name=user_data.name)
        session.add(new_user)
        response = session.commit()
    except Exception as e:
        print(e)
        raise HTTPException(status_code=500, detail="server error")
    return {"response": response}

def save_user(user_data: UserData, session: Session):
    try:
        new_user = User(insta_id=user_data.insta_id, is_admin=user_data.is_admin, name=user_data.name)
        session.add(new_user)
        response = session.commit()
    except Exception as e:
        print(e)
        raise HTTPException(status_code=500, detail="server error")
    return {"response": response}