from fastapi import Header, HTTPException
from pathlib import Path
import os
import json

BASE_DIR = Path(__file__).resolve().parent.parent
with open(os.path.join(BASE_DIR, "config.json"), "r") as f:
    config = json.load(f)

async def get_token_header(x_token: str = Header(...)):
    if x_token != "fake-super-secret-token":
        raise HTTPException(status_code=400, detail="X-Token header invalid")


async def get_query_token(token: str):
    if token != "barney":
        raise HTTPException(status_code=400, detail="No Barney token provided")