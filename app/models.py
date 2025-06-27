# GENERADO POR: sqlacodegen postgresql+psycopg://user:pass@localhost:5432/dentware > app/models.py

from typing import List

from sqlalchemy import (
    BigInteger, Boolean, Date, Enum,
    ForeignKeyConstraint, Integer, PrimaryKeyConstraint,
    Text, String, Table, Column, ForeignKey
)
from sqlalchemy_utils import (
    EmailType, ScalarListType, PhoneNumberType
)
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
import datetime

class Base(DeclarativeBase):
    pass

'''
CCOdontologo
Entidad odontologo que representa a un profesional odontológico.
''' 
class Odontologo(Base):
    __tablename__ = 'odontologo'
    __table_args__ = (
        PrimaryKeyConstraint('odontologo_id', name='odontologo_pkey'),
    )

    odontologo_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    odontologo_dni: Mapped[str] = mapped_column(String, info={'label': 'Dni'})
    nombre: Mapped[str] = mapped_column(String, info={'label': 'Nombres y Apellidos'})
    tipo_odontologo: Mapped[str] = mapped_column(Enum('Interno', 'Externo', 'Temporal', name='tipo_odontologo_t'), info={'label': 'Tipo de Odontólogo'})

    tratamientos: Mapped[List['Tratamiento']] = relationship('Tratamiento', back_populates='odontologo')
    sesiones: Mapped[List['TratamientoSesion']] = relationship('TratamientoSesion', back_populates='odontologo')

'''
CCPaciente
Entidad paciente que representa a un cliente de la clínica.
'''
class Paciente(Base):
    __tablename__ = 'paciente'
    __table_args__ = (
        PrimaryKeyConstraint('paciente_id', name='paciente_pkey'),
    )

    paciente_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    documento_identidad: Mapped[str] = mapped_column(String, info={'label': 'Documento de Identidad'})
    nombres: Mapped[str] = mapped_column(String, info={'label': 'Nombres'})
    apellidos: Mapped[str] = mapped_column(String, info={'label': 'Apellidos'})
    fecha_nacimiento: Mapped[datetime.date] = mapped_column(Date, info={'label': 'Fecha de Nacimiento'})
    telefono: Mapped[str] = mapped_column(PhoneNumberType, info={'label': 'Teléfono'})
    lugar_nacimiento: Mapped[str] = mapped_column(String, info={'label': 'Lugar de Nacimiento'}, default='')
    estado_civil: Mapped[str] = mapped_column(Enum('Soltero', 'Casado', 'Conviviente', 'Viudo', 'Divorciado', 'Separado', name='estado_civil_t'), default='Soltero', nullable=True, info={'label': 'Estado Civil'})
    direccion: Mapped[str] = mapped_column(String, info={'label': 'Dirección'}, default='')
    email: Mapped[str] = mapped_column(EmailType, info={'label': 'Email'}, default='')
    ocupacion: Mapped[str] = mapped_column(String, info={'label': 'Ocupación'}, default='')
    lugar_trabajo_estudio: Mapped[str] = mapped_column(String, info={'label': 'Lugar de Trabajo o Estudio'}, default='')
    apoderado: Mapped[str] = mapped_column(String, info={'label': 'Apoderado'}, default='')

    novedades: Mapped[List['PacienteNovedad']] = relationship('PacienteNovedad', back_populates='paciente')
    historias: Mapped[List['Historia']] = relationship('Historia', back_populates='paciente')
    pagos: Mapped[List['Pago']] = relationship('Pago', back_populates='paciente')

    def crear_nueva_historia(self, db):
        historia = Historia(paciente=self)
        db.session.add(historia)
        db.session.add(HistoriaAntecedentesMedicos(historia=historia))
        db.session.add(HistoriaExamenesEstomatologicos(historia=historia))

'''
CCPacienteNovedad
Entidad que representa la sección de novedades de un paciente en la historia clínica.
'''
class PacienteNovedad(Base):
    __tablename__ = 'paciente_novedades'
    __table_args__ = (
        ForeignKeyConstraint(['paciente_id'], ['paciente.paciente_id'], name='paciente_novedad_paciente_id_fkey'),
        PrimaryKeyConstraint('paciente_id', 'novedad_id', name='paciente_novedad_pkey'),
    )

    paciente_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    novedad_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    descripcion: Mapped[str] = mapped_column(String)
    fecha: Mapped[datetime.date] = mapped_column(Date, default=datetime.date.today)
    es_importante: Mapped[bool] = mapped_column(Boolean, default=False)

    paciente: Mapped['Paciente'] = relationship('Paciente', back_populates='novedades')

