from flask import Blueprint, render_template, request, g, redirect, url_for

from .auth import login_required
from .db import get_db
blog_bp = Blueprint('blog', __name__, url_prefix='/')


@blog_bp.route('/', methods=['GET'])
def index():
    return render_template('index.html')


@blog_bp.route('/create', methods=['GET', 'POST'])
@login_required
def create():
    db = get_db()
    author_id = g.user['id']
    error = None
    if request.method == 'POST':
        title = request.form['title']
        body = request.form['body']
        if not title:
            error = 'Title is required'
        elif not body:
            error = 'Body is required'

        if error is None:
            db.execute(
                'INSERT INTO post (title, body, author_id) VALUES (?, ?, ?)', (title, body, author_id,)
            )
            db.commit()
            return redirect(url_for('blog.index'))
        flash(error)
    return render_template('create.html')