from fastapi import APIRouter, Depends, HTTPException
from utils.util import get_token_header
from .api_util import func_get_long_lived_access_token, func_get_page_id, func_get_instagram_business_account
import requests
from .user import save_user, update_user, save_media, UserData
from sqlalchemy.orm import Session
from utils.deps import get_db
from utils.util import config
from db.model import User
from datetime import datetime

router = APIRouter(
    prefix="/insta",
    tags=["insta"],
    # dependencies=[Depends(get_token_header)], #  token header 유무 확인하는 dependencies
    responses={404: {"description": "Not found"}},
)

access_token = config["long_lived_token"]
instagram_account_id = config["account_id"]

@router.get("/generate_token/{token}")
def generate_longlive_token(token):   
    try:
        global access_token
        access_token = func_get_long_lived_access_token(access_token=token)
    except Exception as e:
        print(e)
        raise HTTPException(status_code=500, detail="server error")
    return {"access_token": access_token}

@router.get("/get_instagram_id")
def get_instagram_id():   
    try:
        global instagram_account_id
        page_id = func_get_page_id(access_token)
        instagram_account_id = func_get_instagram_business_account(page_id, access_token)
    except Exception as e:
        print(e)
        raise HTTPException(status_code=500, detail="server error")
    return {"instagram_account_id": instagram_account_id}

@router.get("/{insta_id}")
def get_insta_data(insta_id: str, session: Session = Depends(get_db)):
    try:
        if (existing_user := _get_existing_user(insta_id, session)) is None:
            response = _func_get_business_account_details(insta_id, instagram_account_id, access_token)
            save_user(UserData(insta_id=insta_id, name=response["business_discovery"]['name'], followers_count=response["business_discovery"]['followers_count'], follows_count=response["business_discovery"]['follows_count'], biography=response["business_discovery"]['biography']), session)
            save_media(response["business_discovery"]['media']['data'], insta_id, session)
        elif (datetime.now() - existing_user.updated_at).total_seconds() > 3600:
            response = _func_get_business_account_details(insta_id, instagram_account_id, access_token)
            update_user(UserData(insta_id=insta_id, name=response["business_discovery"]['name'], followers_count=response["business_discovery"]['followers_count'], follows_count=response["business_discovery"]['follows_count'], biography=response["business_discovery"]['biography']), session)
            print(type(existing_user.updated_at))
            save_media(response["business_discovery"]['media']['data'], insta_id, session, existing_user.updated_at)
        else:
            print("already exist")
            return existing_user
    except Exception as e:
        print(e, "error")
        raise HTTPException(status_code=500, detail="server error")
    return {"response": response}

graph_url = 'https://graph.facebook.com/v15.0/'
def _func_get_business_account_details(search_id='',instagram_account_id='', access_token=''):
    url = graph_url + instagram_account_id 
    param = dict()
    param['fields'] = 'business_discovery.username('+search_id + \
        '){followers_count,follows_count,name,biography,username,profile_picture_url,id, media_count,media{comments_count,like_count,media_url,permalink,user_name,caption,timestamp,media_type,media_product_type}}'
    param['access_token'] = access_token
    response = requests.get(url,params=param)
    response = response.json()
    return response

def _get_existing_user(insta_id: str, session: Session) -> User:
    user = session.query(User).filter_by(insta_id=insta_id).order_by(User.id.desc()).first()
    return user