'''
CCHistoria
Entidad que representa la historia clínica de un paciente, guarda relación con las entidades 
HistoriaAntecedentesMedicos, HistoriaExamenesEstomatologicos y Odontograma.
'''
class Historia(Base):
    __tablename__ = 'historia'
    __table_args__ = (
        ForeignKeyConstraint(['paciente_id'], ['paciente.paciente_id'], name='historia_paciente_id_fkey'),
        PrimaryKeyConstraint('historia_id', name='historia_pkey')
    )

    historia_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    fecha_creacion: Mapped[datetime.date] = mapped_column(Date, default=datetime.date.today)
    paciente_id: Mapped[int] = mapped_column(Integer)

    paciente: Mapped['Paciente'] = relationship('Paciente', back_populates='historias')
    contraindicaciones: Mapped[List['HistoriaContraindicacion']] = relationship('HistoriaContraindicacion', back_populates='historia')
    examenes: Mapped[List['HistoriaExamen']] = relationship('HistoriaExamen', back_populates='historia')
    odontogramas: Mapped[List['Odontograma']] = relationship('Odontograma', back_populates='historia')
    tratamientos: Mapped[List['Tratamiento']] = relationship('Tratamiento', back_populates='historia')

'''
CCHistoriaAntecedentes
Entidad que representa los antecedentes médicos de un paciente en su historia clínica.
'''
class HistoriaAntecedentesMedicos(Base):
    __tablename__ = 'historia_antecedentes_medicos'
    __table_args__ = (
        ForeignKeyConstraint(['historia_id'], ['historia.historia_id'], name='historia_antecedentes_medicos_historia_id_fkey'),
        PrimaryKeyConstraint('historia_id', name='historia_antecedentes_medicos_pkey')
    )

    historia_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    enfermedad_cardiaca: Mapped[bool] = mapped_column(Boolean, default=False, info={'label': 'Enfermedad cardíaca'})
    enfermedad_renal: Mapped[bool] = mapped_column(Boolean, default=False, info={'label': 'Enfermedad renal'})
    vih: Mapped[bool] = mapped_column(Boolean, default=False, info={'label': 'VIH'})
    alergias: Mapped[bool] = mapped_column(Boolean, default=False, info={'label': 'Alergias'})
    hemorragias: Mapped[bool] = mapped_column(Boolean, default=False, info={'label': 'Hemorragias'})
    medicado: Mapped[bool] = mapped_column(Boolean, default=False, info={'label': 'Medicado'})
    diabetes: Mapped[bool] = mapped_column(Boolean, default=False, info={'label': 'Diabetes'})
    hepatitis: Mapped[bool] = mapped_column(Boolean, default=False, info={'label': 'Hepatitis'})
    problemas_hemorragicos: Mapped[bool] = mapped_column(Boolean, default=False, info={'label': 'Problemas hemorrágicos'})
    presion_alta: Mapped[bool] = mapped_column(Boolean, default=False, info={'label': 'Presión alta'})
    epilepsia: Mapped[bool] = mapped_column(Boolean, default=False, info={'label': 'Epilepsia'})
    embarazo: Mapped[bool] = mapped_column(Boolean, default=False, info={'label': 'Embarazo'})
    otros: Mapped[str] = mapped_column(Text, default='')

    historia: Mapped['Historia'] = relationship('Historia', backref='antecedentes_medicos')

'''
CCHistContraindicacion
Entidad que representa las contraindicaciones médicas de un paciente en su historia clínica.
'''
class HistoriaContraindicacion(Base):
    __tablename__ = 'historia_contraindicacion'
    __table_args__ = (
        ForeignKeyConstraint(['historia_id'], ['historia.historia_id'], name='historia_contraindicacion_historia_id_fkey'),
        PrimaryKeyConstraint('historia_id', 'contraindicacion_id', name='historia_contraindicacion_pkey')
    )

    historia_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    contraindicacion_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    descripcion: Mapped[str] = mapped_column(String)
    es_grave: Mapped[bool] = mapped_column(Boolean)

    historia: Mapped['Historia'] = relationship('Historia', back_populates='contraindicaciones')

