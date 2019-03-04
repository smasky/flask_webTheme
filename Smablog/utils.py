import datetime

def cal_days():
    start=datetime.datetime(2018,10,11)
    time_now=datetime.datetime.now()
    days_from_start=(time_now-start).days
    return days_from_start
