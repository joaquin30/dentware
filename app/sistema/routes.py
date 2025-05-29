from flask import flash, url_for
from flask import render_template, redirect, request, abort
from app.sistema import bp
from app.sistema.forms import PacienteForm, AntMedForm, ExamenesEstomatologicosForm
from app.extensions import db
from app.models import Paciente, Historia, HistoriaAntecedentesMedicos, HistoriaExamenesEstomatologicos
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

@bp.route('/paciente/<int:paciente_dni>/editar', methods=['GET', 'POST'])
def editar_paciente(paciente_dni):
    paciente = db.session.get(Paciente, paciente_dni)
    if not paciente:
        abort(404)

    if not paciente.historias:
        flash("No hay historia clínica para este paciente.", "danger")
        return redirect(url_for('index'))
    
    historia = paciente.historias[0]

    # Aquí elegimos el primer antecedente o creamos uno si no existe
    if historia.antecedentes_medicos:
        antecedente = historia.antecedentes_medicos[0]
    else:
        antecedente = HistoriaAntecedentesMedicos(historia=historia)
        historia.antecedentes_medicos.append(antecedente)
    
    form_paciente = PacienteForm(obj=paciente)
    form_antmed = AntMedForm(obj=antecedente)

    if form_paciente.validate_on_submit() and form_antmed.validate_on_submit():
        form_paciente.populate_obj(paciente)
        form_antmed.populate_obj(antecedente)
        print("Antecedentes después de populate_obj:", antecedente.enfermedad_cardiaca, antecedente.vih, antecedente.diabetes, antecedente.alergias, antecedente.otros)
        
        db.session.add(paciente)       # por seguridad
        db.session.add(antecedente)    # por seguridad
        db.session.commit()
        
        flash("Datos personales y antecedentes médicos actualizados correctamente.", "success")
        return redirect(url_for('historia.index', historia_id=historia.historia_id))

    return render_template('sistema/editar.html', 
                           form_paciente=form_paciente, 
                           form_antmed=form_antmed,
                           historia=historia, paciente=historia.paciente)

@bp.route('/paciente/<int:paciente_dni>/examenes-estomatologicos', methods=['GET', 'POST'])
def examenes_estomatologicos(paciente_dni):
    paciente = db.session.get(Paciente, paciente_dni)
    if not paciente:
        abort(404)

    if not paciente.historias:
        flash("No hay historia clínica para este paciente.", "danger")
        return redirect(url_for('index'))

    historia = paciente.historias[0]

    # Buscar o crear el objeto de examen estomatológico
    if historia.examenes_estomatologicos:
        examen = historia.examenes_estomatologicos[0]
    else:
        examen = HistoriaExamenesEstomatologicos(historia=historia)
        historia.examenes_estomatologicos.append(examen)

    form_examen = ExamenesEstomatologicosForm(obj=examen)

    if form_examen.validate_on_submit():
        form_examen.populate_obj(examen)
        db.session.add(examen)
        db.session.commit()
        flash("Exámenes clínicos estomatológicos guardados correctamente.", "success")
        return redirect(url_for('historia.index', historia_id=historia.historia_id))

    return render_template('historia/examenes_estomatologicos.html', form_examen=form_examen, historia=historia, paciente=historia.paciente)