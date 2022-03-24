"""
@File    : util.py
@Software: PyCharm
@Modify Time      @Author    @Version    @Desciption
------------      -------    --------    -----------
2022/2/23 10:52  xing       1.0          request function
"""

import requests


def request_type(host, path, type, tokenStr='', bodyData=''):
    url = host + path
    if type == 'get':
        return requests.get(url, headers={'Authorization': tokenStr}).json()
    elif type == 'post':
        if tokenStr:
            return requests.post(url, headers={'Authorization': tokenStr, "Content-Type": "application/json"},
                                 json=bodyData).json()
        else:
            return requests.post(url, headers={"Content-Type": "application/json"}, json=bodyData).json()
    else:
        return

