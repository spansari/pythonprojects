import os

from flask import (Flask, render_template, url_for)
from flask_bootstrap import Bootstrap
from .nav import nav
from .model import db

def create_app(test_config=None):
    app = Flask(__name__)

    if test_config is None:
        print('Loading config')
        app.config.from_pyfile('config.py', silent=True)
    else:
        app.config.from_mapping(test_config)

    from . import auth
    app.register_blueprint(auth.bp)

    from . import blog
    app.register_blueprint(blog.bp)
    app.add_url_rule('/', endpoint='index')

    with app.app_context():
        Bootstrap(app)
        nav.init_app(app)
        db.init_app(app)
        db.create_all()

    @app.route('/hello')
    def hello_world():
        return 'Hello World'

    return app