'''
CCHistExamen
Entidad que representa los exámenes auxiliares realizados a un paciente en su historia clínica.
'''
class HistoriaExamen(Base):
    __tablename__ = 'historia_examen'
    __table_args__ = (
        ForeignKeyConstraint(['historia_id'], ['historia.historia_id'], name='historia_examen_historia_id_fkey'),
        PrimaryKeyConstraint('historia_id', 'examen_id', name='historia_examen_pkey')
    )

    historia_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    examen_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    titulo: Mapped[str] = mapped_column(String)
    fecha: Mapped[datetime.date] = mapped_column(Date, default=datetime.date.today)
    ruta_archivo: Mapped[str] = mapped_column(String)
    observaciones: Mapped[str] = mapped_column(Text, default='')

    historia: Mapped['Historia'] = relationship('Historia', back_populates='examenes')

'''
CCHistEstomatologicos
Entidad que representa los exámenes estomatológicos realizados a un paciente en su historia clínica.
'''
class HistoriaExamenesEstomatologicos(Base):
    __tablename__ = 'historia_examenes_estomatologicos'
    __table_args__ = (
        ForeignKeyConstraint(['historia_id'], ['historia.historia_id'], name='historia_examenes_estomatologicos_historia_id_fkey'),
        PrimaryKeyConstraint('historia_id', name='historia_examenes_estomatologicos_pkey')
    )

    historia_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    maxilares: Mapped[bool] = mapped_column(Boolean, default=False)
    maxilares_descripcion: Mapped[str] = mapped_column(String, default='')
    vestibulo: Mapped[bool] = mapped_column(Boolean, default=False)
    vestibulo_descripcion: Mapped[str] = mapped_column(String, default='')
    labios: Mapped[bool] = mapped_column(Boolean, default=False)
    labios_descripcion: Mapped[str] = mapped_column(String, default='')
    encia: Mapped[bool] = mapped_column(Boolean, default=False)
    encia_descripcion: Mapped[str] = mapped_column(String, default='')
    paladar: Mapped[bool] = mapped_column(Boolean, default=False)
    paladar_descripcion: Mapped[str] = mapped_column(String, default='')
    oclusión: Mapped[bool] = mapped_column(Boolean, default=False)
    oclusión_descripcion: Mapped[str] = mapped_column(String, default='')
    lengua: Mapped[bool] = mapped_column(Boolean, default=False)
    lengua_descripcion: Mapped[str] = mapped_column(String, default='')
    atm: Mapped[bool] = mapped_column(Boolean, default=False)
    atm_descripcion: Mapped[str] = mapped_column(String, default='')
    piso_de_boca: Mapped[bool] = mapped_column(Boolean, default=False)
    piso_de_boca_descripcion: Mapped[str] = mapped_column(String, default='')
    ganglios: Mapped[bool] = mapped_column(Boolean, default=False)
    ganglios_descripcion: Mapped[str] = mapped_column(String, default='')
    orifaringe: Mapped[bool] = mapped_column(Boolean, default=False)
    orifaringe_descripcion: Mapped[str] = mapped_column(String, default='')
    halitosis: Mapped[bool] = mapped_column(Boolean, default=False)
    halitosis_descripcion: Mapped[str] = mapped_column(String, default='')


    historia: Mapped['Historia'] = relationship('Historia', backref='examenes_estomatologicos')

'''
CCOdontograma
Entidad que representa el odontograma (inicial, tratamiento, evolución) de un paciente, guarda relación con la entidad Historia.
'''
class Odontograma(Base):
    __tablename__ = 'odontograma'
    __table_args__ = (
        ForeignKeyConstraint(['historia_id'], ['historia.historia_id'], name='odontograma_historia_id_fkey'),
        PrimaryKeyConstraint('odontograma_id', name='odontograma_pkey')
    )

    odontograma_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    historia_id: Mapped[int] = mapped_column(Integer)
    tipo_odontograma: Mapped[str] = mapped_column(Enum('Inicial', 'Tratamiento', 'Evolución', name='tipo_odontograma_t'))
    ultima_edicion: Mapped[datetime.date] = mapped_column(Date)
    especificaciones: Mapped[str] = mapped_column(Text, default='')
    observaciones: Mapped[str] = mapped_column(Text, default='')
    hallazgos_clinicos: Mapped[str] = mapped_column(Text, default='[]')

    historia: Mapped['Historia'] = relationship('Historia', back_populates='odontogramas')

