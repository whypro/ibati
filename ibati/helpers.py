# -*- coding: utf-8 -*-
from flask import request, current_app


def get_client_ip():
    # 获取 ip 地址
    if 'x-forwarded-for' in request.headers:
        ip = request.headers['x-forwarded-for'].split(', ')[0]
    else:
        ip = request.remote_addr
    return ip


# 取样
# slice step，因为数据量可能过大，因此设置一个步长来减少返回的数据量
def sample(data):
    if current_app.config['DISABLE_SAMPLE']:
        return data
    step = int(len(data) / current_app.config['SAMPLE_POINT'])
    if step == 0: step = 1
    new_data = data[::step]
    return new_data





