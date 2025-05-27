import os

basedir = os.path.abspath(os.path.dirname(__file__))


class Config:
    SECRET_KEY = os.urandom(20)
    # Si postgres esta disponible, modificar y usar la siguiente URI
    # SQLALCHEMY_DATABASE_URI = 'postgresql+psycopg://user:pass@localhost:5432/dentware'
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'app.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False