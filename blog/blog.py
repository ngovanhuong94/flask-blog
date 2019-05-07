from flask import Blueprint, render_template, request, g, redirect, url_for, abort

from .auth import login_required
from .db import get_db
blog_bp = Blueprint('blog', __name__, url_prefix='/')


@blog_bp.route('/', methods=['GET'])
def index():
    db = get_db()
    posts = db.execute(
        'SELECT * FROM post ORDER BY created DESC'
    ).fetchall()
    return render_template('index.html', posts=posts)


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


def get_post(id, check_author=True):
    db = get_db()

    post = db.execute(
        'SELECT p.id, title, body, created, author_id, username'
        ' FROM post p JOIN user u ON p.author_id=u.id'
        ' WHERE p.id=?', (id,)
    ).fetchone()

    if post is None:
        abort(404)
    
    if check_author and post['author_id'] != g.user['id']:
        abort(403)
    return post


@blog_bp.route('/<int:id>')
def detail(id):
    post = get_post(id, False)
    return render_template('detail.html', post=post)


@blog_bp.route('/<int:id>/edit', methods=['GET', 'POST'])
@login_required
def edit(id):
    post = get_post(id)
    error = None
    if request.method == 'POST':
        title = request.form['title']
        body = request.form['body']
        db = get_db()
        if not title:
            error = 'Title is required'
        elif not body:
            error = 'Body is required'
        
        if error is None:
            db.execute(
                'UPDATE post'
                ' SET title=?, body=?'
                ' WHERE id=?', (title, body, post['id'],)
            )
            db.commit()
            return redirect(url_for('blog.detail', id=post['id']))
        flash(error)
    return render_template('edit.html', post=post)

@blog_bp.route('/<int:id>/delete', methods=['POST'])
@login_required
def delete(id):
    post = get_post(id)
    db = get_db()
    db.execute(
        'DELETE FROM post WHERE id=?', (id,)
    )
    db.commit()
    return redirect(url_for('blog.index'))