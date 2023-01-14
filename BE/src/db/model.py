
from sqlalchemy import Column, TEXT, INT, BIGINT, BOOLEAN
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class User(Base):
    __tablename__ = "user"

    id = Column(BIGINT, nullable=False, autoincrement=True, primary_key=True)
    insta_id = Column(TEXT, nullable=True)
    is_admin = Column(BOOLEAN, default=0)
    name = Column(TEXT, nullable=True)