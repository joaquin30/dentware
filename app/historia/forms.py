from app.extensions import ModelForm
from flask_wtf import FlaskForm
from wtforms import StringField, DateField, BooleanField, FileField, SubmitField, HiddenField
from wtforms.validators import DataRequired, Optional
from flask_wtf.file import FileAllowed, FileRequired
from app.models import HistoriaContraindicacion, Tratamiento, TratamientoSesion, Procedimiento
from wtforms import FieldList, FormField, TextAreaField
from wtforms import SelectField, IntegerField
from flask_wtf import FlaskForm
from wtforms import DecimalField
from wtforms.validators import NumberRange
from wtforms import StringField, SelectField, BooleanField, DateField, DecimalField
from wtforms.validators import DataRequired, NumberRange, ValidationError

from wtforms import TextAreaField
from wtforms.validators import Optional

# Formulario para registrar un examen auxiliar en la historia clínica de un paciente. Relacionado con la entidad CCHistoriaExam

class HistoriaExamenForm(FlaskForm):
    archivo = FileField('Archivo', validators=[
        FileRequired(),
        FileAllowed(['pdf', 'jpg', 'jpeg', 'png'], 'Solo archivos PDF, JPG, JPEG o PNG')
    ])
    observaciones = TextAreaField('Observaciones', validators=[Optional()])
    historia_id = HiddenField(validators=[DataRequired()])
    submit = SubmitField('Subir examen')



# Formulario de contraindicaciones médicas. Relacionado con la entidad CCHistoriaContraindicacion

class HistoriaContraindicacionForm(FlaskForm):
    descripcion = StringField('Descripción', validators=[DataRequired()])
    es_grave = BooleanField('Es grave')
    submit = SubmitField('Guardar')
    historia_id = HiddenField()

# Formulario para registrar las contraindicaciones médicas de un paciente en su historia clínica. Relacionado con la entidad CCHistoriaContraindicacion
# Para manejar múltiples contraindicaciones, puedes usar FieldList y FormField:

class ContraindicacionesForm(FlaskForm):
    contraindicaciones = FieldList(FormField(HistoriaContraindicacionForm))
    submit = SubmitField('Guardar')
    historia_id = HiddenField()

# Formulario para registrar las novedades de un paciente. Relación con la entidad CCHistoriaNovedad

class NovedadForm(FlaskForm):
    novedad_id = HiddenField()
    descripcion = StringField('Descripción', validators=[DataRequired()])
    es_importante = BooleanField('Es importante')

# Formulario para manejar múltiples novedades de un paciente en su historia clínica. Relacionado con la entidad CCHistoriaNovedad

class PacienteNovedadesForm(FlaskForm):
    novedades = FieldList(FormField(NovedadForm), min_entries=1)
    submit = SubmitField('Guardar')

# Formulario para registrar tratamientos odontológicos. Relacionado con la entidad CCTratamiento

class FormularioTratamiento(FlaskForm):
    descripcion = StringField('Descripción', validators=[DataRequired()])
    odontologo_id = SelectField('Odontólogo', coerce=int, validators=[DataRequired()])
    en_curso = BooleanField('¿En curso?')
    fecha_creacion = DateField('Fecha', format='%Y-%m-%d', validators=[DataRequired()])

# Formulario para registrar una sesión de tratamiento odontológico. Relacionado con la entidad CCTratamientoSesion
# class Meta significa que este formulario está basado en un modelo de base de datos, en este caso TratamientoSesion.

class FormularioTratamientoSesion(ModelForm):
    tratamiento_id = HiddenField(validators=[DataRequired()])
    sesion_id = HiddenField()  # Se asigna incremental en la ruta, no se valida en el formulario
    odontologo_id = SelectField('Odontólogo', coerce=str, validators=[DataRequired()])
    fecha = DateField('Fecha', format='%Y-%m-%d', validators=[DataRequired()])
    descripcion = TextAreaField('Descripción', validators=[DataRequired()])
    observaciones = TextAreaField('Observaciones', validators=[Optional()])
    submit = SubmitField('Guardar sesión')

    class Meta:
        model = TratamientoSesion
        include_primary_keys = True

# Formulario para registrar un presupuesto de tratamiento odontológico. Relacionado con la entidad CCProcedimiento

class LineaPresupuestoForm(FlaskForm):
    procedimiento = StringField('Procedimiento', validators=[DataRequired()])
    material = StringField('Material', validators=[Optional()])
    costo = DecimalField('Costo', validators=[DataRequired(), NumberRange(min=0)])

# Formulario para manejar un presupuesto de tratamiento odontológico. Relacionado con la entidad CCProcedimiento
# Este formulario permite registrar múltiples líneas de presupuesto para un tratamiento específico.

class PresupuestoForm(FlaskForm):
    tratamiento_id = HiddenField(validators=[DataRequired()])
    lineas = FieldList(FormField(LineaPresupuestoForm), min_entries=1)
        
# Formulario para registrar un pago realizado por un paciente. Relacionado con la entidad CCPago
# Este formulario permite registrar el método de pago y el monto a pagar.

class FormularioPago(FlaskForm):
    # Método de pago
    metodo = SelectField(
        'Método de pago',
        choices=[
            ('Efectivo', 'Efectivo'),
            ('Tarjeta', 'Tarjeta'),
            ('Transferencia', 'Transferencia'),
            ('Yape', 'Yape'),
            ('Plin', 'Plin'),
            ('Otros', 'Otros'),
        ],
        validators=[DataRequired()],
        render_kw={"aria-label": "Método de pago"}
    )

    # Monto
    monto = DecimalField('Monto a pagar', validators=[
        DataRequired(message="El monto es obligatorio."),
        NumberRange(min=0.01, message="Debe ingresar un monto positivo mayor a cero.")
    ], places=2, render_kw={"aria-label": "Monto a pagar"})
    
    submit = SubmitField('Registrar pago', render_kw={"class": "btn-submit"})

    # Validación para el campo monto, verifica que sea un valor positivo
    def validate_monto(form, field):
        if field.data <= 0:
            raise ValidationError("El monto debe ser un valor positivo.")

# Formulario para registrar un procedimiento odontológico. Relacionado con la entidad CCProcedimiento
class FormularioAgregarProcedimiento(FlaskForm):
    nombre = StringField('Nombre del procedimiento', validators=[DataRequired()])
    #costo_referencial = DecimalField('Costo referencial (S/.), en caso el costo varíe por procedimiento, coloque 0', validators=[DataRequired(), NumberRange(min=0)])
    submit = SubmitField('Registrar')

class FormularioPresupuesto(FlaskForm):
    pass  # no necesita campos visibles, solo para CSRF
