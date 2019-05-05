from flask import Blueprint, render_template, request, flash, redirect, url_for, session
from .db import get_db
from werkzeug.security import generate_password_hash, check_password_hash

auth_bp = Blueprint('auth', __name__, url_prefix='/auth')

@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    db = get_db()
    error = None
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        password2 = request.form['password2']   
        if not username:
            error = 'Username is required'
        elif not password:
            error = 'Password is required'
        elif not password2:
            error = 'Confirm password is required'
        elif password != password2:
            error = 'Passwords must matchs'
        elif db.execute(
            'SELECT id FROM user WHERE username = ?', (username,)
        ).fetchone() is not None:
            error = 'Username was used'
        
        if error is None:
            db.execute(
                'INSERT INTO user (username, password) VALUES (?, ?)',
                (username, generate_password_hash(password),)
            )
            db.commit()
            return redirect(url_for('auth.login'))
        flash(error)

    return render_template('register.html')

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    db = get_db()
    error = None
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        # validation
        if not username:
            error = 'Username is required'
        elif not password:
            error = 'Password is required'
        # fetch user by username
        user = db.execute(
            'SELECT id, username, password FROM user WHERE username=?', (username,)
        ).fetchone()

        if user is None:
            error = 'Username not found'
        # check password
        elif not check_password_hash(user['password'], password):
            error = 'Password incorrect'
        
        
        if error is None:
            #save user id to session
            session.clear()
            session['user_id'] = user['id']
            return redirect(url_for('hello_world'))
        # show error to client
        flash(error)
    return render_template('login.html')