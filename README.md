# IBATI

## 安装与部署

下面以本人的 Arch Linux 为例，描述一下安装部署的步骤。  
**注意：所有相对路径都是相对于 IBATI 目录，因此在每一步输入命令前，请确认您已切换到了 IBATI 目录。**

* 安装 gcc

        # pacman -S gcc

* 安装 mysql/mariadb

        # pacman -S mariadb

    初始化 mysql，请注意修改 MySQL root 用户密码：

        # mysql_install_db --user=mysql --basedir=/usr --datadir=/var/lib/mysql
        # mysql_secure_installation

    运行 mysql 并设为开机启动：

        # systemctl start mysqld
        # systemctl enable mysqld

* 安装 python2 与 pip

        # pacman -S python2
        # pacman -S python2-pip

* 安装 virtualenv

        # pip install virtualenv

* 创建虚拟环境并安装第三方依赖

        $ virtualenv venv
        $ source venv/bin/activate
        (venv)$ pip install -r requirements.txt
        (venv)$ deactivate
        
    如果这一步报错，请安装 python-devel 和 mysql-devel

* 修改 ibati/config.py

    按照实际环境设置 MySQL 连接：

        DB_HOST = 'localhost'       # MySQL 服务器地址
        DB_DATABASE = 'ibati'       # MySQL 数据库名称
        DB_USERNAME = 'root'        # MySQL 用户名称
        DB_PASSWORD = 'whypro'      # MySQL 用户密码
        DB_PORT = 3306              # MySQL 端口号


* 初始化

        $ source venv/bin/activate
        (venv)$ python manage.py init
        (venv)$ deactivate

    在这一步需要设置管理员用户名和密码。

* 安装 nginx

        # pacman -S nginx

    创建配置文件：

        # mkdir /etc/nginx/vhosts.d
        # vim /etc/nginx/vhosts.d/ibati.conf

    将下面内容复制到 ibati.conf，请注意 server_name 和 root 选项。

        upstream ibati {
            server 127.0.0.1:8000 fail_timeout=0;
            #server unix:/var/run/ibati.sock fail_timeout=0;
        }
    
        server {
            listen       80;
            server_name  ibati.hy;  # your server name
    
            #access_log  logs/host.access.log  main;
    
            root   /home/whypro/codes/IBATI;    # your root directory
    
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

    编辑 nginx.conf

        # vim /etc/nginx/nginx.conf

    注释掉 server 中所有选项，并在 http 选项结尾加入 include vhosts.d/*.conf;：

        http {
            ...
            include vhosts.d/*.conf;
        }

    运行 nginx 并设置为开机启动：

        # systemctl start nginx
        # systemctl enable nginx

* 安装 supervisor

        # pip install supervisor

    编辑 etc/supervisord.conf，修改其中的管理员用户名和密码，以及访问端口（如果必要）：

        [inet_http_server]
        port=0.0.0.0:9001   ; 监听 IP 和端口
        username=whypro     ; 管理员用户名
        password=whypro     ; 管理员密码
    
    启动守护进程：

        $ supervisord -c etc/supervisord.conf

    访问 http://[your_ip]:9001 管理（启动，停止，重启） Web 服务器。

* 部署完成

    访问 http://[your_ip] 浏览吧！

## 备份与还原

* 备份
		
		$ source venv/bin/activate
    	$ ./manage.py backup
		$ deactivate

	文件会备份至 backup 目录，请定期将其拷贝至安全的地方。

* 还原

		$ source venv/bin/activate
    	$ ./manage.py restore
		$ deactivate

    之后会显示出可以还原的备份文件列表，输入备份文件名后，便可恢复到指定日期。

## 调试

	在一些情况下需要调试服务器时，可以使用：

	$ source venv/bin/activate
	$ ./manage.py debug

