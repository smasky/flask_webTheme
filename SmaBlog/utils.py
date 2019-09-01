import datetime
from urllib.parse import urlparse, urljoin
from flask import request, redirect, url_for, current_app

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
    from .models import Itembox,Paperday
    filename='SmaBlog/static/questions/'+filename+'.txt'
    with open(filename,'r') as f:
        lines=f.readlines()
    num=len(lines)
    papercode=int(lines[0].strip('\n').strip())
    queN=(num-1)/3
    lines=lines[1:]
    paperday=Paperday.query.filter(Paperday.paperdaycode==papercode).first()
    if(not paperday):
        paperday=Paperday(paperdaycode=papercode)
        db.session.add(paperday)
        db.session.commit()
    for i in range(int(queN)):
        question=lines[3*i].strip('\n')
        items=lines[3*i+1].strip('\n')
        right=lines[3*i+2].strip('\n')
        Que=Itembox(papercode=papercode,question=question,answers=items,right=right,paperday_id=paperday.id)
        db.session.add(Que)
        db.session.commit()
def encrypt(key, s):
    b = bytearray(str(s).encode("utf-8"))
    n = len(b)
    c = bytearray(n*2)
    j = 0
    for i in range(0, n):
        b1 = b[i]
        b2 = b1 ^ key
        c1 = b2 % 19
        c2 = b2 // 19
        c1 = c1 + 46
        c2 = c2 + 46
        c[j] = c1
        c[j+1] = c2
        j = j+2
    return c.decode("utf-8")
def decrypt(ksa, s):
    c = bytearray(str(s).encode("utf-8"))
    n = len(c)
    if n % 2 != 0:
        return ""
    n = n // 2
    b = bytearray(n)
    j = 0
    for i in range(0, n):
        c1 = c[j]
        c2 = c[j + 1]
        j = j + 2
        c1 = c1 - 46
        c2 = c2 - 46
        b2 = c2 * 19 + c1
        b1 = b2 ^ ksa
        b[i] = b1
    return b.decode("utf-8")

