# coding: utf-8

import gevent.monkey
gevent.monkey.patch_all()
import multiprocessing

#bind = 'unix:/var/run/ibati.sock'
bind = '0.0.0.0:8000'
max_requests = 100
keepalive = 5

workers = multiprocessing.cpu_count() * 2 + 1
worker_class = 'gunicorn.workers.ggevent.GeventWorker'

loglevel = 'info'
errorlog = '-'

x_forwarded_for_header = 'X-FORWARDED-FOR'

secure_scheme_headers = {
    'X-SCHEME': 'https',
}
