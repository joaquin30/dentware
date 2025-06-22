from flask import flash, url_for
from flask import render_template, redirect, request, abort
from app.sistema import bp
from app.sistema.forms import PacienteForm, AntMedForm, ExamenesEstomatologicosForm, OdontologoForm
from app.extensions import db
from app.models import Paciente, Historia, HistoriaAntecedentesMedicos, HistoriaExamenesEstomatologicos, Odontologo
from sqlalchemy import select
from app.utils import remove_csrf_token
from flask import jsonify, request

'''
COD-001
Función que muestra la lista de pacientes.
'''
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
    
    cantidad_pacientes = len(pacientes)

    return render_template('sistema/index.html', pacientes=pacientes, cantidad_pacientes=cantidad_pacientes)


'''
COD-002
Función del formulario de registro de datos de paciente.
'''
@bp.route('/registrar', methods=['GET', 'POST'])
def registrar_paciente():
    form = PacienteForm()
    if form.validate_on_submit():
        documento_a_verificar = form.documento_identidad.data
        check = db.session.query(Paciente).filter_by(documento_identidad=documento_a_verificar).first()
        if check:
            flash('Ya existe un paciente registrado con ese documento de identidad.', 'danger')
            return redirect('/registrar')

        paciente = Paciente(**remove_csrf_token(form.data))
        paciente.crear_nueva_historia(db)
        db.session.commit()
        flash('Paciente registrado con éxito', 'success')
        return redirect('/')
    return render_template('sistema/registrar.html', form=form)


'''
COD-003
Función de formulario de edición de datos del paciente.
'''
@bp.route('/paciente/<int:paciente_id>/editar', methods=['GET', 'POST'])
def editar_paciente(paciente_id):
    paciente = db.get_or_404(Paciente, paciente_id)

    if not paciente.historias:
        flash("No hay historia clínica para este paciente.", "danger")
        return redirect(url_for('index'))

    historia = paciente.historias[0]

    form_paciente = PacienteForm(obj=paciente)

    if form_paciente.validate_on_submit():
        form_paciente.populate_obj(paciente)
        db.session.add(paciente)
        db.session.commit()

        flash("Datos personales actualizados.", "success")
        return redirect(url_for('historia.index', historia_id=historia.historia_id))

    return render_template('sistema/editar.html',
                           form_paciente=form_paciente,
                           historia=historia, paciente=paciente)

'''
COD-003
Función de formulario de edición de antecedentes médicos.
'''
@bp.route('/historia/<int:historia_id>/antecedentes', methods=['GET', 'POST'])
def editar_antecedentes(historia_id):
    historia = db.get_or_404(Historia, historia_id)

    # Obtener el primer antecedente o crear uno nuevo si no existe
    antecedente = historia.antecedentes_medicos[0] if historia.antecedentes_medicos else HistoriaAntecedentesMedicos(historia=historia)

    form_antmed = AntMedForm(obj=antecedente)

    if form_antmed.validate_on_submit():
        form_antmed.populate_obj(antecedente)
        if not hasattr(antecedente, 'id') or not getattr(antecedente, 'id', None):
            db.session.add(antecedente)
        db.session.commit()
        flash("Antecedentes médicos actualizados.", "success")
        return redirect(url_for('historia.index', historia_id=historia.historia_id))

    return render_template(
        'historia/editar_antecedentes.html',
        form_antmed=form_antmed,
        historia=historia
    )


'''
COD-004
Función que muestra el formualrio de exámenes clínicos estomatológicos.
'''
@bp.route('/paciente/<int:paciente_id>/examenes-estomatologicos', methods=['GET', 'POST'])
def examenes_estomatologicos(paciente_id):
    paciente = db.get_or_404(Paciente, paciente_id)

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

'''
COD-005
Función que permite mostrar el formulario de búsqueda de pacientes y mostrar las coincidencias de la búsqueda.
'''
@bp.route('/sistema/buscar_pacientes')
def buscar_pacientes():
    q = request.args.get('q', '').strip()
    if not q:
        return jsonify([])

    pacientes = db.session.execute(
        select(Historia.historia_id, Paciente.documento_identidad, Paciente.nombres, Paciente.apellidos)
        .join(Historia.paciente)
        .filter(
            (Paciente.documento_identidad.ilike(f'%{q}%')) |
            (Paciente.nombres.ilike(f'%{q}%')) |
            (Paciente.apellidos.ilike(f'%{q}%'))
        )
        .limit(20)
    ).all()

    resultados = [{
        'historia_id': p.historia_id,
        'documento_identidad': p.documento_identidad,
        'nombres': p.nombres,
        'apellidos': p.apellidos
    } for p in pacientes]

    return jsonify(resultados)

@bp.route('/odontologos')
def odontologos():
    odontologos_internos = db.session.query(Odontologo).filter_by(tipo_odontologo='Interno').all()
    odontologos_externos = db.session.query(Odontologo).filter_by(tipo_odontologo='Externo').all()
    odontologos_temporales = db.session.query(Odontologo).filter_by(tipo_odontologo='Temporal').all()

    return render_template('sistema/odontologo_listado.html',
                           internos=odontologos_internos,
                           externos=odontologos_externos,
                           temporales=odontologos_temporales)

@bp.route('/odontologo/<int:odontologo_id>/editar', methods=['GET', 'POST'])
def editar_odontologo(odontologo_id):
    odontologo = db.get_or_404(Odontologo, odontologo_id)
    form = OdontologoForm(obj=odontologo)

    if form.validate_on_submit():
        form.populate_obj(odontologo)
        db.session.commit()
        flash('Odontólogo actualizado correctamente.', 'success')
        return redirect(url_for('sistema.odontologos'))

    return render_template('sistema/editar_odontologo.html', form=form, odontologo=odontologo)


@bp.route('/odontologo/<int:odontologo_id>/eliminar', methods=['POST'])
def eliminar_odontologo(odontologo_id):
    odontologo = db.get_or_404(Odontologo, odontologo_id)
    db.session.delete(odontologo)
    db.session.commit()
    flash('Odontólogo eliminado correctamente.', 'success')
    return redirect(url_for('sistema.odontologos'))

@bp.route('/odontologos/agregar', methods=['GET', 'POST'])
def agregar_odontologo():
    form = OdontologoForm()
    if form.validate_on_submit():
        nuevo_odontologo = Odontologo(
            odontologo_dni=form.odontologo_dni.data,
            nombre=form.nombre.data,
            tipo_odontologo=form.tipo_odontologo.data
        )
        db.session.add(nuevo_odontologo)
        db.session.commit()
        flash('Odontólogo agregado correctamente', 'success')
        return redirect(url_for('sistema.odontologos'))
    return render_template('sistema/agregar_odontologo.html', form=form)
