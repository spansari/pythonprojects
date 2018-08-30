import functools

from blogs.db_alchemy import User, Post, engine
from blogs.base import Session, engine, Base

from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)
from werkzeug.security import check_password_hash, generate_password_hash

from blogs.db import get_db

em = Session()

bp = Blueprint('auth', __name__, url_prefix='/auth')

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
		g.user = em.query(User).filter(User.id == user_id).first()
		# g.user = get_db().execute(
		# 	'SELECT * FROM user WHERE id = ?', (user_id,)
		# ).fetchone()


@bp.route('/register', methods=('GET', 'POST'))
def register():
	
	if request.method == 'POST':
		username = request.form['username']
		password = request.form['password']

		db = get_db()
		error = None

		if not username:
			error = 'Username is required. '
		elif not password:
			error = 'password is required. '
		elif em.query(User).filter(User.username == username).first() is not None:
			error = 'User {0} is already registered. '.format(username)
		# elif db.execute(
		# 	'SELECT id FROM user WHERE username = ?', (username,)
		# ).fetchone() is not None:


		if error is None:
			user = User(username=username, password=generate_password_hash(password))
			em.add(user)
			em.commit()
			#
			# db.execute(
			# 	'INSERT INTO user (username, password) VALUES (?, ?)',
			# 	(username, generate_password_hash(password))
			# )
			# db.commit()
			return redirect(url_for('auth.login'))

		flash(error)

	return render_template('auth/register.html')




@bp.route('/login', methods=('GET', 'POST'))
def login():
	if request.method == 'POST':
		username = request.form['username']
		password = request.form['password']
		db = get_db()

		error = None

		user = em.query(User).filter(User.username == username).first()
		# user = db.execute('SELECT * FROM user WHERE username = ?', (username,)).fetchone()

		if user is None:
			error = 'Incorrect username'
		elif not check_password_hash(user.password, password):
			error = 'Incorrect password'

		if error is None:
			session.clear()
			session['user_id'] = user.id
			return redirect(url_for('index'))

		flash(error)

	return render_template('auth/login.html')


@bp.route('/logout')
def logout():
	session.clear()
	return redirect(url_for('index'))
