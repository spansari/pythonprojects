from flask import (
    Blueprint, Flask, flash, g, redirect, render_template, request, url_for
)
from werkzeug.exceptions import abort

from blogs.db_alchemy import User, Post, db

from blogs.auth import login_required

bp = Blueprint('blog', __name__)

@bp.route('/')
def index():
    posts = db.session.query(Post).join(User, Post.author_id == User.id).with_entities(Post.id, Post.title, Post.body, Post.created, Post.author_id, User.username).order_by(db.desc(Post.created)).all()
    # posts = db.execute(
    #     'SELECT p.id, title, body, created, author_id, username'
    #     ' FROM post p JOIN user u ON p.author_id = u.id'
    #     ' ORDER BY created DESC'from . import db

    # ).fetchall()
    return render_template('blog/index.html', posts=posts)

@bp.route('/create', methods = ('GET', 'POST'))
@login_required
def create():
    if request.method == 'POST':
        title = request.form['title']
        body = request.form['body']
        error =None

        if not title:
            error = 'Title is required. '

        if error is not None:
            flash(error)
        else:
            print(g.user.id)
            post = Post(title=title, body=body, author_id=g.user.id)
            db.session.add(post)
            db.session.commit()
            # db = get_db()
            # db.execute(
            #     'INSERT INTO post (title, body, author_id)'
            #     ' VALUES (?, ?, ?)',
            #     (title, body, g.user['id'])
            # )
            # db.commit()
            return redirect(url_for('blog.index'))

    return render_template('blog/create.html')

def get_post(id, check_author=True):
    post = db.session.query(Post).join(User, Post.author_id == User.id).filter(Post.id == id).one()
    # post = get_db().execute(
    #     'SELECT p.id, title, body, created, author_id, username'
    #     ' FROM post p JOIN user u ON p.author_id = u.id'
    #     ' WHERE p.id = ?',
    #     (id,)
    # ).fetchone()
    if post is None:
        abort('404', "Post id {} doesn't exist".format(id))

    if check_author and post.author_id != g.user.id:
        abort(403)

    return post

@bp.route('/<int:id>/update', methods=('GET', 'POST'))
@login_required
def update(id):
    post = get_post(id)

    if request.method == 'POST':
        title = request.form['title']
        body = request.form['body']
        error = None

        if not title:
            error = 'Title is required.'

        if error is not None:
            flash(error)
        else:
            post.title = title
            post.body = body
            db.session.merge(post)
            db.session.commit()
            # db = get_db()
            # db.execute(
            #     'UPDATE post SET title = ?, body = ?'
            #     ' WHERE id = ?',
            #     (title, body, id)
            # )
            # db.commit()
            return redirect(url_for('blog.index'))

    return render_template('blog/update.html', post=post)


@bp.route('/<int:id>/delete', methods=('POST',))
@login_required
def delete(id):
    post = get_post(id)
    db.session.delete(post)
    db.session.commit()
    # db = get_db()
    # db.execute('DELETE FROM post WHERE id = ?', (id,))
    # db.commit()
    return redirect(url_for('blog.index'))


@bp.route('/chat', methods = ('GET', ))
@login_required
def chat():
    return render_template('blog/chat.html')
