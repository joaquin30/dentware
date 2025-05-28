from flask import render_template, abort, redirect
from app.historia import bp
from app.extensions import db
from app.models import Paciente, Historia
from sqlalchemy import select

@bp.route('/<int:historia_id>')
def index(historia_id):
    historia = db.get_or_404(Historia, historia_id)
    return render_template('historia/index.html', paciente=historia.paciente)
