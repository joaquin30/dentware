from flask import render_template, abort, redirect, url_for, flash, request, current_app, jsonify
from app.historia import bp
from app.extensions import db
from app.models import Paciente, Historia, HistoriaContraindicacion, Tratamiento, Odontologo, TratamientoSesion
from sqlalchemy import select
import os
from werkzeug.utils import secure_filename
from app.models import HistoriaExamen, PacienteNovedad
from app.historia.forms import HistoriaExamenForm, HistoriaContraindicacionForm, ContraindicacionesForm, NovedadForm, PacienteNovedadesForm, FormularioTratamiento, FormularioTratamientoSesion
from datetime import date
from flask import send_from_directory
from sqlalchemy.orm import joinedload

'''
COD-006
Función que muestra la información de una historia clínica específica.
'''
@bp.route('/<int:historia_id>')
def index(historia_id):
    historia = (
        db.session.query(Historia)
        .options(joinedload(Historia.tratamientos).joinedload(Tratamiento.odontologo))  # carga tratamientos y odontólogo
        .get(historia_id)
    )
    if not historia:
        return abort(404)

    tiene_grave = any(c.es_grave for c in historia.contraindicaciones)

    return render_template(
        'historia/index.html',
        paciente=historia.paciente,
        historia=historia,
        tiene_grave=tiene_grave
    )

'''
COD-007
Función que permite la subida de exámenes auxiliares.
'''
@bp.route('/historia/<int:historia_id>/examenes/subir', methods=['GET', 'POST'])
def subir_examen(historia_id):
    historia = db.get_or_404(Historia, historia_id)
    form = HistoriaExamenForm(historia_id=historia_id)

    if form.validate_on_submit():
        archivo = form.archivo.data
        filename = secure_filename(archivo.filename)
        upload_folder = os.path.join(current_app.root_path, current_app.config['UPLOAD_FOLDER'])
        if not os.path.exists(upload_folder):
            os.makedirs(upload_folder)
        filepath = os.path.join(upload_folder, filename)
        archivo.save(filepath)

        # Generar examen_id incremental para esta historia
        last_examen = db.session.query(HistoriaExamen).filter_by(historia_id=historia_id).order_by(HistoriaExamen.examen_id.desc()).first()
        new_examen_id = 1 if not last_examen else last_examen.examen_id + 1

        nuevo_examen = HistoriaExamen(
            historia_id=historia_id,
            examen_id=new_examen_id,
            titulo=filename,  # Usar el nombre del archivo como título automáticamente
            fecha=date.today(),  # Usar fecha actual
            ruta_archivo=filename
        )
        db.session.add(nuevo_examen)
        db.session.commit()

        flash('Examen subido correctamente', 'success')
        return redirect(url_for('historia.subir_examen', historia_id=historia_id))

    examenes = historia.examenes  # Exámenes ya subidos
    return render_template('examenes_aux/subir_examen.html', form=form, historia=historia, paciente=historia.paciente, examenes=examenes)

'''
COD-008
Función que permite la descarga de exámenes auxiliares.
'''
@bp.route('/historia/<int:historia_id>/examenes/<int:examen_id>/descargar')
def descargar_examen(historia_id, examen_id):
    examen = db.session.get(HistoriaExamen, (historia_id, examen_id))
    if not examen:
        abort(404)
    
    upload_folder = current_app.config.get('UPLOAD_FOLDER', 'static/examenes')
    # En caso que guardes en 'static/examenes', la ruta completa es:
    filepath = os.path.join(upload_folder, examen.ruta_archivo)
    
    # Para descargar
    return send_from_directory(upload_folder, examen.ruta_archivo, as_attachment=True)


'''
COD-009
Función que permite ver los exámenes auxiliares de una resoluación más alta.
'''
@bp.route('/historia/<int:historia_id>/examenes/<int:examen_id>/ver')
def ver_examen(historia_id, examen_id):
    examen = db.get_or_404(HistoriaExamen, {'historia_id': historia_id, 'examen_id': examen_id})
    upload_folder = current_app.config.get('UPLOAD_FOLDER', 'uploads')
    # Para imágenes puedes usar send_from_directory sin as_attachment
    return send_from_directory(upload_folder, examen.ruta_archivo)

