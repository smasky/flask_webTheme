from .extensions import db
from datetime import datetime

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
