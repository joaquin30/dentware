from app.extensions import ModelForm
from app.models import Paciente


class PacienteForm(ModelForm):
    class Meta:
        model = Paciente
        exclude = ['novedades']
        include_primary_keys = True