'''
COD-010
Función que permite borrar un examen auxiliar.
'''
@bp.route('/historia/<int:historia_id>/examenes/<int:examen_id>/borrar', methods=['POST'])
def borrar_examen(historia_id, examen_id):
    examen = db.get_or_404(HistoriaExamen, (historia_id, examen_id))
    upload_folder = current_app.config.get('UPLOAD_FOLDER', 'static/examenes')
    filepath = os.path.join(upload_folder, examen.ruta_archivo)
    if os.path.exists(filepath):
        os.remove(filepath)
    db.session.delete(examen)
    db.session.commit()

    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        return jsonify({'status': 'ok'})
    flash("Examen eliminado correctamente.", "success")
    return redirect(url_for('historia.index', historia_id=historia_id))

'''
COD-011
Función que permite actualizar la observación de un examen auxiliar.
'''
@bp.route('/historia/<int:historia_id>/examenes/<int:examen_id>/actualizar-observacion', methods=['POST'])
def actualizar_observacion(historia_id, examen_id):
    examen = db.session.query(HistoriaExamen).filter_by(historia_id=historia_id, examen_id=examen_id).first_or_404()
    observacion = request.form.get('observaciones', '')
    examen.observaciones = observacion
    db.session.commit()
    flash('Observaciones actualizadas correctamente.', 'success')
    return redirect(url_for('historia.subir_examen', historia_id=historia_id))


'''
COD-012
Función que permite agregar o editar contraindicaciones de una historia clínica y sugerencias de contraindicaciones frecuentes.
'''
@bp.route('/historia/<int:historia_id>/contraindicaciones', methods=['GET', 'POST'])
def contraindicaciones(historia_id):
    historia = db.session.get(Historia, historia_id)
    if not historia:
        abort(404)

    form = ContraindicacionesForm()
    form.historia_id.data = historia_id

    if request.method == 'GET':
        if not form.contraindicaciones.entries:
            for c in historia.contraindicaciones:
                form.contraindicaciones.append_entry({
                    'descripcion': c.descripcion,
                    'es_grave': c.es_grave
                })

    if form.validate_on_submit():
        # Borrar todas las contraindicaciones
        db.session.query(HistoriaContraindicacion).filter_by(historia_id=historia_id).delete()
        db.session.commit()

        # Insertar las nuevas
        for cform in form.contraindicaciones.entries:
            last_contra = db.session.query(HistoriaContraindicacion) \
                .filter_by(historia_id=historia_id) \
                .order_by(HistoriaContraindicacion.contraindicacion_id.desc()) \
                .first()
            new_id = 1 if not last_contra else last_contra.contraindicacion_id + 1

            nueva = HistoriaContraindicacion(
                historia_id=historia_id,
                contraindicacion_id=new_id,
                descripcion=cform.form.descripcion.data,
                es_grave=cform.form.es_grave.data
            )
            db.session.add(nueva)
        db.session.commit()

        flash("Contraindicaciones guardadas correctamente", "success")
        # Recargar el objeto historia con los datos actualizados
        historia = db.session.get(Historia, historia_id)
        return redirect(url_for('historia.contraindicaciones', historia_id=historia_id))

    sugerencias = [
    "Alergia a AINES", "Alegia a Anestésicos", "Alergia a Penicilina",
    "Alergia a sulfas", "Hipertensión", "Osteoporosis", "Cardiopatía",
    "Diabetes", "Insuficiencia renal", "Insuficiencia hepática",
    "Enfermedad autoimune", "Fiebre reumática", "Asma", "Tiroides",
    "Gastritis", "Úlsera gástrica", "Anemia", "Terapia oncológica",
    "Discrasia sanguínea"
    ]

    return render_template(
        'historia/contraindicaciones.html',
        form=form,
        historia=historia,
        paciente=historia.paciente,
        sugerencias=sugerencias
    )

