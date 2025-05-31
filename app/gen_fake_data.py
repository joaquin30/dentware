from faker import Faker
from app.models import (
    Paciente, Historia, HistoriaAntecedentesMedicos,
    HistoriaExamenesEstomatologicos, HistoriaContraindicacion,
    Tratamiento, TratamientoSesion
)
from app.extensions import db
import random

fake = Faker('es.PE')

def gen_fake_data():
    PACIENTES = 10
    estado_civil = ['Soltero', 'Casado', 'Conviviente', 'Viudo', 'Divorciado', 'Separado']
    for i in range(PACIENTES):
        paciente = Paciente(
            documento_identidad=str(random.randrange(100000000, 1000000000)),
            nombres=fake.first_name(),
            apellidos=fake.last_name(),
            fecha_nacimiento=fake.date_of_birth(minimum_age=18, maximum_age=85),
            lugar_nacimiento=fake.city(),
            estado_civil=random.choice(estado_civil),
            direccion=fake.address(),
            telefono=fake.phone_number(),
            email=fake.email(),
            ocupacion=fake.job(),
            lugar_trabajo_estudio=fake.company(),
            apoderado=fake.name() if random.random() < 0.2 else None,
        )
        db.session.add(paciente)
        db.session.commit()

        historia = Historia(paciente=paciente)
        db.session.add(historia)
        db.session.commit()
        
        antecedentes_medicos = HistoriaAntecedentesMedicos(historia=historia)
        db.session.add(antecedentes_medicos)
        db.session.commit()

        examenes_estomatologicos = HistoriaExamenesEstomatologicos(historia=historia)
        db.session.add(examenes_estomatologicos)
        db.session.commit()
     