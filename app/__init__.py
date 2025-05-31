from flask import Flask

from config import Config


def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)
    app.config['UPLOAD_FOLDER'] = config_class.UPLOAD_FOLDER

    # Initialize Flask extensions here
    from app.extensions import db
    db.init_app(app)
    from app.gen_fake_data import gen_fake_data
    with app.app_context():
        db.create_all()
        # Descomenta y corre una vez esta funcion
        gen_fake_data()

    from app.extensions import csrf
    csrf.init_app(app)

    from app.extensions import bootstrap
    bootstrap.init_app(app)

    # Register blueprints here
    from app.sistema import bp as sistema_bp
    app.register_blueprint(sistema_bp)

    from app.historia import bp as historia_bp
    app.register_blueprint(historia_bp, url_prefix='/historia')

    return app