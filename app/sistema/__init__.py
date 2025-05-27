from flask import Blueprint

bp = Blueprint('sistema', __name__)

from app.sistema import routes