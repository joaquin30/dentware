from flask import Flask

from config import Config

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    # Initialize Flask extensions here
    from app.extensions import db
    db.init_app(app)

    from app.extensions import bootstrap
    bootstrap.init_app(app)

    # Register blueprints here
    from app.sistema import bp as sistema_bp
    app.register_blueprint(sistema_bp)

    return app