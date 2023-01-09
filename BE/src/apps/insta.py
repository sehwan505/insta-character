from fastapi import APIRouter, Depends, HTTPException

from utils.util import get_token_header
import requests
import json

router = APIRouter(
    prefix="/insta",
    tags=["insta"],
    # dependencies=[Depends(get_token_header)], #  token header 유무 확인하는 dependencies
    responses={404: {"description": "Not found"}},
)

fake_items_db = {"abc":{"count": 0, "name": "newjeans"}}

access_token = ""
post_url = f"https://graph.instagram.com/v13.0/515981870361983?fields=username&access_token={access_token}"

@router.get("/{insta_id}")
def get_insta_data(insta_id):
    r = requests.get(post_url)
    ret = r.json()
    fake_items_db[insta_id]["count"] += 1
    return {"id": insta_id, "count": fake_items_db[insta_id]["count"], "ret": ret}

@router.get("/count/{insta_id}")
def get_insta_data(insta_id):
    if insta_id not in fake_items_db:
        raise HTTPException(status_code=404, detail="insta_id not in fake_items_db")
    return {"count": fake_items_db[insta_id]["count"]}

