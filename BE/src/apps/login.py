from fastapi import APIRouter, Depends, HTTPException
from db.model import User
from db.database import engineconn
from pydantic import BaseModel

engine = engineconn()
session = engine.sessionmaker()

router = APIRouter(
    prefix="/login",
    tags=["login"],
    responses={404: {"description": "Not found"}},
)

class UserData(BaseModel):
    insta_id: str
    is_admin: bool
    name: str

@router.get("/get_all_user",  response_model=UserData)
def get_all_user():
    users = session.query(User).all()   
    return {"users": UserData(users)}
    
@router.post("/save_user")
def save_user(user_data: UserData):
    try:
        new_user = User(insta_id=user_data.insta_id, is_admin=user_data.is_admin, name=user_data.name)
        session.add(new_user)
        ret = session.commit()
    except Exception as e:
        raise HTTPException(status_code=500, detail="server error")
    return {"ret": ret}