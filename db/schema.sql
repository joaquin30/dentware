CREATE TYPE estado_civil_t as ENUM ('Soltero', 'Casado', 'Conviviente', 'Viudo', 'Divorciado', 'Separado');

CREATE TABLE paciente (
    paciente_dni TEXT NOT NULL,
    nombres TEXT NOT NULL,
    apellidos TEXT NOT NULL,
    edad INTEGER NOT NULL,
    fecha_de_nacimiento DATE NOT NULL,
    lugar_de_nacimiento TEXT NOT NULL,
    estado_civil estado_civil_t NOT NULL,
    direccion TEXT NOT NULL,
    telefono TEXT NOT NULL,
    email TEXT NOT NULL,
    ocupacion TEXT NOT NULL,
    lugar_trabajo_estudio TEXT NOT NULL,
    apoderado TEXT NOT NULL,
    novedades TEXT NOT NULL,
    PRIMARY KEY (paciente_dni)
);

CREATE TABLE historia_examenes_estomatologicos (
    historia_id INTEGER NOT NULL,
    maxilares BOOLEAN NOT NULL,
    vestíbulo BOOLEAN NOT NULL,
    labios BOOLEAN NOT NULL,
    encia BOOLEAN NOT NULL,
    paladar BOOLEAN NOT NULL,
    oclusión BOOLEAN NOT NULL,
    lengua BOOLEAN NOT NULL,
    atm BOOLEAN NOT NULL,
    piso_de_boca BOOLEAN NOT NULL,
    ganglios BOOLEAN NOT NULL,
    orifaringe BOOLEAN NOT NULL,
    halitosis BOOLEAN NOT NULL,
    PRIMARY KEY (historia_id)
);

CREATE TABLE historia_antecedentes_medicos (
    historia_id INTEGER NOT NULL,
    enfermedad_cardiaca BOOLEAN NOT NULL,
    enfermedad_renal BOOLEAN NOT NULL,
    vih BOOLEAN NOT NULL,
    alergias BOOLEAN NOT NULL,
    hemorragias BOOLEAN NOT NULL,
    medicado BOOLEAN NOT NULL,
    diabetes BOOLEAN NOT NULL,
    hepatitis BOOLEAN NOT NULL,
    problemas_hemorragicos BOOLEAN NOT NULL,
    presion_alta BOOLEAN NOT NULL,
    epilepsia BOOLEAN NOT NULL,
    embarazo BOOLEAN NOT NULL,
    otros TEXT NOT NULL,
    PRIMARY KEY (historia_id)
);

CREATE TABLE historia_contraindicacion (
    historia_id INTEGER NOT NULL,
    contraindicacion_id SERIAL NOT NULL,
    descripcion TEXT NOT NULL,
    es_grave BOOLEAN NOT NULL,
    PRIMARY KEY (historia_id, contraindicacion_id)
);

CREATE TABLE historia_examen (
    historia_id INTEGER NOT NULL,
    examen_id SERIAL NOT NULL,
    titulo TEXT NOT NULL,
    fecha DATE NOT NULL,
    ruta_archivo TEXT NOT NULL,
    PRIMARY KEY (historia_id, examen_id)
);

CREATE TABLE tratamiento (
    tratamiento_id SERIAL NOT NULL,
    fecha_creacion DATE NOT NULL,
    descripcion TEXT NOT NULL,
    en_curso BOOLEAN NOT NULL,
    odontologo_dni TEXT NOT NULL,
    historia_clinica_id INTEGER NOT NULL,
    PRIMARY KEY (tratamiento_id)
);

CREATE TABLE tratamiento_sesion (
    tratamiento_id INTEGER NOT NULL,
    sesion_id SERIAL NOT NULL,
    fecha DATE NOT NULL,
    descripcion TEXT NOT NULL,
    observaciones TEXT NOT NULL,
    odontologo_dni TEXT NOT NULL,
    PRIMARY KEY (tratamiento_id, sesion_id)
);

CREATE TYPE tipo_odontograma_t as ENUM ('Inicial', 'Tratamiento', 'Evolución');

CREATE TABLE odontograma (
    odontograma_id SERIAL NOT NULL,
    historia_clinica_id INTEGER NOT NULL,
    tipo_odontograma tipo_odontograma_t NOT NULL,
    ultima_edicion DATE NOT NULL,
    especificaciones TEXT NOT NULL,
    observaciones TEXT NOT NULL,
    PRIMARY KEY (odontograma_id)
);

CREATE TABLE tratamiento_pago (
    tratamiento_id INTEGER NOT NULL,
    pago_id SERIAL NOT NULL,
    metodo TEXT NOT NULL,
    monto BIGINT NOT NULL,
    PRIMARY KEY (tratamiento_id, pago_id)
);

CREATE TABLE historia (
    historia_id SERIAL NOT NULL,
    fecha_creacion DATE NOT NULL,
    paciente_dni TEXT NOT NULL,
    PRIMARY KEY (historia_id)
);

CREATE TABLE odontograma_entrada_par_dientes (
    odontograma_id INTEGER NOT NULL,
    id SERIAL NOT NULL,
    diente_uno INTEGER NOT NULL,
    diente_dos INTEGER NOT NULL,
    tipo_entrada TEXT NOT NULL,
    es_grave BOOLEAN NOT NULL,
    PRIMARY KEY (odontograma_id, id)
);

