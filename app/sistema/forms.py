from app.extensions import ModelForm
from app.models import Paciente, HistoriaAntecedentesMedicos, HistoriaExamenesEstomatologicos
from wtforms import SubmitField

class PacienteForm(ModelForm):
    class Meta:
        model = Paciente
        #exclude = ['novedades']

class AntMedForm(ModelForm):
    class Meta:
        model = HistoriaAntecedentesMedicos

class ExamenesEstomatologicosForm(ModelForm):
    class Meta:
        model = HistoriaExamenesEstomatologicos