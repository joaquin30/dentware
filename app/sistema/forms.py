from app.extensions import ModelForm
from app.models import Paciente
from wtforms import SubmitField

class PacienteForm(ModelForm):
    class Meta:
        model = Paciente
        exclude = ['novedades']
        include_primary_keys = True