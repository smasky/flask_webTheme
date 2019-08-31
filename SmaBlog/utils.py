import datetime
from urllib.parse import urlparse, urljoin
from flask import request, redirect, url_for, current_app
from .models import itembox
from .extensions import db
def cal_days():
    start=datetime.datetime(2018,10,11)
    time_now=datetime.datetime.now()
    days_from_start=(time_now-start).days
    return days_from_start

def redirect_back(default='blog.index', **kwargs):
    for target in request.args.get('next'), request.referrer:
        if not target:
            continue
        if is_safe_url(target):
            return redirect(target)
    return redirect(url_for(default, **kwargs))

def sum_comment(posts):
    num_comments=0
    for post in posts:
        num_comments+=post.comments
    return num_comments

def loadque(filename):
    '''
        向数据库中添加试题库
    '''
    filename='SmaBlog/static/questions/'+filename+'.txt'
    with open(filename,'r') as f:
        lines=f.readlines()
    num=len(lines)
    papercode=int(lines[0].strip('\n').strip())
    queN=(num-1)/3
    lines=lines[1:]
    for i in range(int(queN)):
        question=lines[3*i].strip('\n')
        items=lines[3*i+1].strip('\n')
        right=lines[3*i+2].strip('\n')
        Que=itembox(papercode=papercode,question=question,answers=items,right=right)
        db.session.add(Que)
        db.session.commit()

