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
from wtforms.validators import DataRequired, NumberRange

from wtforms import TextAreaField
from wtforms.validators import Optional

class HistoriaExamenForm(FlaskForm):
    archivo = FileField('Archivo', validators=[
        FileRequired(),
        FileAllowed(['pdf', 'jpg', 'jpeg', 'png'], 'Solo archivos PDF, JPG, JPEG o PNG')
    ])
    observaciones = TextAreaField('Observaciones', validators=[Optional()])
    historia_id = HiddenField(validators=[DataRequired()])
    submit = SubmitField('Subir examen')




class HistoriaContraindicacionForm(FlaskForm):
    descripcion = StringField('Descripción', validators=[DataRequired()])
    es_grave = BooleanField('Es grave')
    submit = SubmitField('Guardar')
    historia_id = HiddenField()

# Para manejar múltiples contraindicaciones, puedes usar FieldList y FormField:
class ContraindicacionesForm(FlaskForm):
    contraindicaciones = FieldList(FormField(HistoriaContraindicacionForm))
    submit = SubmitField('Guardar')
    historia_id = HiddenField()


class NovedadForm(FlaskForm):
    novedad_id = HiddenField()
    descripcion = StringField('Descripción', validators=[DataRequired()])
    es_importante = BooleanField('Es importante')

class PacienteNovedadesForm(FlaskForm):
    novedades = FieldList(FormField(NovedadForm), min_entries=1)
    submit = SubmitField('Guardar')

class FormularioTratamiento(FlaskForm):
    descripcion = StringField('Descripción', validators=[DataRequired()])
    odontologo_id = SelectField('Odontólogo', coerce=int, validators=[DataRequired()])
    en_curso = BooleanField('¿En curso?')
    fecha_creacion = DateField('Fecha', format='%Y-%m-%d', validators=[DataRequired()])
    costo = DecimalField('Costo', places=2, rounding=None, validators=[
        DataRequired(message="Debe ingresar un costo."),
        NumberRange(min=0, message="El costo no puede ser negativo.")
    ])


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

class LineaPresupuestoForm(FlaskForm):
    procedimiento = StringField('Procedimiento', validators=[DataRequired()])
    material = StringField('Material', validators=[Optional()])
    costo = DecimalField('Costo', validators=[DataRequired(), NumberRange(min=0)])

class PresupuestoForm(FlaskForm):
    tratamiento_id = HiddenField(validators=[DataRequired()])
    lineas = FieldList(FormField(LineaPresupuestoForm), min_entries=1)
        
class FormularioPago(FlaskForm):
    tratamiento_id = HiddenField(validators=[DataRequired()])
    metodo = SelectField(
        'Método de pago',
        choices=[
            ('efectivo', 'Efectivo'),
            ('tarjeta', 'Tarjeta'),
            ('transferencia', 'Transferencia'),
            ('yape', 'Yape'),
            ('plin', 'Plin'),
        ],
        validators=[DataRequired()]
    )
    monto = DecimalField('Monto a pagar', validators=[
        DataRequired(),
        NumberRange(min=0.01, message="Debe ingresar un monto positivo")
    ])
    submit = SubmitField('Registrar pago')