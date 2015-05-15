# -*- coding: utf-8 -*-

class Config(object):
    SECRET_KEY = 'Institute of Biomedical Analytical Technology and Instrumentation'
    # JSON_SORT_KEY = False
    # JSONIFY_PRETTYPRINT_REGULAR = False

    # 数据库配置
    DB_HOST = 'localhost'
    DB_DATABASE = 'ibati'
    DB_USERNAME = 'root'
    DB_PASSWORD = ''
    DB_PORT = int(3306)

    # FLASK-SQLALCHEMY
    SQLALCHEMY_DATABASE_URI = 'mysql://{username}:{password}@{host}:{port}/{database}?charset=utf8'.format(
        username=DB_USERNAME, 
        password=DB_PASSWORD,
        host=DB_HOST, 
        port=DB_PORT,
        database=DB_DATABASE
    )
    # Flask-SQLAlchemy Debugging Option
    # SQLALCHEMY_ECHO = True
