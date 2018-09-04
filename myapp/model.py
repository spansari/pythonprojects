from flask_sqlalchemy import SQLAlchemy
# from flask_migrate import Migrate

db = SQLAlchemy()
# migrate = Migrate(db)
# Define a base model for other database tables to inherit
class Base(db.Model):
    __abstract__  = True
    id            = db.Column(db.Integer, primary_key=True)
    created  = db.Column(db.DateTime,  default=db.func.current_timestamp())
    modified = db.Column(db.DateTime,  default=db.func.current_timestamp(),
                                           onupdate=db.func.current_timestamp())

class User(Base):
	__tablename__ = 'User'
	username = db.Column(db.String(128), unique=True, nullable=False)
	password = db.Column(db.String(128), nullable=False)
	name = db.Column(db.String(128))
	email = db.Column(db.String(128))

class Post(Base):
	__tablename__ = 'Post'
	author_id = db.Column(db.Integer, db.ForeignKey('User.id'), nullable=False)
	title = db.Column(db.String(500), nullable=False)
	body = db.Column(db.TEXT, nullable=False)
	user = db.relationship(User)

class ChatHistory(Base):
	__tablename__ = 'ChatHistory'
	message = db.Column(db.TEXT)
	username = db.Column(db.String(128), nullable=False)
