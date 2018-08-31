from flask import Flask, render_template, Blueprint
from flask_sqlalchemy import SQLAlchemy
from blogs.auth import login_required
from blogs.db_alchemy import ChatHistory
app = Flask(__name__)
app.config['SECRET_KEY'] = 'mysecret'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///sqlalchemy_blog.db'

db = SQLAlchemy(app)

bp = Blueprint('chat', __name__)

@bp.route('/chat', methods = ('GET', ))
@login_required
def chat():
    messages = db.session.query(ChatHistory).order_by("created desc").all()
    print(messages)
    #messages = ['Message One', 'Message Two']
    return render_template('blog/chat.html', messages=messages)


