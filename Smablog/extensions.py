from flask_sqlalchemy import SQLAlchemy
from flask_bootstrap import Bootstrap
from flask_moment import Moment
from flask_wtf.csrf import CSRFProtect
from flask_login import LoginManager

db=SQLAlchemy()
bootstrap=Bootstrap()
moment=Moment()
csrf = CSRFProtect()
login=LoginManager()

@login.user_loader
def load_user(user_id):
    from .models import Admin
    user=Admin.query.get(int(user_id))
    return user
