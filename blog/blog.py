from flask import Blueprint, render_template

from .auth import login_required
blog_bp = Blueprint('blog', __name__, url_prefix='/')


@blog_bp.route('/', methods=['GET'])
def index():
    return render_template('index.html')


@blog_bp.route('/create', methods=['GET', 'POST'])
@login_required
def create():
    return render_template('create.html')