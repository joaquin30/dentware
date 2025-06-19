from app.extensions import ModelForm
from flask_wtf import FlaskForm
from wtforms import StringField, DateField, BooleanField, FileField, SubmitField, HiddenField
from wtforms.validators import DataRequired, Optional
from flask_wtf.file import FileAllowed, FileRequired
from app.models import HistoriaContraindicacion, Tratamiento, TratamientoSesion
from wtforms import FieldList, FormField, TextAreaField
from wtforms import SelectField
from flask_wtf import FlaskForm

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
    odontologo_id = SelectField('Odontólogo', coerce=int, validators=[DataRequired()])
    en_curso = BooleanField('¿En curso?')
    fecha = DateField('Fecha', format='%Y-%m-%d', validators=[DataRequired()])
    descripcion = TextAreaField('Tratamiento', validators=[DataRequired()])

class FormularioTratamientoSesion(ModelForm):
    tratamiento_id = HiddenField(validators=[DataRequired()])
    sesion_id = HiddenField()  # Se asigna incremental en la ruta, no se valida en el formulario
    odontologo_id = SelectField('Odontólogo', coerce=int, validators=[DataRequired()])
    fecha = DateField('Fecha', format='%Y-%m-%d', validators=[DataRequired()])
    descripcion = TextAreaField('Descripción', validators=[DataRequired()])
    observaciones = TextAreaField('Observaciones', validators=[Optional()])
    submit = SubmitField('Guardar sesión')

    class Meta:
        model = TratamientoSesion
        include_primary_keys = True

