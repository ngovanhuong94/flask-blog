from flask import Flask


def create_app():
    app = Flask(__name__)

    @app.route('/')
    def hello_world():
        return 'Hello world'
    
    from . import auth

    app.register_blueprint(auth.auth_bp)

    return app