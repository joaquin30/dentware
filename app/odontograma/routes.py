from flask import render_template, abort, redirect, url_for, flash, request, current_app, jsonify
from app.odontograma import bp
from app.extensions import db
from app.models import Historia, Odontograma
import json
import datetime

@bp.route('/<int:historia_id>/<tipo_odontograma>', methods=['GET', 'POST'])
def index(historia_id, tipo_odontograma):
    # Para traducir entre la url y los nombres verdaderos de los tipos
    slug_tipos = ['inicial', 'tratamiento', 'evolucion']
    tipos = ['Inicial', 'Tratamiento', 'Evolución']
    tipo_odontograma = tipos[slug_tipos.index(tipo_odontograma)]

    historia = db.get_or_404(Historia, historia_id)

    # Si es la primera vez que se entra a un odontograma en un paciente, se crean los tres odontograma
    if len(historia.odontogramas) == 0:
        odontogramas = []
        for tipo in tipos:
            odontogramas.append(Odontograma(tipo_odontograma=tipo, ultima_edicion=datetime.date.today(), historia=historia))
        db.session.add_all(odontogramas)
        db.session.commit()
        db.session.refresh(historia)

    assert len(historia.odontogramas) == 3
    odontograma = db.session.query(Odontograma).filter_by(historia=historia, tipo_odontograma=tipo_odontograma).first()
    assert odontograma is not None

    if request.method == 'POST':
        try:
            data = request.get_json()
            odontograma.hallazgos_clinicos = json.dumps(data['hallazgos_clinicos'], ensure_ascii=False)
            odontograma.especificaciones = data['especificaciones']
            odontograma.observaciones = data['observaciones']
            odontograma.ultima_edicion = datetime.date.today()
            db.session.commit()
            return jsonify({"success": True}), 200
        except Exception as e:
            return jsonify({"success": False, "message": str(e)}), 404

    return render_template('odontograma/index.html', historia=historia, odontograma=odontograma)