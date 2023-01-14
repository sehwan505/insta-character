from sqlalchemy import *
from sqlalchemy.orm import sessionmaker
from pathlib import Path
import os
import json

BASE_DIR = Path(__file__).resolve().parent.parent
with open(os.path.join(BASE_DIR, "config.json"), "r") as f:
    config = json.load(f)

DB_URL = 'mysql+pymysql://root:root@localhost:3306/insta_character'

class engineconn:
    def __init__(self):
        self.engine = create_engine(DB_URL, pool_recycle = 500)

    def sessionmaker(self):
        Session = sessionmaker(bind=self.engine)
        session = Session()
        return session

    def connection(self):
        conn = self.engine.connect()
        return conn