'''
COD-013
Función que permite agregar o editar novedades de un paciente y asignarles una prioridad.
'''
@bp.route('/paciente/<string:paciente_id>/novedades', methods=['GET', 'POST'])
def paciente_novedades(paciente_id):
    paciente = db.get_or_404(Paciente, paciente_id)
    form = PacienteNovedadesForm()

    if request.method == 'GET':
        # Cargar las novedades actuales en el formulario
        for nov in paciente.novedades:
            form.novedades.append_entry({
                'novedad_id': getattr(nov, 'novedad_id', None),
                'descripcion': nov.descripcion,
                'es_importante': nov.es_importante,
            })

    if form.validate_on_submit():
        # IDs actuales en BD
        ids_actuales = {nov.novedad_id for nov in paciente.novedades}
        # IDs enviados en formulario
        ids_form = set()

        for entry in form.novedades.data:
            nid = entry.get('novedad_id')
            ids_form.add(nid)

            if nid and nid in ids_actuales:
                # Actualizar novedad existente
                nov = db.session.query(PacienteNovedad).filter_by(
                    paciente_id=paciente_id, novedad_id=nid).first()
                if nov:
                    nov.descripcion = entry['descripcion']
                    nov.es_importante = entry.get('es_importante', False)
                    nov.fecha = date.today()
            else:
                # Crear novedad nueva, asignando novedad_id incremental
                last_novedad = (
                    db.session.query(PacienteNovedad)
                    .filter_by(paciente_id=paciente_id)
                    .order_by(PacienteNovedad.novedad_id.desc())
                    .first()
                )
                new_novedad_id = 1 if last_novedad is None else last_novedad.novedad_id + 1

                nueva_novedad = PacienteNovedad(
                    paciente_id=paciente_id,
                    novedad_id=new_novedad_id,
                    descripcion=entry['descripcion'],
                    es_importante=entry.get('es_importante', False),
                    fecha=date.today()
                )
                db.session.add(nueva_novedad)

        # Eliminar novedades borradas (no enviadas en formulario)
        ids_a_eliminar = ids_actuales - ids_form
        if ids_a_eliminar:
            db.session.query(PacienteNovedad).filter(
                PacienteNovedad.paciente_id == paciente_id,
                PacienteNovedad.novedad_id.in_(ids_a_eliminar)
            ).delete(synchronize_session=False)

        db.session.commit()
        flash('Novedades actualizadas correctamente', 'success')
        return redirect(url_for('historia.paciente_novedades', paciente_id=paciente_id))

    return render_template(
        'historia/novedades.html',
        paciente=paciente,
        historia=paciente.historias[0],
        form=form,
    )

'''
COD-014
Función que permite crear un tratamiento para un paciente.
'''
@bp.route('/historia/<int:historia_id>/tratamiento/nuevo', methods=['GET', 'POST'])
def crear_tratamiento(historia_id):
    historia = db.get_or_404(Historia, historia_id)
    paciente = historia.paciente
    form = FormularioTratamiento()

    odontologos = db.session.query(Odontologo).all()
    form.odontologo_id.choices = [(od.odontologo_id, od.nombre) for od in odontologos]

    if form.validate_on_submit():
        nuevo_tratamiento = Tratamiento(
            fecha_creacion=form.fecha.data,
            descripcion=form.descripcion.data,
            en_curso=form.en_curso.data,
            odontologo_id=form.odontologo_id.data,
            historia_id=historia_id
        )
        db.session.add(nuevo_tratamiento)
        db.session.commit()
        flash('Tratamiento creado correctamente.', 'success')
        return redirect(url_for('historia.index', historia_id=historia_id))  # <- corrige aquí también

    return render_template(
        "historia/crearTratamiento.html",
        form=form,
        historia_id=historia_id,
        historia=historia,
        paciente=paciente
    )

