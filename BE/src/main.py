from fastapi import Depends, FastAPI
from db.model import *
from utils.util import get_query_token
from apps import insta, user

# app = FastAPI(dependencies=[Depends(get_query_token)]) # token 유무 확인하는 dependencies
app = FastAPI()

app.include_router(insta.router)
app.include_router(user.router)