tratamiento_procedimiento = Table(
    'tratamiento_procedimiento',
    Base.metadata,
    Column('tratamiento_id', ForeignKey('tratamiento.tratamiento_id')),
    Column('procedimiento_id', ForeignKey('procedimiento.procedimiento_id'))
)

'''
CCTratamiento
Entidad que representa un tratamiento odontológico realizado a un paciente, guarda relación con las entidades Historia, Odontologo, 
Procedimiento y TratamientoSesion.
'''
class Tratamiento(Base):
    __tablename__ = 'tratamiento'
    __table_args__ = (
        ForeignKeyConstraint(['historia_id'], ['historia.historia_id'], name='tratamiento_historia_id_fkey'),
        ForeignKeyConstraint(['odontologo_id'], ['odontologo.odontologo_id'], name='tratamiento_odontologo_id_fkey'),
        PrimaryKeyConstraint('tratamiento_id', name='tratamiento_pkey')
    )

    tratamiento_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    fecha_creacion: Mapped[datetime.date] = mapped_column(Date, default=datetime.date.today)
    descripcion: Mapped[str] = mapped_column(String, info={'label': 'Descripción de tratamientos'})
    en_curso: Mapped[bool] = mapped_column(Boolean)
    costo: Mapped[int] = mapped_column(BigInteger)
    descuento_porcentaje: Mapped[int] = mapped_column(Integer, default=0)

    odontologo_id: Mapped[str] = mapped_column(String)
    historia_id: Mapped[int] = mapped_column(Integer)

    historia: Mapped['Historia'] = relationship('Historia', back_populates='tratamientos')
    odontologo: Mapped['Odontologo'] = relationship('Odontologo', back_populates='tratamientos')
    sesiones: Mapped[List['TratamientoSesion']] = relationship('TratamientoSesion', back_populates='tratamiento')
    procedimientos: Mapped[List['Procedimiento']] = relationship(secondary=tratamiento_procedimiento)

'''
CCProcedimiento
Entidad que representa un procedimiento odontológico realizado a un paciente, 
guarda relación con las entidades Historia, Odontologo y Tratamiento.
'''
class Procedimiento(Base):
    __tablename__ = 'procedimiento'
    __table_args__ = (
        PrimaryKeyConstraint('procedimiento_id', name='procedimiento_pkey'),
    )

    procedimiento_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    nombre: Mapped[str] = mapped_column(String)
    costo_referencial: Mapped[int] = mapped_column(BigInteger)

'''
CCPago
Entidad que representa un pago realizado por un paciente.
'''
class Pago(Base):
    __tablename__ = 'pago'
    __table_args__ = (
        ForeignKeyConstraint(['paciente_id'], ['paciente.paciente_id'], name='pago_paciente_id_fkey'),
        PrimaryKeyConstraint('pago_id', name='pago_pkey')
    )

    pago_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    metodo: Mapped[str] = mapped_column(Enum('Efectivo', 'Tarjeta', 'Transferencia', 'Yape', 'Plin', 'Otros', name='metodo_pago_t'))
    monto: Mapped[int] = mapped_column(BigInteger)
    fecha: Mapped[datetime.date] = mapped_column(Date, default=datetime.date.today)
    paciente_id: Mapped[int] = mapped_column(Integer)

    paciente: Mapped['Paciente'] = relationship('Paciente', back_populates='pagos')

'''
CCTratSesion
Entidad que representa una sesión de tratamiento odontológico de un paciente.
'''
class TratamientoSesion(Base):
    __tablename__ = 'tratamiento_sesion'
    __table_args__ = (
        ForeignKeyConstraint(['odontologo_id'], ['odontologo.odontologo_id'], name='tratamiento_sesion_odontologo_id_fkey'),
        ForeignKeyConstraint(['tratamiento_id'], ['tratamiento.tratamiento_id'], name='tratamiento_sesion_tratamiento_id_fkey'),
        PrimaryKeyConstraint('tratamiento_id', 'sesion_id', name='tratamiento_sesion_pkey')
    )

    tratamiento_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    sesion_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    fecha: Mapped[datetime.date] = mapped_column(Date, default=datetime.date.today)
    descripcion: Mapped[str] = mapped_column(String)
    observaciones: Mapped[str] = mapped_column(Text)
    odontologo_id: Mapped[str] = mapped_column(String)

    odontologo: Mapped['Odontologo'] = relationship('Odontologo', back_populates='sesiones')
    tratamiento: Mapped['Tratamiento'] = relationship('Tratamiento', back_populates='sesiones')
