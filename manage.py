#!/usr/bin/python
#  -*- coding: utf-8 -*-
from __future__ import unicode_literals
from ibati import create_app
from ibati import config

app = create_app(config.Config)


import subprocess
import os
import datetime
import shutil
from zipfile import ZipFile

from flask.ext.script import Manager, Server
from flask.ext.migrate import Migrate, MigrateCommand

from ibati.extensions import db
from ibati.init_data import init_home, init_links, init_member, init_post

migrate = Migrate(app, db)

manager = Manager(app)
manager.add_command('db', MigrateCommand)
# manager.add_command('debug', Server(host='127.0.0.1', port=8080, debug=True))


def get_pid():
    gunicorn_pid = None
    if os.path.exists('/tmp/gunicorn.pid'):
        f = open('/tmp/gunicorn.pid', 'r')
        pid = f.readline().strip()
        if pid:
            p = subprocess.Popen(['ps', 'h', pid], stdout=subprocess.PIPE)
            pro, err = p.communicate()
            if pro:
                gunicorn_pid = int(pid)
    return gunicorn_pid


@manager.command
def stop():
    """Stop server"""
    pid = get_pid()
    if pid is None:
        print 'ibati is not running.'
        return False
    subprocess.call(['kill', str(pid)])
    return True


@manager.command
def start():
    """Start server by gunicorn"""
    if get_pid() is not None:
        print 'ibati is running.'
        return False
    print subprocess.call('source venv/bin/activate', shell=True)
    subprocess.call('./gunicorn.sh', shell=True)
    return True


@manager.command
def pid():
    """Show pid"""
    print get_pid()


@manager.command
def debug():
    """Start Server in debug mode"""
    if get_pid() is not None:
        print 'ibati is running.'
        return False
    app.run(host='0.0.0.0', port=5000, debug=True, processes=1)


@manager.command
def backup():
    # 备份上传文件
    date_str = datetime.datetime.now().strftime('%Y%m%d%H%M%S')
    ret = shutil.make_archive('backup/uploads-{date}'.format(date=date_str), 'zip', './', 'uploads')
    print '文件已备份至 {0}'.format(ret)
    # print ret

    # 备份数据库
    sql_file = 'backup/ibati-{date}.sql'.format(date=date_str)
    f = open(sql_file, 'w')
    ret = subprocess.call(
        [
            'mysqldump', '-u', config.Config.DB_USERNAME,
            '-p{0}'.format(config.Config.DB_PASSWORD),
            config.Config.DB_DATABASE,
        ],
        stdout=f
    )
    f.close()
    if not ret:
        print '数据库已备份至 {0}'.format(os.path.abspath(sql_file))
    else:
        os.remove(sql_file)
        print '数据库备份失败'


@manager.command
def restore():
    files = os.listdir('backup')
    print '可以还原的备份文件有：'
    print '\n'.join(set([bf.split('-')[-1].split('.')[0] for bf in files]))
    print '请选择备份文件日期：'
    date_str = raw_input()

    # 还原数据库
    f = open('backup/ibati-{date}.sql'.format(date=date_str), 'r')
    ret = subprocess.call(
        [
            'mysql', '-u', config.Config.DB_USERNAME,
            '-p{0}'.format(config.Config.DB_PASSWORD),
            config.Config.DB_DATABASE,
        ],
        stdin=f
    )
    f.close()
    if not ret:
        print '数据库已还原'
    else:
        print '数据库还原失败'

    # 还原上传文件
    with ZipFile('backup/uploads-{date}.zip'.format(date=date_str), 'r') as z:
        z.extractall()
    print '文件已还原'


@manager.command
def init():
    db.drop_all()
    db.create_all()
    init_home(db.session)
    init_post(db.session)
    init_member(db.session)

    uploads_dir = config.Config.UPLOADS_DEFAULT_DEST
    if os.path.exists(uploads_dir):
        shutil.rmtree(uploads_dir)


if __name__ == '__main__':
    # app.run(host='0.0.0.0', port=8080, processes=10, debug=True)
    # app.run(host='0.0.0.0', port=8080, debug=True)
    manager.run()
