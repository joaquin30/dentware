from flask import render_template, abort, redirect, url_for, flash, request, current_app, jsonify
from app.historia import bp
from app.extensions import db
from app.models import Paciente, Historia
from sqlalchemy import select
import os
from werkzeug.utils import secure_filename
from app.models import HistoriaExamen
from app.historia.forms import HistoriaExamenForm
from datetime import date
from flask import send_from_directory


@bp.route('/<int:historia_id>')
def index(historia_id):
    historia = db.session.query(Historia).get(historia_id)
    if not historia:
        return abort(404)
    return render_template('historia/index.html', paciente=historia.paciente, historia=historia)


@bp.route('/historia/<int:historia_id>/examenes/subir', methods=['GET', 'POST'])
def subir_examen(historia_id):
    historia = db.get_or_404(Historia, historia_id)
    form = HistoriaExamenForm(historia_id=historia_id)

    if form.validate_on_submit():
        archivo = form.archivo.data
        filename = secure_filename(archivo.filename)
        upload_folder = current_app.config.get('UPLOAD_FOLDER', 'uploads')
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