# GENERADO POR: sqlacodegen postgresql+psycopg://user:pass@localhost:5432/dentware > app/models.py

from typing import List

from sqlalchemy import ARRAY, BigInteger, Boolean, Date, Enum, ForeignKeyConstraint, Integer, PrimaryKeyConstraint, Text, String
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

    tratamiento_material: Mapped[List['TratamientoMaterial']] = relationship('TratamientoMaterial', back_populates='material')


class Odontologo(Base):
    __tablename__ = 'odontologo'
    __table_args__ = (
        PrimaryKeyConstraint('odontologo_dni', name='odontologo_pkey'),
    )

    odontologo_dni: Mapped[str] = mapped_column(String, primary_key=True)
    nombre: Mapped[str] = mapped_column(String)
    tipo_odontologo: Mapped[str] = mapped_column(Enum('Interno', 'Externo', 'Temporal', name='tipo_odontologo_t'))

    tratamiento: Mapped[List['Tratamiento']] = relationship('Tratamiento', back_populates='odontologo')
    tratamiento_sesion: Mapped[List['TratamientoSesion']] = relationship('TratamientoSesion', back_populates='odontologo')


class Paciente(Base):
    __tablename__ = 'paciente'
    __table_args__ = (
        PrimaryKeyConstraint('paciente_dni', name='paciente_pkey'),
    )

    paciente_dni: Mapped[str] = mapped_column(String, primary_key=True)
    nombres: Mapped[str] = mapped_column(String, info={'label': 'Nombres'})
    apellidos: Mapped[str] = mapped_column(String)
    edad: Mapped[int] = mapped_column(Integer)
    fecha_de_nacimiento: Mapped[datetime.date] = mapped_column(Date)
    lugar_de_nacimiento: Mapped[str] = mapped_column(String)
    estado_civil: Mapped[str] = mapped_column(Enum('Soltero', 'Casado', 'Conviviente', 'Viudo', 'Divorciado', 'Separado', name='estado_civil_t'))
    direccion: Mapped[str] = mapped_column(String)
    telefono: Mapped[str] = mapped_column(String)
    email: Mapped[str] = mapped_column(String)
    ocupacion: Mapped[str] = mapped_column(String)
    lugar_trabajo_estudio: Mapped[str] = mapped_column(String)
    apoderado: Mapped[str] = mapped_column(String)
    novedades: Mapped[str] = mapped_column(Text)

    historia: Mapped[List['Historia']] = relationship('Historia', back_populates='paciente')


class Procedimiento(Base):
    __tablename__ = 'procedimiento'
    __table_args__ = (
        PrimaryKeyConstraint('procedimiento_id', name='procedimiento_pkey'),
    )

    procedimiento_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    nombre: Mapped[str] = mapped_column(String)
    costo_referencial: Mapped[int] = mapped_column(BigInteger)

    tratamiento_procedimiento: Mapped[List['TratamientoProcedimiento']] = relationship('TratamientoProcedimiento', back_populates='procedimiento')


class Historia(Base):
    __tablename__ = 'historia'
    __table_args__ = (
        ForeignKeyConstraint(['paciente_dni'], ['paciente.paciente_dni'], name='historia_paciente_dni_fkey'),
        PrimaryKeyConstraint('historia_id', name='historia_pkey')
    )

    historia_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    fecha_creacion: Mapped[datetime.date] = mapped_column(Date)
    paciente_dni: Mapped[str] = mapped_column(String)

    paciente: Mapped['Paciente'] = relationship('Paciente', back_populates='historia')
    historia_contraindicacion: Mapped[List['HistoriaContraindicacion']] = relationship('HistoriaContraindicacion', back_populates='historia')
    historia_examen: Mapped[List['HistoriaExamen']] = relationship('HistoriaExamen', back_populates='historia')
    odontograma: Mapped[List['Odontograma']] = relationship('Odontograma', back_populates='historia_clinica')
    tratamiento: Mapped[List['Tratamiento']] = relationship('Tratamiento', back_populates='historia_clinica')


