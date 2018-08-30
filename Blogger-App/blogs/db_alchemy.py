import os
import sys
from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column, ForeignKey, Integer, String, DateTime, TEXT
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine
from blogs.base import Base

class User(Base):
	__tablename__ = 'User'
	id = Column(Integer, primary_key=True)
	username = Column(TEXT, unique=True, nullable=False)
	password = Column(TEXT, nullable=False)

class Post(Base):
	__tablename__ = 'Post'
	id = Column(Integer, primary_key=True)
	author_id = Column(Integer, ForeignKey('User.id'), nullable=False)
	created = Column(DateTime, nullable=False, default=datetime.now())
	title = Column(TEXT, nullable=False)
	body = Column(TEXT, nullable=False)
	user = relationship(User)

# Create an engine that stores data in the local directory's
# sqlalchemy_example.db file.
engine = create_engine('sqlite:///sqlalchemy_blog.db')

Base.metadata.create_all(engine)


