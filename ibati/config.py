# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import os


class Config(object):
    SECRET_KEY = 'Institute of Biomedical Analytical Technology and Instrumentation'
    # JSON_SORT_KEY = False
    # JSONIFY_PRETTYPRINT_REGULAR = False

    # 数据库配置
    DB_HOST = 'localhost'
    DB_DATABASE = 'ibati'
    DB_USERNAME = 'root'
    DB_PASSWORD = 'whypro'
    DB_PORT = 3306

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

    # Flask-Uploads
    UPLOADS_DEFAULT_DEST = os.path.realpath('uploads')
    UPLOADED_FILES_ALLOW = ['pdf']

    POSTS_PER_PAGE = 10     # 每页显示的主题数
    INDEX_NEWS_NUM = 6      # 首页新闻个数
    INDEX_AREA_NUM = 8     # 首页研究方向个数

    APP_DIR = os.path.realpath('.')
