DEBUG = True

#Define the application directory
import os
BASE_DIR = os.path.abspath(os.path.dirname(__file__))

#SQLALCHEMY_DATABASE_URI='mysql://sa:password@localhost/app_db'
SQLALCHEMY_DATABASE_URI = 'sqlite:///sqlalchemy_blog.db'

DATABASE_CONNECT_OPTIONS = {}


# Application threads. A common general assumption is
# using 2 per available processor cores - to handle
# incoming requests using one and performing background
# operations using the other.
THREADS_PER_PAGE = 2

SECRET_KEY = 'dev'
