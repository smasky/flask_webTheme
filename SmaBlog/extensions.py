from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import MetaData
from flask_bootstrap import Bootstrap
from flask_moment import Moment
from flask_wtf.csrf import CSRFProtect
from flask_login import LoginManager,AnonymousUserMixin
from flask_pjax import PJAX
naming_convention = {
    "ix": 'ix_%(column_0_label)s',
    "uq": "uq_%(table_name)s_%(column_0_name)s",
    "ck": "ck_%(table_name)s_%(column_0_name)s",
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
    "pk": "pk_%(table_name)s"
}
db=SQLAlchemy(metadata=MetaData(naming_convention=naming_convention))
bootstrap=Bootstrap()
moment=Moment()
csrf = CSRFProtect()
login=LoginManager()
pjax=PJAX()

@login.user_loader
def load_user(user_id):
    from .models import Admin
    user=Admin.query.get(int(user_id))
    return user

class Guest(AnonymousUserMixin):
    def can(self):
        return False
    def test_right(self):
        return False
