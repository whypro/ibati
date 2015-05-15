#!/usr/bin/python
#  -*- coding: utf-8 -*-
from ibati import create_app


app = create_app('ibati.config')


import subprocess
import os
from flask.ext.script import Manager, Server
from flask.ext.migrate import Migrate, MigrateCommand
from ibati.db import sadb as db

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
    app.run(host='0.0.0.0', port=8080, debug=True)


if __name__ == '__main__':
    # app.run(host='0.0.0.0', port=8080, processes=10, debug=True)
    # app.run(host='0.0.0.0', port=8080, debug=True)
    manager.run()
