import random

from faker import Faker

from .models import Post,Message
from .extensions import db

fake=Faker()

def fake_posts(count=50):
    for i in range(count):
        post=Post(title=fake.sentence(),
                  body=fake.text(2000),
                  views=fake.random_int(min=0,max=100),
                  comments=fake.random_int(min=0,max=100),
                  timestamp=fake.date_time_this_year())
        db.session.add(post)
    db.session.commit()

def fake_message(count=50):
    for i in range(count):
        message=Message(body=fake.text(50),
                        name=fake.name(),
                        timestamp=fake.date_time_this_year())
        db.session.add(message)
    db.session.commit()
