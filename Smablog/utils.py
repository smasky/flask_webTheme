import datetime
from urllib.parse import urlparse, urljoin
from flask import request, redirect, url_for, current_app
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
