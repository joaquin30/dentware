from flask import render_template
from app.sistema import bp
from app.sistema.forms import PacienteForm
from app.extensions import db
from app.models import Paciente, Historia
from sqlalchemy import select

@bp.route('/')
def index():
    pacientes = db.session.execute(
        select(Historia.historia_id, Paciente.nombres, Paciente.apellidos)
        .join(Historia.paciente)
    ).all()
    return render_template('sistema/index.html', pacientes=pacientes)


@bp.route('/registrar', methods=['GET', 'POST'])
def registrar_paciente():
    form = PacienteForm()
    if form.validate_on_submit():
        return "Validado"
    return render_template('sistema/registrar.html', form=form)