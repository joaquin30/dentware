from flask import render_template, abort, redirect, url_for, flash, request, current_app, jsonify, session
from app.historia import bp
from app.extensions import db
from app.models import Paciente, Historia, HistoriaContraindicacion, Tratamiento, Odontologo, TratamientoSesion, Procedimiento, Pago
from sqlalchemy import select
import os
from werkzeug.utils import secure_filename
from app.models import HistoriaExamen, PacienteNovedad
from app.historia.forms import HistoriaExamenForm, HistoriaContraindicacionForm, ContraindicacionesForm, NovedadForm, PacienteNovedadesForm, FormularioTratamiento, FormularioTratamientoSesion, PresupuestoForm, LineaPresupuestoForm, FormularioAgregarProcedimiento, FormularioPresupuesto, FormularioPago
from datetime import date
from flask import send_from_directory
from sqlalchemy.orm import joinedload
from datetime import datetime
from math import ceil

'''
F-hist_index
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
F-subir_exam_aux
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
F-descar_exam_aux
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
F-ver_exam_aux
Función que permite ver los exámenes auxiliares de una resoluación más alta.
'''
@bp.route('/historia/<int:historia_id>/examenes/<int:examen_id>/ver')
def ver_examen(historia_id, examen_id):
    examen = db.get_or_404(HistoriaExamen, {'historia_id': historia_id, 'examen_id': examen_id})
    upload_folder = current_app.config.get('UPLOAD_FOLDER', 'uploads')
    # Para imágenes puedes usar send_from_directory sin as_attachment
    return send_from_directory(upload_folder, examen.ruta_archivo)

