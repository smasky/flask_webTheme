from .extensions import db
from datetime import datetime
from werkzeug.security import generate_password_hash,check_password_hash
from flask_login import UserMixin
class Post(db.Model):
    id=db.Column(db.Integer,primary_key=True)
    title=db.Column(db.String(60))
    post_img=db.Column(db.String(60))
    abstract=db.Column(db.String(60))
    url=db.Column(db.String(60))
    body=db.Column(db.Text)
    views=db.Column(db.Integer)
    timestamp=db.Column(db.DateTime,default=datetime.utcnow,index=True)
    comments=db.Column(db.Integer,default=0)
    postcomments=db.relationship('PostComment',back_populates='post',cascade='all')
    
class Music(db.Model):
    id=db.Column(db.Integer,primary_key=True)
    name=db.Column(db.String(20))
    artist=db.Column(db.String(20))
    url=db.Column(db.String(20))

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
class SelfComment(db.Model):
    id=db.Column(db.Integer,primary_key=True)
    body=db.Column(db.String(200))
    timestamp=db.Column(db.DateTime,default=datetime.utcnow,index=True)
    secret=db.Column(db.Boolean,default=False)
    admin_id=db.Column(db.Integer,db.ForeignKey('admin.id'))
    admin=db.relationship('Admin',back_populates='selfcomments')
'''
微信部分数据库
'''
class Itembox(db.Model):
    id=db.Column(db.Integer,primary_key=True)
    papercode=db.Column(db.Integer)
    question=db.Column(db.String)
    answers=db.Column(db.String)#ssss\sss\sss\sss
    right=db.Column(db.String)
    paperday_id=db.Column(db.Integer,db.ForeignKey('paperday.id'))
    paperday=db.relationship('Paperday',back_populates='itemboxs')
    dati=db.relationship('Dati',back_populates='itembox')
class Paperday(db.Model):
    id=db.Column(db.Integer,primary_key=True)
    paperdaycode=db.Column(db.Integer,unique=True)
    content=db.Column(db.String)
    weiitems=db.relationship('Weiitem',back_populates='paperday')
    itemboxs=db.relationship('Itembox',back_populates='paperday')
class Dati(db.Model):
    id=db.Column(db.Integer,primary_key=True)
    itembox_id=db.Column(db.Integer,db.ForeignKey('itembox.id'))
    itembox=db.relationship('Itembox',back_populates='dati')
    right=db.Column(db.Boolean)
    answer=db.Column(db.String)
    weiitem_id=db.Column(db.Integer,db.ForeignKey('weiitem.id'))
    weiitem=db.relationship('Weiitem',back_populates='datis')
    
class Weiadmin(db.Model):
    id=db.Column(db.Integer,primary_key=True)
    openid=db.Column(db.String,unique=True)
    truename=db.Column(db.String)
    username=db.Column(db.String)
    year=db.Column(db.String)
    ifstudent=db.Column(db.Boolean)
    weiitems=db.relationship('Weiitem',back_populates='weiadmin')
class Weiitem(db.Model):
    id=db.Column(db.Integer,primary_key=True)
    weiadmin_id=db.Column(db.Integer,db.ForeignKey('weiadmin.id'))
    weiadmin=db.relationship('Weiadmin',back_populates='weiitems')
    paperday_id=db.Column(db.Integer,db.ForeignKey('paperday.id'))
    paperday=db.relationship('Paperday',back_populates='weiitems')
    datis=db.relationship('Dati',back_populates='weiitem')
    rank=db.Column(db.Integer)
    answers=db.Column(db.String)
'''
'''
class Admin(db.Model,UserMixin):
    id=db.Column(db.Integer,primary_key=True)
    name=db.Column(db.String(20))
    web=db.Column(db.String,default='#')
    username=db.Column(db.String(20),unique=True)
    password_hash=db.Column(db.String(128))
    email=db.Column(db.String(30),unique=True)
    avater=db.Column(db.String(128),default="https://ws1.sinaimg.cn/large/007G9tRkgy1g15xb7y323j3074074q3a.jpg")
    right=db.Column(db.Integer,default=3)
    selfcomments=db.relationship('SelfComment',back_populates='admin')
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

    def test_right(self):
        if(self.right==1):
            return True
        return False
    def can(self):
        return True
