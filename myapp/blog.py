from flask import (
    Blueprint, Flask, flash, g, redirect, render_template, request, url_for
)
from werkzeug.exceptions import abort

from .model import User, Post, db
from .auth import login_required
from .forms import PostForm
bp = Blueprint('blog', __name__)

@bp.route('/')
def index():
    posts = db.session.query(Post).join(User, Post.author_id == User.id).with_entities(Post.id, Post.title, Post.body, Post.created, Post.author_id, User.username).order_by(db.desc(Post.created)).all()
    return render_template('blog/index.html', posts=posts)

@bp.route('/create', methods = ('GET', 'POST'))
@login_required
def create():
    form = PostForm()
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
            return redirect(url_for('blog.index'))

    return render_template('blog/create.html', form=form)

def get_post(id, check_author=True):
    post = db.session.query(Post).join(User, Post.author_id == User.id).filter(Post.id == id).one()
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
            return redirect(url_for('blog.index'))

    return render_template('blog/update.html', post=post)


@bp.route('/<int:id>/delete', methods=('POST',))
@login_required
def delete(id):
    post = get_post(id)
    db.session.delete(post)
    db.session.commit()
    return redirect(url_for('blog.index'))
