from fastapi import Depends, FastAPI
from db.database import engineconn
from db.model import *
from utils.util import get_query_token
from apps import insta, login

# app = FastAPI(dependencies=[Depends(get_query_token)]) # token 유무 확인하는 dependencies
app = FastAPI()

engine = engineconn()
session = engine.sessionmaker()

app.include_router(insta.router)
app.include_router(login.router)