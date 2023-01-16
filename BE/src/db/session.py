from sqlalchemy import *
from sqlalchemy.orm import sessionmaker
from utils.util import config

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

engine = engineconn()
session = engine.sessionmaker()