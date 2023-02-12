from fastapi import APIRouter, Depends, HTTPException
from db.model import User, InstaMedia
from db.session import engine
from .gpt import classfy_text
from pydantic import BaseModel, Extra
from typing import List
from sqlalchemy.orm import Session
from utils.deps import get_db
from datetime import datetime


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
    comments_count: int
    like_count: int
    # media_url : str
    caption : str
    media_type : str
    media_product_type : str

    class Config:
        extra = Extra.allow

class UserList(BaseModel):
    __root__: List[UserData]

@router.get("/get_all_user")
def get_all_user(session: Session = Depends(get_db)):
    users = session.query(User).all()
    return {"users": users}

@router.get("/get_media_by_user/{insta_id}")
def get_media_by_user(insta_id: str, session: Session = Depends(get_db)):
    media = session.query(InstaMedia).filter(InstaMedia.insta_id == insta_id).all()
    return {"media": media}

@router.get("/classifcation_by_user/{insta_id}")
def classifications_by_user(insta_id: str, session = Depends(get_db)):
    try:
        media = session.query(InstaMedia).filter(InstaMedia.insta_id == insta_id).all()
        captions = [m.caption for m in media]
        response = classfy_text(captions[0])
    except Exception as e:
        print(e)
        raise HTTPException(status_code=500, detail="server error")
    return {"response": ""}

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
        session.query(User).filter(User.insta_id == user_data.insta_id).update(user_data.dict())
        response = session.commit()
    except Exception as e:
        print(e)
        raise HTTPException(status_code=500, detail="server error")
    return {"response": response}

def save_media(media_list: List[dict], insta_id: str, session: Session, updated_at: datetime = None):
    try:
        if updated_at is not None:
            temp_list = []
            for media in media_list:
                media["insta_id"] = insta_id
                del media["id"]
                if (timestamp := datetime.strptime(media["timestamp"], '%Y-%m-%dT%H:%M:%S+0000')) > updated_at:
                    media["timestamp"] = timestamp
                    temp_list.append(media)
            media_list = temp_list
        else:
            for media in media_list:
                media["insta_id"] = insta_id
                del media["id"]
            
        session.bulk_insert_mappings(InstaMedia, media_list)
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