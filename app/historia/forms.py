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
<<<<<<< Updated upstream
    # Tratamiento id: Cambiar a SelectField si es necesario
    tratamiento_id = SelectField('Seleccione el tratamiento', coerce=int, validators=[DataRequired()])
    
    # Método de pago
=======
>>>>>>> Stashed changes
    metodo = SelectField(
        'Método de pago',
        choices=[
            ('Efectivo', 'Efectivo'),
            ('Tarjeta', 'Tarjeta'),
            ('Transferencia', 'Transferencia'),
            ('Yape', 'Yape'),
            ('Plin', 'Plin'),
        ],
        validators=[DataRequired()],
        render_kw={"aria-label": "Método de pago"}  # Mejora accesibilidad
    )

    # Monto
    monto = DecimalField('Monto a pagar', validators=[
        DataRequired(message="El monto es obligatorio."),
        NumberRange(min=0.01, message="Debe ingresar un monto positivo mayor a cero.")
    ], places=2, render_kw={"aria-label": "Monto a pagar"})
    
    submit = SubmitField('Registrar pago', render_kw={"class": "btn-submit"})

    # Custom validation if needed (for example, if you want to check if the monto is a valid amount)
    def validate_monto(form, field):
        if field.data <= 0:
            raise ValidationError("El monto debe ser un valor positivo.")


class FormularioAgregarProcedimiento(FlaskForm):
    nombre = StringField('Nombre del procedimiento', validators=[DataRequired()])
    submit = SubmitField('Registrar')


class FormularioPresupuesto(FlaskForm):
    pass  # no necesita campos visibles, solo para CSRF
