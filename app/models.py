# GENERADO POR: sqlacodegen postgresql+psycopg://user:pass@localhost:5432/dentware > app/models.py

from typing import List

from sqlalchemy import (
    BigInteger, Boolean, Date, Enum,
    ForeignKeyConstraint, Integer, PrimaryKeyConstraint,
    Text, String
)
from sqlalchemy_utils import (
    EmailType, ScalarListType, PhoneNumberType
)
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
import datetime

class Base(DeclarativeBase):
    pass


class Material(Base):
    __tablename__ = 'material'
    __table_args__ = (
        PrimaryKeyConstraint('material_id', name='material_pkey'),
    )

    material_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    nombre: Mapped[str] = mapped_column(String)
    costo_referencial: Mapped[int] = mapped_column(BigInteger)

    tratamientos: Mapped[List['TratamientoMaterial']] = relationship('TratamientoMaterial', back_populates='material')


class Odontologo(Base):
    __tablename__ = 'odontologo'
    __table_args__ = (
        PrimaryKeyConstraint('odontologo_id', name='odontologo_pkey'),
    )

    odontologo_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    odontologo_dni: Mapped[str] = mapped_column(String)
    nombre: Mapped[str] = mapped_column(String)
    tipo_odontologo: Mapped[str] = mapped_column(Enum('Interno', 'Externo', 'Temporal', name='tipo_odontologo_t'))

    tratamientos: Mapped[List['Tratamiento']] = relationship('Tratamiento', back_populates='odontologo')
    sesiones: Mapped[List['TratamientoSesion']] = relationship('TratamientoSesion', back_populates='odontologo')


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

    def crear_nueva_historia(self, db):
        historia = Historia(paciente=self)
        db.session.add(historia)
        db.session.add(HistoriaAntecedentesMedicos(historia=historia))
        db.session.add(HistoriaExamenesEstomatologicos(historia=historia))


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


class Procedimiento(Base):
    __tablename__ = 'procedimiento'
    __table_args__ = (
        PrimaryKeyConstraint('procedimiento_id', name='procedimiento_pkey'),
    )

    procedimiento_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    nombre: Mapped[str] = mapped_column(String)
    costo_referencial: Mapped[int] = mapped_column(BigInteger)

    tratamientos: Mapped[List['TratamientoProcedimiento']] = relationship('TratamientoProcedimiento', back_populates='procedimiento')


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


class HistoriaExamenesEstomatologicos(Base):
    __tablename__ = 'historia_examenes_estomatologicos'
    __table_args__ = (
        ForeignKeyConstraint(['historia_id'], ['historia.historia_id'], name='historia_examenes_estomatologicos_historia_id_fkey'),
        PrimaryKeyConstraint('historia_id', name='historia_examenes_estomatologicos_pkey')
    )

    historia_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    maxilares: Mapped[bool] = mapped_column(Boolean, default=False)
    vestíbulo: Mapped[bool] = mapped_column(Boolean, default=False)
    labios: Mapped[bool] = mapped_column(Boolean, default=False)
    encia: Mapped[bool] = mapped_column(Boolean, default=False)
    paladar: Mapped[bool] = mapped_column(Boolean, default=False)
    oclusión: Mapped[bool] = mapped_column(Boolean, default=False)
    lengua: Mapped[bool] = mapped_column(Boolean, default=False)
    atm: Mapped[bool] = mapped_column(Boolean, default=False)
    piso_de_boca: Mapped[bool] = mapped_column(Boolean, default=False)
    ganglios: Mapped[bool] = mapped_column(Boolean, default=False)
    orifaringe: Mapped[bool] = mapped_column(Boolean, default=False)
    halitosis: Mapped[bool] = mapped_column(Boolean, default=False)

    historia: Mapped['Historia'] = relationship('Historia', backref='examenes_estomatologicos')


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
    especificaciones: Mapped[str] = mapped_column(Text)
    observaciones: Mapped[str] = mapped_column(Text)

    historia: Mapped['Historia'] = relationship('Historia', back_populates='odontogramas')
    entradas_areas_diente: Mapped[List['OdontogramaEntradaAreasDiente']] = relationship('OdontogramaEntradaAreasDiente', back_populates='odontograma')
    entradas_bordes_diente: Mapped[List['OdontogramaEntradaBordesDiente']] = relationship('OdontogramaEntradaBordesDiente', back_populates='odontograma')
    entradas_diente: Mapped[List['OdontogramaEntradaDiente']] = relationship('OdontogramaEntradaDiente', back_populates='odontograma')
    entradas_par_dientes: Mapped[List['OdontogramaEntradaParDientes']] = relationship('OdontogramaEntradaParDientes', back_populates='odontograma')
    entradas_rango_dientes: Mapped[List['OdontogramaEntradaRangoDientes']] = relationship('OdontogramaEntradaRangoDientes', back_populates='odontograma')


