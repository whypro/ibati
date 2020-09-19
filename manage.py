#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from ibati import create_app
from ibati import config


app = create_app(config.Config)


import subprocess
import os
import shutil

from flask.ext.script import Manager, Server
from flask.ext.migrate import Migrate, MigrateCommand

from ibati.extensions import db
from ibati.init_data import init_home, init_links, init_post
from ibati.helpers import backup as db_backup
from ibati.helpers import restore as db_restore


migrate = Migrate(app, db)

manager = Manager(app)
manager.add_command('db', MigrateCommand)
# manager.add_command('debug', Server(host='127.0.0.1', port=8080, debug=True))

@manager.command
def debug():
    """Start Server in debug mode"""
    app.run(host='0.0.0.0', port=5000, debug=True, processes=1)



@manager.command
def backup():
    # 备份上传文件
    date_str, _, _ = db_backup()
    if date_str:
        return 0
    return -1

@manager.command
def restore(date_str=None):
    if not date_str:
        files = os.listdir('backup')
        print '可以还原的备份文件有：'
        print '\n'.join(set([bf.split('-')[-1].split('.')[0] for bf in files]))
        print '请选择备份文件日期：'
        date_str = raw_input()

    db_restore(date_str)


@manager.command
def init():
    # 创建数据库
    create_db_sql = 'CREATE DATABASE IF NOT EXISTS {0} DEFAULT CHARACTER SET utf8'.format(config.Config.DB_DATABASE)
    # print create_db_sql
    ret = subprocess.call(
        [
            'mysql',
            '-h', config.Config.DB_HOST,
            '-P', str(config.Config.DB_PORT),
            '-u', config.Config.DB_USERNAME,
            '-p{0}'.format(config.Config.DB_PASSWORD),
            '-e', create_db_sql,
        ]
    )
    if not ret:
        print '数据库创建成功'
    else:
        print '数据库创建失败'
        return 

    db.drop_all()
    db.create_all()
    print '数据表创建成功'
    init_home(db.session)
    init_post(db.session)
    print '数据初始化成功'

    def clean_dir(dirname):
        for filename in os.listdir(dirname):
            path = os.path.join(dirname, filename)
            if os.path.isfile(path) or os.path.islink(path):
                os.unlink(path)
            elif os.path.isdir(path):
                shutil.rmtree(path)

    uploads_dir = config.Config.UPLOADS_DEFAULT_DEST
    # if os.path.exists(uploads_dir):
    #     shutil.rmtree(uploads_dir)
    clean_dir(uploads_dir)

    print '目录初始化成功'


if __name__ == '__main__':
    # app.run(host='0.0.0.0', port=8080, processes=10, debug=True)
    # app.run(host='0.0.0.0', port=8080, debug=True)
    manager.run()
