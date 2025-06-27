from app.extensions import ModelForm
from app.models import Paciente, HistoriaAntecedentesMedicos, HistoriaExamenesEstomatologicos, Odontologo
from wtforms import SubmitField

# Formulario para registrar un paciente. Relacionado con la entidad CCPaciente
# Este formulario permite registrar los datos básicos de un paciente, como su nombre, fecha de nacimiento, género, etc.
# Se ignora el campo novedades, ya que se maneja en otro formulario específico para novedades de pacientes.
class PacienteForm(ModelForm):
    class Meta:
        model = Paciente
        #exclude = ['novedades']
# Formulario para registrar los antecedentes médicos de un paciente. Relacionado con la entidad CCHistoriaAntecedentesMedicos
class AntMedForm(ModelForm):
    class Meta:
        model = HistoriaAntecedentesMedicos

# Formulario para registrar los exámenes estomatológicos de un paciente. Relacionado con la entidad CCHistoriaExamenesEstomatologicos
class ExamenesEstomatologicosForm(ModelForm):
    class Meta:
        model = HistoriaExamenesEstomatologicos

# Formulario para registrar un odontólogo. Relacionado con la entidad CCOdontologo
class OdontologoForm(ModelForm):
    class Meta:
        model = Odontologo