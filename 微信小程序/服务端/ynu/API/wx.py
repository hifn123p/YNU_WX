from urllib import request
import json


def open_id(code):
    url2 = 'https://api.weixin.qq.com/sns/jscode2session?appid='
    APPID = 'wx94a7d3260f54d4ad'
    SECRET = '3e1c9792f049f67c1ca5b496e1bf02de'
    url = url2 + APPID + '&secret=' + SECRET + '&js_code=' + code + '&grant_type=authorization_code'
    res = request.urlopen(url)
    data = res.read().decode()
    js = json.loads(data)
    openid = js.get('openid')
    return openid
