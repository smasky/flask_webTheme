from .models import Post
from .extensions import db
import time
import datetime
import markdown
from faker import Faker
fake=Faker()

def loading_post(filename=''):
    print('bb')
    if(filename):
        Cfilename='static/post/'+filename
        Info={}
        content=[]
        with open(Cfilename,'r',encoding='utf-8') as f:
            is_info=False
            is_zw=False
            n=0
            for line in f:
                n+=1
                if(is_zw):
                    content.append(line)
                if('@-' in line):
                    is_info=not is_info
                    if(not is_info):
                        is_zw=True
                if(is_info and n>1):
                    info=line.strip('\n').split('::')
                    Info[info[0]]=info[1]
        html=markdown.markdown(''.join(content))

        post=Post(title=Info['title'],
                    body=html,
                    views=0,
                    post_img=Info['top_img'],
                    abstract=Info['abstract'],
                    comments=0,
                    timestamp=datetime.datetime.utcnow())
        print('aa')
        db.session.add(post)
        db.session.commit()
