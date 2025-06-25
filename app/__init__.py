from flask import Flask
from config import Config

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)
    app.config['UPLOAD_FOLDER'] = config_class.UPLOAD_FOLDER

    # Initialize Flask extensions
    from app.extensions import db
    db.init_app(app)

    from app.gen_fake_data import gen_fake_data
    from app.importar_procedimientos import importar_procedimientos_desde_json
    with app.app_context():
        db.create_all()
        # gen_fake_data()  # Uncomment to populate test data
        # importar_procedimientos_desde_json()

    from app.extensions import csrf
    csrf.init_app(app)

    from app.extensions import bootstrap
    bootstrap.init_app(app)

    # Register blueprints
    from app.sistema import bp as sistema_bp
    app.register_blueprint(sistema_bp)

    from app.historia import bp as historia_bp
    app.register_blueprint(historia_bp, url_prefix='/historia')

    from app.odontograma import bp as odontograma_bp
    app.register_blueprint(odontograma_bp, url_prefix='/odontograma')

    return app
