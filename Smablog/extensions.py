from flask_sqlalchemy import SQLAlchemy
from flask_bootstrap import Bootstrap
from flask_moment import Moment
from flask_wtf.csrf import CSRFProtect
db=SQLAlchemy()
bootstrap=Bootstrap()
moment=Moment()
csrf = CSRFProtect()
