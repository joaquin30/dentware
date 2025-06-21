from flask import Blueprint

bp = Blueprint('odontograma', __name__)

from app.odontograma import routes