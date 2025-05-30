from app.extensions import ModelForm
from flask_wtf import FlaskForm
from wtforms import StringField, DateField, BooleanField, FileField, SubmitField, HiddenField
from wtforms.validators import DataRequired
from flask_wtf.file import FileAllowed, FileRequired
from app.models import HistoriaContraindicacion
from wtforms import FieldList, FormField, TextAreaField

class HistoriaExamenForm(FlaskForm):
    archivo = FileField('Archivo', validators=[
        FileRequired(),
        FileAllowed(['pdf', 'jpg', 'jpeg', 'png'], 'Solo archivos PDF, JPG, JPEG o PNG')
    ])
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


class NovedadesForm(FlaskForm):
    novedades = TextAreaField('Novedades', validators=[DataRequired()])
    submit = SubmitField('Guardar')