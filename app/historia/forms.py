from app.extensions import ModelForm
from flask_wtf import FlaskForm
from wtforms import StringField, DateField, FileField, SubmitField, HiddenField
from wtforms.validators import DataRequired
from flask_wtf.file import FileAllowed, FileRequired

class HistoriaExamenForm(FlaskForm):
    archivo = FileField('Archivo', validators=[
        FileRequired(),
        FileAllowed(['pdf', 'jpg', 'jpeg', 'png'], 'Solo archivos PDF, JPG, JPEG o PNG')
    ])
    historia_id = HiddenField(validators=[DataRequired()])
    submit = SubmitField('Subir examen')