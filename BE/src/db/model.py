
from sqlalchemy import Column, TEXT, INT, BIGINT, BOOLEAN, TIMESTAMP, ForeignKey
from sqlalchemy.ext.declarative import declarative_base

# mysql code to alter table with User model

Base = declarative_base()

class User(Base):
    __tablename__ = "user"

    id = Column(BIGINT, nullable=False, autoincrement=True, primary_key=True)
    insta_id = Column(TEXT, primary_key=True)
    name = Column(TEXT, nullable=True)
    followers_count = Column(INT, nullable=True)
    follows_count = Column(INT, nullable=True)
    biography = Column(TEXT, nullable=True)
    updated_at = Column(TIMESTAMP)


class InstaMedia(Base):
    __tablename__ = "media"

    id = Column(BIGINT, nullable=False, autoincrement=True, primary_key=True)
    insta_id = Column(TEXT, ForeignKey('user.media'))
    comments_count = Column(INT, nullable=True)
    like_count = Column(INT, nullable=True)
    media_url = Column(TEXT, nullable=True)
    caption = Column(TEXT, nullable=True)
    media_type = Column(TEXT, nullable=True)
    media_product_type = Column(TEXT, nullable=True)
    user = relationship("user")

# create table InstaMedia in mysql