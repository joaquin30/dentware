from flask import render_template
from app.sistema import bp
from app.sistema.forms import PacienteForm


@bp.route('/')
def index():
    return 'Buscar paciente'


@bp.route('/crear')
def crear_paciente():
    form = PacienteForm()
    return render_template('sistema/crear.html', form=form)