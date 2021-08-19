from sqlalchemy import Column, Integer, String, Boolean
from sqlalchemy.orm import declarative_base

Base = declarative_base()

# TODO: Add your models below this line!


class User(Base):
	__tablename__ = 'User'
	id = Column(Integer, primary_key=True)
	nickname = Column(String, unique=True)
	password = Column(String)
	bio = Column(String)
	age = Column(Integer)
	profile_picture_link = Column(String)


class Post(Base):
	__tablename__ = 'Post'
	id = Column(Integer, primary_key=True)
	nickname = Column(String)
	content = Column(String)
	image_link = Column(String)
	comments = Column(String)
