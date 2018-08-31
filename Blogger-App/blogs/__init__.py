import os

from flask import Flask
from flask_socketio import SocketIO, send
from blogs.db_alchemy import ChatHistory
from flask_sqlalchemy import SQLAlchemy

def create_app(test_config=None):
	app = Flask(__name__, instance_relative_config=True)
	app.config.from_mapping(
		SECRET_KEY='dev',
		DATABASE=os.path.join(app.instance_path, 'blogs.sqlite'),
	)
	app.config['SECRET_KEY'] = 'mysecret'

	if test_config is None:
		app.config.from_pyfile('config.py', silent=True)
	else:
		app.config.from_mapping(test_config)

	try:
		os.makedirs(app.instance_path)
	except OSError:
		pass

	@app.route('/hello')
	def hello_world():
		return 'Hello World!'

	from . import db
	db.init_app(app)

	from . import auth
	app.register_blueprint(auth.bp)

	from . import chat
	app.register_blueprint(chat.bp)

	from . import blog
	app.register_blueprint(blog.bp)
	app.add_url_rule('/', endpoint='index')

	socketio = SocketIO(app)

	db1 = SQLAlchemy(app)

	@socketio.on('message')
	def handleMessage(msg):
		print('Message: '+msg)
		message = ChatHistory(message=msg, username='default')
		db1.session.add(message)
		db1.session.commit()
		send(msg, broadcast=True)
    #
	# if __name__ == '__main__':
	# 	socketio.run(app)

	return app