class Tratamiento(Base):
    __tablename__ = 'tratamiento'
    __table_args__ = (
        ForeignKeyConstraint(['historia_id'], ['historia.historia_id'], name='tratamiento_historia_id_fkey'),
        ForeignKeyConstraint(['odontologo_id'], ['odontologo.odontologo_id'], name='tratamiento_odontologo_id_fkey'),
        PrimaryKeyConstraint('tratamiento_id', name='tratamiento_pkey')
    )

    tratamiento_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    fecha_creacion: Mapped[datetime.date] = mapped_column(Date, default=datetime.date.today)
    descripcion: Mapped[str] = mapped_column(String)
    en_curso: Mapped[bool] = mapped_column(Boolean)
    odontologo_id: Mapped[str] = mapped_column(String)
    historia_id: Mapped[int] = mapped_column(Integer)

    historia: Mapped['Historia'] = relationship('Historia', back_populates='tratamientos')
    odontologo: Mapped['Odontologo'] = relationship('Odontologo', back_populates='tratamientos')
    materiales: Mapped[List['TratamientoMaterial']] = relationship('TratamientoMaterial', back_populates='tratamiento')
    pagos: Mapped[List['TratamientoPago']] = relationship('TratamientoPago', back_populates='tratamiento')
    procedimientos: Mapped[List['TratamientoProcedimiento']] = relationship('TratamientoProcedimiento', back_populates='tratamiento')
    sesiones: Mapped[List['TratamientoSesion']] = relationship('TratamientoSesion', back_populates='tratamiento')


class OdontogramaEntradaAreasDiente(Base):
    __tablename__ = 'odontograma_entrada_areas_diente'
    __table_args__ = (
        ForeignKeyConstraint(['odontograma_id'], ['odontograma.odontograma_id'], name='odontograma_entrada_areas_diente_odontograma_id_fkey'),
        PrimaryKeyConstraint('odontograma_id', 'id', name='odontograma_entrada_areas_diente_pkey')
    )

    odontograma_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    diente: Mapped[int] = mapped_column(Integer)
    tipo_entrada: Mapped[str] = mapped_column(String)
    areas: Mapped[list[int]] = mapped_column(ScalarListType) # Esto era array
    es_grave: Mapped[bool] = mapped_column(Boolean)

    odontograma: Mapped['Odontograma'] = relationship('Odontograma', back_populates='entradas_areas_diente')


class OdontogramaEntradaBordesDiente(Base):
    __tablename__ = 'odontograma_entrada_bordes_diente'
    __table_args__ = (
        ForeignKeyConstraint(['odontograma_id'], ['odontograma.odontograma_id'], name='odontograma_entrada_bordes_diente_odontograma_id_fkey'),
        PrimaryKeyConstraint('odontograma_id', 'id', name='odontograma_entrada_bordes_diente_pkey')
    )

    odontograma_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    diente: Mapped[int] = mapped_column(Integer)
    tipo_entrada: Mapped[str] = mapped_column(String)
    bordes: Mapped[list[int]] = mapped_column(ScalarListType) # Esto era array
    es_grave: Mapped[bool] = mapped_column(Boolean)

    odontograma: Mapped['Odontograma'] = relationship('Odontograma', back_populates='entradas_bordes_diente')


class OdontogramaEntradaDiente(Base):
    __tablename__ = 'odontograma_entrada_diente'
    __table_args__ = (
        ForeignKeyConstraint(['odontograma_id'], ['odontograma.odontograma_id'], name='odontograma_entrada_diente_odontograma_id_fkey'),
        PrimaryKeyConstraint('odontograma_id', 'id', name='odontograma_entrada_diente_pkey')
    )

    odontograma_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    diente: Mapped[int] = mapped_column(Integer)
    tipo_entrada: Mapped[str] = mapped_column(String)
    es_grave: Mapped[bool] = mapped_column(Boolean)

    odontograma: Mapped['Odontograma'] = relationship('Odontograma', back_populates='entradas_diente')


