from flask import Flask, render_template
import os


def create_app():
    # create app
    app = Flask(__name__, instance_relative_config=True)

    # config app
    app.config.from_mapping(
        SECRET_KEY='mysecret',
        DATABASE=os.path.join(app.instance_path, 'blog.sqlite')
    )
    # create instance path
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass
    # test router
    @app.route('/hello')
    def hello_world():
        return 'Hello world'
    
    # blueprints
    from . import auth
    from . import blog
    app.register_blueprint(auth.auth_bp)
    app.register_blueprint(blog.blog_bp)
    
    from . import db
    db.init_app(app)

    @app.errorhandler(404)
    def page_not_found(e):
        return render_template('404.html'), 404

    @app.errorhandler(403)
    def forbidden(e):
        return render_template('403.html'), 403
    
    return app