'''
F-elim_exam_aux
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
F-actua_observaciones
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
F-edit_contraindi
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
F-paciente_novedades
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
F-crear_tratamnt
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
            fecha_creacion=form.fecha_creacion.data,
            descripcion=form.descripcion.data,
            en_curso=True,
            costo=0,  # 👈 valor fijo por defecto
            odontologo_id=form.odontologo_id.data,
            historia_id=historia_id
        )

        db.session.add(nuevo_tratamiento)
        db.session.commit()
        flash('Tratamiento creado correctamente.', 'success')
        return redirect(url_for('historia.index', historia_id=historia_id))

    return render_template(
        "historia/crearTratamiento.html",
        form=form,
        historia_id=historia_id,
        historia=historia,
        paciente=paciente
    )

'''
F-ver_tratamnt
Función que permite ver un tratamiento específico y editarlo.
'''
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
        tratamiento.fecha_creacion = form.fecha_creacion.data

        db.session.commit()
        flash('Tratamiento actualizado correctamente.', 'success')
        return redirect(url_for('historia.index', historia_id=historia.historia_id))


    return render_template(
        'historia/verTratamiento.html',
        tratamiento=tratamiento,
        historia=historia,
        paciente=paciente,
        form=form
    )

'''
F-crear_sesion
Función que permite crear una sesión de tratamiento.
'''
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

'''
F_edit-sesion
Función que permite ver una sesión de tratamiento y editarla.
'''
@bp.route('/historia/tratamiento/<int:tratamiento_id>/sesion/<int:sesion_id>/editar', methods=['GET', 'POST'])
def editar_sesion_tratamiento(tratamiento_id, sesion_id):
    sesion = db.session.query(TratamientoSesion).filter_by(
        tratamiento_id=tratamiento_id, sesion_id=sesion_id).first_or_404()

    tratamiento = sesion.tratamiento
    historia = tratamiento.historia
    paciente = historia.paciente

    form = FormularioTratamientoSesion(obj=sesion)
    form.tratamiento_id.data = str(tratamiento_id)
    form.sesion_id.data = str(sesion_id)

    odontologos = db.session.query(Odontologo).all()
    form.odontologo_id.choices = [(str(od.odontologo_id), od.nombre) for od in odontologos]

    if form.validate_on_submit():
        sesion.fecha = form.fecha.data
        sesion.descripcion = form.descripcion.data
        sesion.observaciones = form.observaciones.data
        sesion.odontologo_id = form.odontologo_id.data

        db.session.commit()
        flash('Sesión actualizada correctamente.', 'success')
        return redirect(url_for('historia.ver_tratamiento', tratamiento_id=tratamiento_id))

    return render_template('historia/verSesion.html',
                           form=form,
                           tratamiento=tratamiento,
                           paciente=paciente,
                           historia=historia)


'''
F-pagos
Función que permite ver los pagos de un paciente y el total de dauda pendiente.
'''
@bp.route('/paciente/<string:paciente_id>/pagos', methods=['GET'])
def pagos(paciente_id):
    paciente = db.get_or_404(Paciente, paciente_id)
    historia = paciente.historias[0]  # Obtener la primera historia del paciente

    # Calcular el presupuesto total sumando los costos de los tratamientos
    total_presupuestos = 0.0
    for tratamiento in historia.tratamientos:
        if tratamiento.costo:
            total_presupuestos += float(tratamiento.costo)

    # Calcular el total de pagos realizados
    total_pagos = sum(pago.monto for pago in paciente.pagos)

    return render_template(
        'historia/pagos.html',
        paciente=paciente,
        historia=historia,
        total_presupuestos=round(total_presupuestos, 2),
        total_pagos=round(total_pagos, 2),
        pagos=paciente.pagos
    )


'''
F-add_pago
Función que permite agregar un pago a un tratamiento específico.
'''
@bp.route('/paciente/<int:paciente_id>/pago', methods=['GET', 'POST'])
def agregar_pago(paciente_id):
    paciente = db.get_or_404(Paciente, paciente_id)
    historia = paciente.historias[0]  # Obtener la primera historia del paciente

    # Calcular el presupuesto total sumando los costos de los tratamientos
    total_presupuestos = 0.0
    for tratamiento in historia.tratamientos:
        if tratamiento.costo:
            total_presupuestos += float(tratamiento.costo)

    # Calcular el total de pagos realizados
    total_pagos = sum(pago.monto for pago in paciente.pagos)
    form = FormularioPago()

    if form.validate_on_submit():
        monto = float(form.monto.data)
        metodo = form.metodo.data
        total_pagos += monto
        if total_pagos > total_presupuestos:
            flash("El monto del pago excede el total del presupuesto.", "danger")
            return redirect(url_for('historia.pagos', paciente_id=paciente_id))

        nuevo_pago = Pago(
            monto=monto,
            metodo=metodo,
            paciente=paciente
        )
        db.session.add(nuevo_pago)
        db.session.commit()

        flash("Pago registrado con éxito.", "success")
        return redirect(url_for('historia.pagos', paciente_id=paciente_id))

    return render_template(
        'historia/agregar_pago.html',
        form=form,
        paciente=paciente
    )

'''
F-presupuesto
Función que permite crear un presupuesto para un tratamiento específico.
'''
@bp.route('/paciente/<int:paciente_id>/tratamiento/<int:tratamiento_id>/presupuesto', methods=['GET', 'POST'])
def presupuesto(paciente_id, tratamiento_id):
    tratamiento = db.get_or_404(Tratamiento, tratamiento_id)
    paciente = db.get_or_404(Paciente, paciente_id)
    form = FormularioPresupuesto()
    descuento_porcentaje = 0
    descuento_aplicado = 0

    if form.validate_on_submit():
        for procedimiento in tratamiento.procedimientos:
            nuevo_costo = request.form.get(f'costo_{procedimiento.procedimiento_id}')
            if nuevo_costo:
                try:
                    procedimiento.costo_referencial = int(nuevo_costo)
                except ValueError:
                    pass

        total_costo = sum(p.costo_referencial or 0 for p in tratamiento.procedimientos)

        # Obtener porcentaje de descuento ingresado (si existe)
        descuento_input = request.form.get("descuento", "0")
        try:
            descuento_porcentaje = int(descuento_input)
        except ValueError:
            descuento_porcentaje = 0

                # Calcular descuento redondeado hacia arriba
        descuento_aplicado = ceil(total_costo * descuento_porcentaje / 100)

        # Guardar el total con descuento y el porcentaje
        tratamiento.costo = total_costo - descuento_aplicado
        tratamiento.descuento_porcentaje = descuento_porcentaje

        db.session.commit()
        flash(f'Se aplicó un descuento del {descuento_porcentaje}% correctamente. Total actualizado: S/ {tratamiento.costo}', 'success')
        return redirect(request.url)

    total_costo = sum(p.costo_referencial or 0 for p in tratamiento.procedimientos)
    descuento_porcentaje = tratamiento.descuento_porcentaje or 0
    descuento_aplicado = ceil(total_costo * descuento_porcentaje / 100)
    total_con_descuento = total_costo - descuento_aplicado

    return render_template('historia/presupuesto.html',
                           tratamiento=tratamiento,
                           paciente=paciente,
                           form=form,
                           total_costo=total_costo,
                           descuento=descuento_porcentaje,
                           total_con_descuento=total_costo - descuento_aplicado
    )


'''
F-gestionar_procedimnts
Función que permite agregar un procedimiento a un procedimiento específico.
'''

@bp.route('/tratamiento/<int:tratamiento_id>/procedimientos', methods=['GET', 'POST'])
def gestionar_procedimientos(tratamiento_id):
    tratamiento = db.get_or_404(Tratamiento, tratamiento_id)
    form = FormularioAgregarProcedimiento()

    # Verificamos si viene un 'delete_id' en el POST (es decir, solicitud para eliminar)
    if request.method == 'POST':
        delete_id = request.form.get('delete_id')
        if delete_id:
            procedimiento = db.get_or_404(Procedimiento, int(delete_id))
            try:
                tratamiento.procedimientos.remove(procedimiento)

                # Recalcular costo total
                tratamiento.costo = sum(p.costo_referencial or 0 for p in tratamiento.procedimientos)

                db.session.commit()
                flash('Procedimiento eliminado correctamente.', 'success')
            except Exception as e:
                db.session.rollback()
                flash(f'Error al eliminar el procedimiento: {e}', 'danger')
            return redirect(url_for('historia.gestionar_procedimientos', tratamiento_id=tratamiento_id))

        # Si no hay delete_id, se asume que es una adición de procedimiento
        if form.validate_on_submit():
            try:
                nombre_proc = form.nombre.data.strip()

                # Buscar si el procedimiento ya existe
                procedimiento = db.session.execute(
                    db.select(Procedimiento).filter_by(nombre=nombre_proc)
                ).scalar_one_or_none()
                if not procedimiento:
                    # Crear nuevo procedimiento con costo_referencial null
                    procedimiento = Procedimiento(nombre=nombre_proc, costo_referencial=0)
                    db.session.add(procedimiento)
                    db.session.flush()  # Obtener ID temporal

                    flash('Nuevo procedimiento registrado.', 'info')

                # Verificar si ya está asociado al tratamiento
                if procedimiento in tratamiento.procedimientos:
                    flash('Este procedimiento ya está asociado al tratamiento.', 'info')
                else:
                    tratamiento.procedimientos.append(procedimiento)
                    tratamiento.costo = sum(p.costo_referencial or 0 for p in tratamiento.procedimientos)
                    db.session.commit()
                    flash('Procedimiento agregado correctamente.', 'success')

            except Exception as e:
                db.session.rollback()
                flash(f'Error al agregar el procedimiento: {e}', 'danger')

            return redirect(url_for('historia.gestionar_procedimientos', tratamiento_id=tratamiento_id))

    # Para autocompletado en el formulario
    procedimientos_disponibles = db.session.query(Procedimiento).all()

    return render_template(
        'historia/gestionar_procedimientos.html',
        tratamiento=tratamiento,
        form=form,
        procedimientos_disponibles=procedimientos_disponibles
    )
