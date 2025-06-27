# Importación de los procedimientos desde un archivo JSON a la base de dato, para tenerlos como datos predefinidos

import json
import os
from app import create_app
from app.extensions import db
from app.models import Procedimiento


def importar_procedimientos_desde_json():
    base_dir = os.path.dirname(__file__)
    path = os.path.join(base_dir, 'procedimientos.json')
    with open(path, 'r', encoding='utf-8') as f:
        procedimientos = json.load(f)
    db.session.query(Procedimiento).delete() #para eliminar la base de datos previa
    db.session.commit()

    nuevos = 0
    for item in procedimientos:
        nombre = item.get('nombre', '').strip()
        raw_costo = item.get('costo_referencial')

        try:
            costo = int(raw_costo) if raw_costo is not None else 0
        except Exception:
            costo = 0

        if not db.session.query(Procedimiento).filter_by(nombre=nombre).first():
            db.session.add(Procedimiento(nombre=nombre, costo_referencial=costo))
            nuevos += 1

    db.session.commit()
    print(f"{nuevos} procedimientos importados.")

if __name__ == '__main__':
    app = create_app()
    with app.app_context():
        importar_procedimientos_desde_json()
