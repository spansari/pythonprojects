import functools
from flask import (Blueprint, flash, g, redirect, render_template, request, session, url_for)
from .forms import RegisterForm, LoginForm
from werkzeug.security import generate_password_hash, check_password_hash
from .model import User, db
from markupsafe import escape

bp = Blueprint('auth', __name__, url_prefix='/auth')

@bp.route('/register', methods=('GET', 'POST'))
def register():
    form = RegisterForm()
    error = None
    # print('hello:'+ form.username.data)
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data

        if db.session.query(User).filter(User.username == username).first() is not None:
            error = 'User {} is already registered'.format(username)

        if error is None:
            user = User(username=username, password=generate_password_hash(password))
            db.session.add(user)
            db.session.commit()
            flash('Hello, {}. You have   successfully signed up'
                  .format(username))
            return redirect(url_for('auth.login'))

        flash(error)
    return render_template('auth/register.html', form=form)

@bp.route('/login',  methods=('GET', 'POST'))
def login():
    form = LoginForm()
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data

        error = None
        user = db.session.query(User).filter(User.username == username).first()

        if user is None:
            error = 'Incorrect username'
        elif not check_password_hash(user.password, password):
            error = 'Incorrect password'

        if error is None:
            session.clear()
            session['user_id'] = user.id
            flash('Hello, {}. You have successfully logged in'.format(username))
            return redirect(url_for('index'))

        flash(error)

    return render_template('auth/login.html', form=form)


def login_required(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None:
            return redirect(url_for('auth.login'))
        return view(**kwargs)
    return wrapped_view


@bp.before_app_request
def load_logged_in_user():
    user_id = session.get('user_id')
    if user_id is None:
        g.user = None
    else:
        g.user = db.session.query(User).filter(User.id == user_id).first()

@bp.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('index'))