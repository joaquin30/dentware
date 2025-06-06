from flask import render_template, abort, redirect, url_for, flash, request, current_app, jsonify
from app.historia import bp
from app.extensions import db
from app.models import Paciente, Historia, HistoriaContraindicacion
from sqlalchemy import select
import os
from werkzeug.utils import secure_filename
from app.models import HistoriaExamen, PacienteNovedad
from app.historia.forms import HistoriaExamenForm, HistoriaContraindicacionForm, ContraindicacionesForm, NovedadForm, PacienteNovedadesForm
from datetime import date
from flask import send_from_directory


@bp.route('/<int:historia_id>')
def index(historia_id):
    historia = db.session.query(Historia).get(historia_id)
    if not historia:
        return abort(404)
    tiene_grave = any(c.es_grave for c in historia.contraindicaciones)
    return render_template('historia/index.html', paciente=historia.paciente, historia=historia, tiene_grave=tiene_grave)


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



@bp.route('/historia/<int:historia_id>/examenes/<int:examen_id>/ver')
def ver_examen(historia_id, examen_id):
    examen = db.get_or_404(HistoriaExamen, {'historia_id': historia_id, 'examen_id': examen_id})
    upload_folder = current_app.config.get('UPLOAD_FOLDER', 'uploads')
    # Para imágenes puedes usar send_from_directory sin as_attachment
    return send_from_directory(upload_folder, examen.ruta_archivo)


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


@bp.route('/historia/<int:historia_id>/examenes/<int:examen_id>/actualizar-observacion', methods=['POST'])
def actualizar_observacion(historia_id, examen_id):
    examen = db.session.query(HistoriaExamen).filter_by(historia_id=historia_id, examen_id=examen_id).first_or_404()
    observacion = request.form.get('observaciones', '')
    examen.observaciones = observacion
    db.session.commit()
    flash('Observaciones actualizadas correctamente.', 'success')
    return redirect(url_for('historia.subir_examen', historia_id=historia_id))



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
                    nov.fecha = datetime.date.today()
            else:
                # Crear novedad nueva
                nueva_novedad = PacienteNovedad(
                    paciente_id=paciente_id,
                    descripcion=entry['descripcion'],
                    es_importante=entry.get('es_importante', False),
                    fecha=datetime.date.today()
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
        return redirect(url_for('sistema.paciente_novedades', paciente_id=paciente_id))

    return render_template(
        'historia/novedades.html',
        paciente=paciente,
        historia=paciente.historias[0],
        form=form,
    )





