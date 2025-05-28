from flask import render_template, redirect, request, abort
from app.sistema import bp
from app.sistema.forms import PacienteForm
from app.extensions import db
from app.models import Paciente, Historia
from sqlalchemy import select
from app.utils import remove_csrf_token

@bp.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        historia_id = request.form.get('historia_id')
        if not historia_id:
            return abort(404)
        return redirect(f'/historia/{historia_id}')
    pacientes = db.session.execute(
        select(Historia.historia_id, Paciente.nombres, Paciente.apellidos)
        .join(Historia.paciente).order_by(Paciente.nombres, Paciente.apellidos)
    ).all()
    return render_template('sistema/index.html', pacientes=pacientes)


@bp.route('/registrar', methods=['GET', 'POST'])
def registrar_paciente():
    form = PacienteForm()
    if form.validate_on_submit():
        paciente = Paciente(**remove_csrf_token(form.data))
        paciente.crear_nueva_historia(db)
        db.session.commit() 
        return redirect('/')
    return render_template('sistema/registrar.html', form=form)