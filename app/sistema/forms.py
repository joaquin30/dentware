from app.extensions import ModelForm
from app.models import Paciente, HistoriaAntecedentesMedicos
from wtforms import SubmitField

class PacienteForm(ModelForm):
    class Meta:
        model = Paciente
        exclude = ['novedades']
        include_primary_keys = True

class AntMedForm(ModelForm):
    class Meta:
        model = HistoriaAntecedentesMedicos