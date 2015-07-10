## 部署

    $ virtualenv venv
    $ source venv/bin/activate
    (venv)$ pip install -r requirements.txt
    (venv)$ python manage.py init


    $ supervisord -c etc/supervisord.conf
