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
    timestamp=db.Column(db.DateTime,default=datetime.utcnow,index=True)
    comments=db.Column(db.Integer,default=0)
    postcomments=db.relationship('PostComment',back_populates='post',cascade='all')

class Message(db.Model):
    id=db.Column(db.Integer,primary_key=True)
    body=db.Column(db.String(200))
    timestamp=db.Column(db.DateTime,default=datetime.utcnow,index=True)
    admin_id=db.Column(db.Integer,db.ForeignKey('admin.id'))
    admin=db.relationship('Admin',back_populates='messages')

class PostComment(db.Model):
    id=db.Column(db.Integer,primary_key=True)
    body=db.Column(db.String(200))
    timestamp=db.Column(db.DateTime,default=datetime.utcnow,index=True)
    post_id=db.Column(db.Integer,db.ForeignKey('post.id')) #与表post建立联系
    admin_id=db.Column(db.Integer,db.ForeignKey('admin.id'))
    admin=db.relationship('Admin',back_populates='postcomments')
    post=db.relationship('Post',back_populates='postcomments')

    #admin_id=db.Column(db.Integer,db.ForeignKey('admin.id')) #与表admin建立联系
    #admin=db.relationship('Admin'.back_populates='postcomments') 暂时先不和用户表连接
class Admin(db.Model,UserMixin):
    id=db.Column(db.Integer,primary_key=True)
    name=db.Column(db.String(20))
    web=db.Column(db.String,default='#')
    username=db.Column(db.String(20),unique=True)
    password_hash=db.Column(db.String(128))
    email=db.Column(db.String(30),unique=True)
    avater=db.Column(db.String(128),default="https://ws1.sinaimg.cn/large/007G9tRkgy1g15xb7y323j3074074q3a.jpg")
    right=db.Column(db.Integer,default=3)
    messages=db.relationship('Message',back_populates='admin')   #与表message建立联系
    postcomments=db.relationship('PostComment',back_populates='admin') #与表postcomment建立联系

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

    def can(self):
        return True