class OdontogramaEntradaParDientes(Base):
    __tablename__ = 'odontograma_entrada_par_dientes'
    __table_args__ = (
        ForeignKeyConstraint(['odontograma_id'], ['odontograma.odontograma_id'], name='odontograma_entrada_par_dientes_odontograma_id_fkey'),
        PrimaryKeyConstraint('odontograma_id', 'id', name='odontograma_entrada_par_dientes_pkey')
    )

    odontograma_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    diente_uno: Mapped[int] = mapped_column(Integer)
    diente_dos: Mapped[int] = mapped_column(Integer)
    tipo_entrada: Mapped[str] = mapped_column(String)
    es_grave: Mapped[bool] = mapped_column(Boolean)

    odontograma: Mapped['Odontograma'] = relationship('Odontograma', back_populates='entradas_par_dientes')


class OdontogramaEntradaRangoDientes(Base):
    __tablename__ = 'odontograma_entrada_rango_dientes'
    __table_args__ = (
        ForeignKeyConstraint(['odontograma_id'], ['odontograma.odontograma_id'], name='odontograma_entrada_rango_dientes_odontograma_id_fkey'),
        PrimaryKeyConstraint('odontograma_id', 'id', name='odontograma_entrada_rango_dientes_pkey')
    )

    odontograma_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    diente_inicial: Mapped[int] = mapped_column(Integer)
    diente_final: Mapped[int] = mapped_column(Integer)
    tipo_entrada: Mapped[str] = mapped_column(String)
    es_grave: Mapped[bool] = mapped_column(Boolean)

    odontograma: Mapped['Odontograma'] = relationship('Odontograma', back_populates='entradas_rango_dientes')


class TratamientoMaterial(Base):
    __tablename__ = 'tratamiento_material'
    __table_args__ = (
        ForeignKeyConstraint(['material_id'], ['material.material_id'], name='tratamiento_material_material_id_fkey'),
        ForeignKeyConstraint(['tratamiento_id'], ['tratamiento.tratamiento_id'], name='tratamiento_material_tratamiento_id_fkey'),
        PrimaryKeyConstraint('tratamiento_id', 'material_id', name='tratamiento_material_pkey')
    )

    tratamiento_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    material_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    cantidad: Mapped[int] = mapped_column(Integer)
    costo: Mapped[int] = mapped_column(BigInteger)

    material: Mapped['Material'] = relationship('Material', back_populates='tratamientos')
    tratamiento: Mapped['Tratamiento'] = relationship('Tratamiento', back_populates='materiales')


class TratamientoPago(Base):
    __tablename__ = 'tratamiento_pago'
    __table_args__ = (
        ForeignKeyConstraint(['tratamiento_id'], ['tratamiento.tratamiento_id'], name='tratamiento_pago_tratamiento_id_fkey'),
        PrimaryKeyConstraint('tratamiento_id', 'pago_id', name='tratamiento_pago_pkey')
    )

    tratamiento_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    pago_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    metodo: Mapped[str] = mapped_column(String)
    monto: Mapped[int] = mapped_column(BigInteger)

    tratamiento: Mapped['Tratamiento'] = relationship('Tratamiento', back_populates='pagos')


class TratamientoProcedimiento(Base):
    __tablename__ = 'tratamiento_procedimiento'
    __table_args__ = (
        ForeignKeyConstraint(['procedimiento_id'], ['procedimiento.procedimiento_id'], name='tratamiento_procedimiento_procedimiento_id_fkey'),
        ForeignKeyConstraint(['tratamiento_id'], ['tratamiento.tratamiento_id'], name='tratamiento_procedimiento_tratamiento_id_fkey'),
        PrimaryKeyConstraint('tratamiento_id', 'procedimiento_id', name='tratamiento_procedimiento_pkey')
    )

    tratamiento_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    procedimiento_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    cantidad: Mapped[int] = mapped_column(Integer)
    costo: Mapped[int] = mapped_column(BigInteger)

    procedimiento: Mapped['Procedimiento'] = relationship('Procedimiento', back_populates='tratamientos')
    tratamiento: Mapped['Tratamiento'] = relationship('Tratamiento', back_populates='procedimientos')


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
    odontologo_id: Mapped[str] = mapped_column(Text)

    odontologo: Mapped['Odontologo'] = relationship('Odontologo', back_populates='sesiones')
    tratamiento: Mapped['Tratamiento'] = relationship('Tratamiento', back_populates='sesiones')
