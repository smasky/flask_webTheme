from .extensions import db
from datetime import datetime
from werkzeug.security import generate_password_hash,check_password_hash
from flask_login import UserMixin
class Post(db.Model):
    id=db.Column(db.Integer,primary_key=True)
    title=db.Column(db.String(60))
    post_img=db.Column(db.String(60))
    abstract=db.Column(db.String(60))
    body=db.Column(db.Text)
    views=db.Column(db.Integer)
    comments=db.Column(db.Integer)
    timestamp=db.Column(db.DateTime,default=datetime.utcnow,index=True)

class Message(db.Model):
    id=db.Column(db.Integer,primary_key=True)
    body=db.Column(db.String(200))
    name=db.Column(db.String(20))
    timestamp=db.Column(db.DateTime,default=datetime.utcnow,index=True)

class Admin(db.Model,UserMixin):
    id=db.Column(db.Integer,primary_key=True)
    username=db.Column(db.String(20))
    password_hash=db.Column(db.String(128))
    email=db.Column(db.String(30),unique=True)
    avater=db.Column(db.String(128),default="{{ url_for( 'static',filename='img/comment.png' ) }}")
    right=db.Column(db.Integer)

    def set_password(self,password):
        self.password_hash=generate_password_hash(password)

    def validate_password(self,password):
        return check_password_hash(self.password_hash,password)

    @property
    def password(self):
        raise AttributeError(u'此属性不可读')

    @password.setter
    def password(self,password):
        self.password_hash=generate_password_hash(password)