CREATE TABLE odontograma_entrada_areas_diente (
    odontograma_id INTEGER NOT NULL,
    id SERIAL NOT NULL,
    diente INTEGER NOT NULL,
    tipo_entrada TEXT NOT NULL,
    areas INTEGER ARRAY NOT NULL,
    es_grave BOOLEAN NOT NULL,
    PRIMARY KEY (odontograma_id, id)
);

CREATE TABLE odontograma_entrada_bordes_diente (
    odontograma_id INTEGER NOT NULL,
    id SERIAL NOT NULL,
    diente INTEGER NOT NULL,
    tipo_entrada TEXT NOT NULL,
    bordes INTEGER ARRAY NOT NULL,
    es_grave BOOLEAN NOT NULL,
    PRIMARY KEY (odontograma_id, id)
);

CREATE TABLE odontograma_entrada_diente (
    odontograma_id INTEGER NOT NULL,
    id SERIAL NOT NULL,
    diente INTEGER NOT NULL,
    tipo_entrada TEXT NOT NULL,
    es_grave BOOLEAN NOT NULL,
    PRIMARY KEY (odontograma_id, id)
);

CREATE TABLE odontograma_entrada_rango_dientes (
    odontograma_id INTEGER NOT NULL,
    id SERIAL NOT NULL,
    diente_inicial INTEGER NOT NULL,
    diente_final INTEGER NOT NULL,
    tipo_entrada TEXT NOT NULL,
    es_grave BOOLEAN NOT NULL,
    PRIMARY KEY (odontograma_id, id)
);

CREATE TYPE tipo_odontologo_t as ENUM ('Interno', 'Externo', 'Temporal');

CREATE TABLE odontologo (
    odontologo_dni TEXT NOT NULL,
    nombre TEXT NOT NULL,
    tipo_odontologo tipo_odontologo_t NOT NULL,
    PRIMARY KEY (odontologo_dni)
);

CREATE TABLE procedimiento (
    procedimiento_id SERIAL NOT NULL,
    nombre TEXT NOT NULL,
    costo_referencial BIGINT NOT NULL,
    PRIMARY KEY (procedimiento_id)
);

CREATE TABLE material (
    material_id SERIAL NOT NULL,
    nombre TEXT NOT NULL,
    costo_referencial BIGINT NOT NULL,
    PRIMARY KEY (material_id)
);

CREATE TABLE tratamiento_material (
    tratamiento_id INTEGER NOT NULL,
    material_id INTEGER NOT NULL,
    cantidad INTEGER NOT NULL,
    costo BIGINT NOT NULL,
    PRIMARY KEY (tratamiento_id, material_id)
);

CREATE TABLE tratamiento_procedimiento (
    tratamiento_id INTEGER NOT NULL,
    procedimiento_id INTEGER NOT NULL,
    cantidad INTEGER NOT NULL,
    costo BIGINT NOT NULL,
    PRIMARY KEY (tratamiento_id, procedimiento_id)
);

ALTER TABLE historia_examenes_estomatologicos ADD FOREIGN KEY (historia_id) REFERENCES historia(historia_id);
ALTER TABLE historia_antecedentes_medicos ADD FOREIGN KEY (historia_id) REFERENCES historia(historia_id);
ALTER TABLE historia_contraindicacion ADD FOREIGN KEY (historia_id) REFERENCES historia(historia_id);
ALTER TABLE historia_examen ADD FOREIGN KEY (historia_id) REFERENCES historia(historia_id);
ALTER TABLE tratamiento ADD FOREIGN KEY (historia_clinica_id) REFERENCES historia(historia_id);
ALTER TABLE tratamiento ADD FOREIGN KEY (odontologo_dni) REFERENCES odontologo(odontologo_dni);
ALTER TABLE tratamiento_sesion ADD FOREIGN KEY (tratamiento_id) REFERENCES tratamiento(tratamiento_id);
ALTER TABLE tratamiento_sesion ADD FOREIGN KEY (odontologo_dni) REFERENCES odontologo(odontologo_dni);
ALTER TABLE odontograma ADD FOREIGN KEY (historia_clinica_id) REFERENCES historia(historia_id);
ALTER TABLE tratamiento_pago ADD FOREIGN KEY (tratamiento_id) REFERENCES tratamiento(tratamiento_id);
ALTER TABLE historia ADD FOREIGN KEY (paciente_dni) REFERENCES paciente(paciente_dni);
ALTER TABLE odontograma_entrada_par_dientes ADD FOREIGN KEY (odontograma_id) REFERENCES odontograma(odontograma_id);
ALTER TABLE odontograma_entrada_areas_diente ADD FOREIGN KEY (odontograma_id) REFERENCES odontograma(odontograma_id);
ALTER TABLE odontograma_entrada_bordes_diente ADD FOREIGN KEY (odontograma_id) REFERENCES odontograma(odontograma_id);
ALTER TABLE odontograma_entrada_diente ADD FOREIGN KEY (odontograma_id) REFERENCES odontograma(odontograma_id);
ALTER TABLE odontograma_entrada_rango_dientes ADD FOREIGN KEY (odontograma_id) REFERENCES odontograma(odontograma_id);
ALTER TABLE tratamiento_material ADD FOREIGN KEY (tratamiento_id) REFERENCES tratamiento(tratamiento_id);
ALTER TABLE tratamiento_material ADD FOREIGN KEY (material_id) REFERENCES material(material_id);
ALTER TABLE tratamiento_procedimiento ADD FOREIGN KEY (tratamiento_id) REFERENCES tratamiento(tratamiento_id);
ALTER TABLE tratamiento_procedimiento ADD FOREIGN KEY (procedimiento_id) REFERENCES procedimiento(procedimiento_id);