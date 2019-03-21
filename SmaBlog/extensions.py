from flask_sqlalchemy import SQLAlchemy
from flask_bootstrap import Bootstrap
from flask_moment import Moment
from flask_wtf.csrf import CSRFProtect
from flask_login import LoginManager,AnonymousUserMixin
from flask_pjax import PJAX
db=SQLAlchemy()
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
