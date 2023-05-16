# -*- coding: utf-8 -*-
"""
Created on Wed Apr 26 18:40:51 2023

@author: Erlend
"""

# This code runs on Python 2.7.x and Python 3.x.
# You may install `requests` to run this code: pip install requests
# api document:https://api.fanyi.baidu.com/doc/21

import requests
import random
# import json
from hashlib import md5


def baidu_translate_api(from_lang, to_lang, query):
    from_lang = from_lang
    to_lang = to_lang
    query = query

    # Set your own appid/appkey.
    appid = 'you id'
    appkey = 'you key'
    endpoint = 'http://api.fanyi.baidu.com'
    path = '/api/trans/vip/translate'
    url = endpoint + path

    salt = random.randint(32768, 65536)
    sign = make_md5(appid + query + str(salt) + appkey)

    # Build request
    headers = {'Content-Type': 'application/x-www-form-urlencoded'}
    payload = {'appid': appid,
               'q': query,
               'from': from_lang,
               'to': to_lang,
               'salt': salt,
               'sign': sign}
    # Send request
    r = requests.post(url, params=payload, headers=headers)
    result = r.json()
    print(result)
    # # Show response
    # print(json.dumps(result, indent=4, ensure_ascii=False))
    return result


# Generate salt and sign
def make_md5(s, encoding='utf-8'):
    return md5(s.encode(encoding)).hexdigest()
