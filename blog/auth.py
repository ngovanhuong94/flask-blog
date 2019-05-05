from flask import Blueprint, render_template, request, flash, redirect, url_for
from .db import get_db
from werkzeug.security import generate_password_hash

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
    return 'Login page'