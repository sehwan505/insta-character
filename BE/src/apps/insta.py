from fastapi import APIRouter, Depends, HTTPException

from utils.util import get_token_header
from .api_utils import func_get_long_lived_access_token, func_get_page_id, func_get_instagram_business_account
import requests
import json

router = APIRouter(
    prefix="/insta",
    tags=["insta"],
    # dependencies=[Depends(get_token_header)], #  token header 유무 확인하는 dependencies
    responses={404: {"description": "Not found"}},
)

access_token = ""
instagram_account_id = "3312068002378609"

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
def get_insta_data(insta_id):
    try:
        ret = func_get_business_account_deatils(insta_id, instagram_account_id, access_token)
    except Exception as e:
        print(e)
        raise HTTPException(status_code=500, detail="server error")
    return {"id": insta_id, "ret": ret}

graph_url = 'https://graph.facebook.com/v15.0/'
def func_get_business_account_deatils(search_id='',instagram_account_id='',access_token=''):
    url = graph_url + instagram_account_id 
    param = dict()
    param['fields'] = 'business_discovery.username('+search_id + \
        '){followers_count,follows_count,name,biography,username,profile_picture_url,id, media_count,media{comments_count,like_count,media_url,permalink,user_name,caption,timestamp,media_type,media_product_type}}'
    param['access_token'] = access_token
    response = requests.get(url,params=param)
    response =response.json()
    return response