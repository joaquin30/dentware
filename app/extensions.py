from flask_sqlalchemy import SQLAlchemy
from app.models import Base
db = SQLAlchemy(model_class=Base)

from flask_wtf import FlaskForm
from wtforms_alchemy import model_form_factory

BaseModelForm = model_form_factory(FlaskForm)

class ModelForm(BaseModelForm):
    @classmethod
    def get_session(self):
        return db.session

from flask_bootstrap import Bootstrap5
bootstrap = Bootstrap5()