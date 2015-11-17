# -*- coding: utf-8 -*-
from __future__ import unicode_literals, division
from zipfile import ZipFile, ZIP_DEFLATED
import datetime
import subprocess
import os
import math

from flask import request, current_app

from . import config
from .extensions import db

def get_client_ip():
    # 获取 ip 地址
    if 'x-forwarded-for' in request.headers:
        ip = request.headers['x-forwarded-for'].split(', ')[0]
    else:
        ip = request.remote_addr
    return ip


def backup():
    date_str = datetime.datetime.now().strftime('%Y%m%d%H%M%S')
    zip_file = 'backup/ibati-{date}.zip'.format(date=date_str)
    if not os.path.exists('backup'):
        os.makedirs('backup')

    # 备份数据库
    sql_file = 'backup/ibati-{date}.sql'.format(date=date_str)
    with open(sql_file, 'w') as f:
        ret = subprocess.call(
            [
                'mysqldump', '-u', config.Config.DB_USERNAME,
                '-p{0}'.format(config.Config.DB_PASSWORD),
                config.Config.DB_DATABASE,
            ],
            stdout=f
        )
    if not ret:
        current_app.logger.error('数据库备份成功')
    else:
        os.remove(sql_file)
        current_app.logger.error('数据库备份失败')
        return None

    # 生成压缩包
    with ZipFile(zip_file, 'w', compression=ZIP_DEFLATED) as zf:
        uploads_dir = os.path.relpath(current_app.config['UPLOADS_DEFAULT_DEST'], current_app.config['APP_DIR'])
        for root, dirs, files in os.walk(uploads_dir):
            # print root, dirs, files
            for f in files:
                zf.write(os.path.join(root, f))

        zf.write(sql_file, arcname=os.path.basename(sql_file))

    os.remove(sql_file)

    current_app.logger.error('数据已备份至 {0}'.format(zip_file))

    return date_str, zip_file, os.path.getsize(zip_file)


def restore(date_str):
    zip_file = 'backup/ibati-{date}.zip'.format(date=date_str)
    sql_file = 'ibati-{date}.sql'.format(date=date_str)

    # 还原上传文件
    with ZipFile(zip_file, 'r') as zf:
        zf.extractall()
    current_app.logger.error('文件已还原')

    # 还原数据库
    with open(sql_file, 'r') as f:
        ret = subprocess.call(
            [
                'mysql', '-u', config.Config.DB_USERNAME,
                '-p{0}'.format(config.Config.DB_PASSWORD),
                config.Config.DB_DATABASE,
            ],
            stdin=f
        )
    if not ret:
        current_app.logger.error('数据库还原成功')
    else:
        current_app.logger.error('数据库还原失败')
    os.remove(sql_file)


def human_readable_size(size):
    unit = 1024
    if size < unit: return str(size) + ' B'
    exp = int(math.log(size) / math.log(unit))
    pre = 'KMGTPE'[exp-1]
    return '{0:.2f} {1}'.format(size / math.pow(unit, exp), pre)
