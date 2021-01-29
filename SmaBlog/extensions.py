from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import MetaData
from flask_bootstrap import Bootstrap
from flask_moment import Moment
from flask_wtf.csrf import CSRFProtect
from flask_login import LoginManager,AnonymousUserMixin
from flask_pjax import PJAX
from werobot import WeRoBot
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
robot=WeRoBot(token='wmt')

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
from werobot.replies import ArticlesReply,Article
import re

@robot.text
def hello(message):
    from SmaBlog.models import SelfComment,Admin
    from flask_login import login_user
    admin=Admin.query.filter(Admin.username=='smasky').first()
    login_user(admin,remember=True)
    from flask_login import current_user
    pattern=re.compile('#\u79c1\u5bc6(.*)')
    result=re.match(pattern,message.content)
    if(result):
        Selfmessage=SelfComment(body=result.group(1),admin_id=current_user.id,secret=True)
        db.session.add(Selfmessage)
        db.session.commit()
        return result.group(1)
    else:
        Selfmessage=SelfComment(body=message.content,admin_id=current_user.id)
        db.session.add(Selfmessage)
        db.session.commit()
        return message.content