@bp.route('/tratamiento/<int:tratamiento_id>', methods=['GET', 'POST'])
def ver_tratamiento(tratamiento_id):
    tratamiento = (
    db.session.query(Tratamiento)
    .options(
        joinedload(Tratamiento.odontologo),
        joinedload(Tratamiento.historia).joinedload(Historia.paciente),
        joinedload(Tratamiento.sesiones).joinedload(TratamientoSesion.odontologo)
    )
    .filter(Tratamiento.tratamiento_id == tratamiento_id)
    .first()
    )

    if not tratamiento:
        abort(404)

    historia = tratamiento.historia
    paciente = historia.paciente

    form = FormularioTratamiento(obj=tratamiento)
    odontologos = db.session.query(Odontologo).all()
    form.odontologo_id.choices = [(od.odontologo_id, od.nombre) for od in odontologos]

    if form.validate_on_submit():
        tratamiento.descripcion = form.descripcion.data
        tratamiento.en_curso = form.en_curso.data
        tratamiento.odontologo_id = form.odontologo_id.data
        tratamiento.fecha_creacion = form.fecha.data

        db.session.commit()
        flash('Tratamiento actualizado correctamente.', 'success')
        return redirect(url_for('historia.ver_tratamiento', tratamiento_id=tratamiento_id))

    return render_template(
        'historia/verTratamiento.html',
        tratamiento=tratamiento,
        historia=historia,
        paciente=paciente,
        form=form
    )


@bp.route('/historia/tratamiento/<int:tratamiento_id>/sesion/nuevo', methods=['GET', 'POST'])
def crear_sesion_tratamiento(tratamiento_id):
    tratamiento = db.get_or_404(Tratamiento, tratamiento_id)
    form = FormularioTratamientoSesion()

    form.tratamiento_id.data = str(tratamiento_id)

    # Cargar odontólogos para el SelectField
    odontologos = db.session.query(Odontologo).all()
    form.odontologo_id.choices = [(str(od.odontologo_id), od.nombre) for od in odontologos]

    if form.validate_on_submit():
        # Calcular nuevo sesion_id incremental para este tratamiento
        last_sesion = (
            db.session.query(TratamientoSesion)
            .filter_by(tratamiento_id=tratamiento_id)
            .order_by(TratamientoSesion.sesion_id.desc())
            .first()
        )
        new_sesion_id = 1 if last_sesion is None else last_sesion.sesion_id + 1

        nueva_sesion = TratamientoSesion(
            tratamiento_id=tratamiento_id,
            sesion_id=new_sesion_id,
            fecha=form.fecha.data,
            descripcion=form.descripcion.data,
            observaciones=form.observaciones.data,
            odontologo_id=form.odontologo_id.data,
        )
        db.session.add(nueva_sesion)
        db.session.commit()
        flash('Sesión creada correctamente.', 'success')
        return redirect(url_for('historia.ver_tratamiento', tratamiento_id=tratamiento_id))
    else:
        print("Errores del formulario:", form.errors)

    historia = tratamiento.historia

    return render_template(
        'historia/crearSesion.html',
        form=form,
        tratamiento=tratamiento,
        paciente=tratamiento.historia.paciente,
        historia=historia
    )

@bp.route('/historia/tratamiento/<int:tratamiento_id>/sesion/<int:sesion_id>')
def ver_sesion_tratamiento(tratamiento_id, sesion_id):
    sesion = (
        db.session.query(TratamientoSesion)
        .filter_by(tratamiento_id=tratamiento_id, sesion_id=sesion_id)
        .join(Odontologo)
        .options(joinedload(TratamientoSesion.odontologo), joinedload(TratamientoSesion.tratamiento))
        .first()
    )

    if not sesion:
        abort(404)

    tratamiento = sesion.tratamiento
    paciente = tratamiento.historia.paciente
    historia = tratamiento.historia

    return render_template(
        'historia/verSesion.html',
        sesion=sesion,
        tratamiento=tratamiento,
        historia=historia,
        paciente=paciente
    )


'''
COD-015
Función que muestra los pagos realizados por un paciente.
'''
@bp.route('/paciente/<string:paciente_id>/pagos', methods=['GET'])
def pagos(paciente_id):
    paciente = db.get_or_404(Paciente, paciente_id)
    historia = paciente.historias[0]
    return render_template('historia/pagos.html', paciente=paciente, historia=historia)