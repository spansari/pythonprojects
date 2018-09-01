from flask import Flask, render_template, Blueprint
from blogs.auth import login_required
from blogs.db_alchemy import ChatHistory, db

bp = Blueprint('chat', __name__)

@bp.route('/chat', methods = ('GET', ))
@login_required
def chat():
    messages = db.session.query(ChatHistory).order_by(db.desc(ChatHistory.id)).all()
    print(messages)
    #messages = ['Message One', 'Message Two']
    return render_template('blog/chat.html', messages=messages)