class HistoriaAntecedentesMedicos(Historia):
    __tablename__ = 'historia_antecedentes_medicos'
    __table_args__ = (
        ForeignKeyConstraint(['historia_id'], ['historia.historia_id'], name='historia_antecedentes_medicos_historia_id_fkey'),
        PrimaryKeyConstraint('historia_id', name='historia_antecedentes_medicos_pkey')
    )

    historia_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    enfermedad_cardiaca: Mapped[bool] = mapped_column(Boolean)
    enfermedad_renal: Mapped[bool] = mapped_column(Boolean)
    vih: Mapped[bool] = mapped_column(Boolean)
    alergias: Mapped[bool] = mapped_column(Boolean)
    hemorragias: Mapped[bool] = mapped_column(Boolean)
    medicado: Mapped[bool] = mapped_column(Boolean)
    diabetes: Mapped[bool] = mapped_column(Boolean)
    hepatitis: Mapped[bool] = mapped_column(Boolean)
    problemas_hemorragicos: Mapped[bool] = mapped_column(Boolean)
    presion_alta: Mapped[bool] = mapped_column(Boolean)
    epilepsia: Mapped[bool] = mapped_column(Boolean)
    embarazo: Mapped[bool] = mapped_column(Boolean)
    otros: Mapped[str] = mapped_column(Text)


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

    historia: Mapped['Historia'] = relationship('Historia', back_populates='historia_contraindicacion')


class HistoriaExamen(Base):
    __tablename__ = 'historia_examen'
    __table_args__ = (
        ForeignKeyConstraint(['historia_id'], ['historia.historia_id'], name='historia_examen_historia_id_fkey'),
        PrimaryKeyConstraint('historia_id', 'examen_id', name='historia_examen_pkey')
    )

    historia_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    examen_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    titulo: Mapped[str] = mapped_column(String)
    fecha: Mapped[datetime.date] = mapped_column(Date)
    ruta_archivo: Mapped[str] = mapped_column(String)

    historia: Mapped['Historia'] = relationship('Historia', back_populates='historia_examen')


class HistoriaExamenesEstomatologicos(Historia):
    __tablename__ = 'historia_examenes_estomatologicos'
    __table_args__ = (
        ForeignKeyConstraint(['historia_id'], ['historia.historia_id'], name='historia_examenes_estomatologicos_historia_id_fkey'),
        PrimaryKeyConstraint('historia_id', name='historia_examenes_estomatologicos_pkey')
    )

    historia_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    maxilares: Mapped[bool] = mapped_column(Boolean)
    vestíbulo: Mapped[bool] = mapped_column(Boolean)
    labios: Mapped[bool] = mapped_column(Boolean)
    encia: Mapped[bool] = mapped_column(Boolean)
    paladar: Mapped[bool] = mapped_column(Boolean)
    oclusión: Mapped[bool] = mapped_column(Boolean)
    lengua: Mapped[bool] = mapped_column(Boolean)
    atm: Mapped[bool] = mapped_column(Boolean)
    piso_de_boca: Mapped[bool] = mapped_column(Boolean)
    ganglios: Mapped[bool] = mapped_column(Boolean)
    orifaringe: Mapped[bool] = mapped_column(Boolean)
    halitosis: Mapped[bool] = mapped_column(Boolean)


class Odontograma(Base):
    __tablename__ = 'odontograma'
    __table_args__ = (
        ForeignKeyConstraint(['historia_clinica_id'], ['historia.historia_id'], name='odontograma_historia_clinica_id_fkey'),
        PrimaryKeyConstraint('odontograma_id', name='odontograma_pkey')
    )

    odontograma_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    historia_clinica_id: Mapped[int] = mapped_column(Integer)
    tipo_odontograma: Mapped[str] = mapped_column(Enum('Inicial', 'Tratamiento', 'Evolución', name='tipo_odontograma_t'))
    ultima_edicion: Mapped[datetime.date] = mapped_column(Date)
    especificaciones: Mapped[str] = mapped_column(Text)
    observaciones: Mapped[str] = mapped_column(Text)

    historia_clinica: Mapped['Historia'] = relationship('Historia', back_populates='odontograma')
    odontograma_entrada_areas_diente: Mapped[List['OdontogramaEntradaAreasDiente']] = relationship('OdontogramaEntradaAreasDiente', back_populates='odontograma')
    odontograma_entrada_bordes_diente: Mapped[List['OdontogramaEntradaBordesDiente']] = relationship('OdontogramaEntradaBordesDiente', back_populates='odontograma')
    odontograma_entrada_diente: Mapped[List['OdontogramaEntradaDiente']] = relationship('OdontogramaEntradaDiente', back_populates='odontograma')
    odontograma_entrada_par_dientes: Mapped[List['OdontogramaEntradaParDientes']] = relationship('OdontogramaEntradaParDientes', back_populates='odontograma')
    odontograma_entrada_rango_dientes: Mapped[List['OdontogramaEntradaRangoDientes']] = relationship('OdontogramaEntradaRangoDientes', back_populates='odontograma')


