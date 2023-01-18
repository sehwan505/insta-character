
from sqlalchemy import Column, TEXT, String, INT, BIGINT, BOOLEAN, TIMESTAMP, ForeignKey, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

# mysql code to alter table with User model

Base = declarative_base()

class User(Base):
    __tablename__ = "user"

    id = Column(BIGINT, nullable=True, autoincrement=True)
    insta_id = Column(String(20), primary_key=True)
    name = Column(TEXT, nullable=True)
    followers_count = Column(INT, nullable=True)
    follows_count = Column(INT, nullable=True)
    biography = Column(TEXT, nullable=True)
    updated_at = Column(DateTime, nullable=False, default=func.utc_timestamp(), onupdate=func.utc_timestamp())
    media = relationship("InstaMedia", back_populates="user")


class InstaMedia(Base):
    __tablename__ = "media"

    id = Column(BIGINT, nullable=False, autoincrement=True, primary_key=True)
    insta_id = Column(String(20), ForeignKey('user.insta_id'))
    comments_count = Column(INT, nullable=True)
    like_count = Column(INT, nullable=True)
    media_url = Column(TEXT, nullable=True)
    caption = Column(TEXT, nullable=True)
    media_type = Column(TEXT, nullable=True)
    media_product_type = Column(TEXT, nullable=True)
    user = relationship("User", back_populates="media")


# create table InstaMedia in mysql