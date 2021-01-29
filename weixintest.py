import requests
import os

def get_token():
    payload_access_token = {
        'grant_type': 'client_credential',
        'appid': 'wx343fe184128a8bf4',
        'secret': 'b1d45901ca12ec9ee6ea3f44ee507139'
    }
    token_url = 'https://api.weixin.qq.com/cgi-bin/token'
    r = requests.get(token_url, params=payload_access_token)
    dict_result = (r.json())
    return dict_result['access_token']


def get_user():
    payload_user = {
        'access_token': get_token(),
    }
    token_url = 'https://api.weixin.qq.com/cgi-bin/user/get'
    r = requests.get(token_url, params=payload_user)
    dict_result = (r.json())
    return dict_result

def get_media_ID(path):
    img_url = 'https://api.weixin.qq.com/cgi-bin/media/upload'
    payload_img = {
        'access_token': get_token(),
        'type': 'image'
    }
    rr=requests.get(path)
    with open('img.png', 'wb') as f:
        f.write(rr.content)
    f = open('img.png', 'rb')
    data = {'media': f}
    r = requests.post(url=img_url, params=payload_img, files=data)
    f.close()
    dict = r.json()
    return dict['media_id']


