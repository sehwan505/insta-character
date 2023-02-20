from fastapi import Depends, FastAPI
from fastapi.middleware.cors import CORSMiddleware
from db.model import *
from utils.util import get_query_token
from apps import insta, user

# app = FastAPI(dependencies=[Depends(get_query_token)]) # token 유무 확인하는 dependencies
app = FastAPI()

origins = [
    "https://k-army-project-irpqk.run.goorm.io/",
    "https://insta-character.run.goorm.site/",
    "http://localhost",
    "http://localhost:8000",
    "*"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(insta.router)
app.include_router(user.router)