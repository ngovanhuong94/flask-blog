from flask import Flask
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
    @app.route('/')
    def hello_world():
        return 'Hello world'
    
    # blueprints
    from . import auth

    app.register_blueprint(auth.auth_bp)

    from . import db
    db.init_app(app)

    return app