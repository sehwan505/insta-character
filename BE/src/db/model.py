
from sqlalchemy import Column, TEXT, INT, BIGINT, BOOLEAN, TIMESTAMP, ForeignKey
from sqlalchemy.ext.declarative import declarative_base

# mysql code to alter table with User model

Base = declarative_base()

class User(Base):
    __tablename__ = "user"

    id = Column(BIGINT, nullable=False, autoincrement=True, primary_key=True)
    insta_id = Column(TEXT, nullable=True)
    name = Column(TEXT, nullable=True)
    followers_count = Column(INT, nullable=True)
    follows_count = Column(INT, nullable=True)
    biography = Column(TEXT, nullable=True)
    updated_at = Column(TIMESTAMP)

