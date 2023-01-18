from fastapi import APIRouter, Depends, HTTPException
from db.model import User, InstaMedia
from pydantic import BaseModel
from typing import List
from sqlalchemy.orm import Session
from utils.deps import get_db
from db.session import engine

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

class MediaData(BaseModel):
    insta_id: str
    comments_count: int
    like_count: int
    # media_url : str
    caption : str
    media_type : str
    media_product_type : str

class MediaList(BaseModel):
    __root__: List[MediaData]

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


def update_user(user_data: UserData, session: Session):
    try:
        new_inform = User(insta_id=user_data.insta_id, name=user_data.name, followers_count=user_data.followers_count, follows_count=user_data.follows_count, biography=user_data.biography)
        session.query(User).filter_by(insta_id=user_data.insta_id).update(new_inform)
        response = session.commit()
    except Exception as e:
        print(e)
        raise HTTPException(status_code=500, detail="server error")
    return {"response": response}

def save_media(media_list: MediaList, insta_id: str, session: Session):
    try:
        new_media = InstaMedia(insta_id=user_data.insta_id, name=user_data.name, followers_count=user_data.followers_count, follows_count=user_data.follows_count, biography=user_data.biography)
        session.bulk_save_objects(new_media)
        response = session.commit()
    except Exception as e:
        print(e)
        raise HTTPException(status_code=500, detail="server error")
    return {"response": response}


# @router.get("/make_table")
# def make_table():
#     User.__table__.create(bind=engine.engine, checkfirst=True)
#     InstaMedia.__table__.create(bind=engine.engine, checkfirst=True)

#     return 