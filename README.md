
### Nginx 配置文件

    upstream ibati {
        server 127.0.0.1:8000 fail_timeout=0;
        #server unix:/var/run/ibati.sock fail_timeout=0;
    }

    server {
        listen       80;
        server_name  ibati.hy;

        #access_log  logs/host.access.log  main;

        root   /home/whypro/codes/IBATI;

        location / {
            try_files $uri @proxy_to_app;
        }

        location @proxy_to_app {
            proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
            proxy_set_header Host $http_host;
            proxy_set_header X-Forwarded-Proto $scheme;
            proxy_redirect off;
            proxy_pass http://ibati;
        }

        # redirect server error pages to the static page /50x.html
        error_page   500 502 503 504  /50x.html;
        location = /50x.html {
            root   /usr/share/nginx/html;
        }
    }

### 安装

* python2.7+
* virtualenv
* supervisor


    $ virtualenv venv
    $ source venv/bin/activate
    (venv)$ pip install -r requirements.txt
    (venv)$ python manage.py init

### 运行
    $ supervisord -c etc/supervisord.conf