class Tratamiento(Base):
    __tablename__ = 'tratamiento'
    __table_args__ = (
        ForeignKeyConstraint(['historia_clinica_id'], ['historia.historia_id'], name='tratamiento_historia_clinica_id_fkey'),
        ForeignKeyConstraint(['odontologo_dni'], ['odontologo.odontologo_dni'], name='tratamiento_odontologo_dni_fkey'),
        PrimaryKeyConstraint('tratamiento_id', name='tratamiento_pkey')
    )

    tratamiento_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    fecha_creacion: Mapped[datetime.date] = mapped_column(Date)
    descripcion: Mapped[str] = mapped_column(String)
    en_curso: Mapped[bool] = mapped_column(Boolean)
    odontologo_dni: Mapped[str] = mapped_column(String)
    historia_clinica_id: Mapped[int] = mapped_column(Integer)

    historia_clinica: Mapped['Historia'] = relationship('Historia', back_populates='tratamiento')
    odontologo: Mapped['Odontologo'] = relationship('Odontologo', back_populates='tratamiento')
    tratamiento_material: Mapped[List['TratamientoMaterial']] = relationship('TratamientoMaterial', back_populates='tratamiento')
    tratamiento_pago: Mapped[List['TratamientoPago']] = relationship('TratamientoPago', back_populates='tratamiento')
    tratamiento_procedimiento: Mapped[List['TratamientoProcedimiento']] = relationship('TratamientoProcedimiento', back_populates='tratamiento')
    tratamiento_sesion: Mapped[List['TratamientoSesion']] = relationship('TratamientoSesion', back_populates='tratamiento')


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
    areas: Mapped[list] = mapped_column(ARRAY(Integer()))
    es_grave: Mapped[bool] = mapped_column(Boolean)

    odontograma: Mapped['Odontograma'] = relationship('Odontograma', back_populates='odontograma_entrada_areas_diente')


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
    bordes: Mapped[list] = mapped_column(ARRAY(Integer()))
    es_grave: Mapped[bool] = mapped_column(Boolean)

    odontograma: Mapped['Odontograma'] = relationship('Odontograma', back_populates='odontograma_entrada_bordes_diente')


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

    odontograma: Mapped['Odontograma'] = relationship('Odontograma', back_populates='odontograma_entrada_diente')


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

    odontograma: Mapped['Odontograma'] = relationship('Odontograma', back_populates='odontograma_entrada_par_dientes')


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

    odontograma: Mapped['Odontograma'] = relationship('Odontograma', back_populates='odontograma_entrada_rango_dientes')


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

    material: Mapped['Material'] = relationship('Material', back_populates='tratamiento_material')
    tratamiento: Mapped['Tratamiento'] = relationship('Tratamiento', back_populates='tratamiento_material')


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

    tratamiento: Mapped['Tratamiento'] = relationship('Tratamiento', back_populates='tratamiento_pago')


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

    procedimiento: Mapped['Procedimiento'] = relationship('Procedimiento', back_populates='tratamiento_procedimiento')
    tratamiento: Mapped['Tratamiento'] = relationship('Tratamiento', back_populates='tratamiento_procedimiento')


class TratamientoSesion(Base):
    __tablename__ = 'tratamiento_sesion'
    __table_args__ = (
        ForeignKeyConstraint(['odontologo_dni'], ['odontologo.odontologo_dni'], name='tratamiento_sesion_odontologo_dni_fkey'),
        ForeignKeyConstraint(['tratamiento_id'], ['tratamiento.tratamiento_id'], name='tratamiento_sesion_tratamiento_id_fkey'),
        PrimaryKeyConstraint('tratamiento_id', 'sesion_id', name='tratamiento_sesion_pkey')
    )

    tratamiento_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    sesion_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    fecha: Mapped[datetime.date] = mapped_column(Date)
    descripcion: Mapped[str] = mapped_column(String)
    observaciones: Mapped[str] = mapped_column(Text)
    odontologo_dni: Mapped[str] = mapped_column(Text)

    odontologo: Mapped['Odontologo'] = relationship('Odontologo', back_populates='tratamiento_sesion')
    tratamiento: Mapped['Tratamiento'] = relationship('Tratamiento', back_populates='tratamiento_sesion')
