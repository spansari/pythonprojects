# coding=utf-8

from sqlalchemy.pool import SingletonThreadPool
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# engine = create_engine('postgresql://usr:pass@localhost:5432/sqlalchemy')

engine = create_engine('sqlite:///sqlalchemy_blog.db?check_same_thread=False', poolclass=SingletonThreadPool)
Session = sessionmaker(bind=engine)

Base = declarative_base()