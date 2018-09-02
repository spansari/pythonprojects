import os

from flask import Flask

def create_app(test_config=None):
	# app = Flask(__name__, instance_relative_config=True)
	app = Flask(__name__)
	if test_config is None:
		print('Loading config')
		app.config.from_pyfile('config.py', silent=True)
	else:
		app.config.from_mapping(test_config)

	# try:
	# 	os.makedirs(app.instance_path)
	# except OSError:
	# 	pass

	@app.route('/hello')
	def hello_world():
		return 'Hello World!'

	from . import auth
	app.register_blueprint(auth.bp)

	from . import chat
	app.register_blueprint(chat.bp)

	from . import blog
	app.register_blueprint(blog.bp)
	app.add_url_rule('/', endpoint='index')

	from blogs.db_model import db, ChatHistory, migrate

	with app.app_context():
		db.init_app(app)
		db.create_all()
		#migrate.init_app(app)

	from flask_socketio import SocketIO, send
	socketio = SocketIO()
	socketio.init_app(app)

	@socketio.on('message')
	def handleMessage(msg):
		print('Message: '+msg)
		message = ChatHistory(message=msg, username='default')
		db.session.add(message)
		db.session.commit()
		send(msg, broadcast=True)
    #
	# if __name__ == '__main__':
	# 	socketio.run(app)

	return app
