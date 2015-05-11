from flask import Flask
import views
from db import sadb as db
import logging
from logging import FileHandler, Formatter


def create_app(config=None):
    app = Flask(__name__)
    
    # config
    app.config.from_object(config)

    # blueprint
    app.register_blueprint(views.home)
    #app.register_blueprint(views.machine)
    #app.register_blueprint(views.log)
    #app.register_blueprint(views.admin)
    #app.register_blueprint(views.error_log)
    #app.register_blueprint(views.error_log_status)

    # database
    db.init_app(app)

    # logger
    init_app_logger(app)

    return app


def init_app_logger(app):
    # logging

    file_handler = FileHandler('flask.log')

    file_handler.setFormatter(Formatter(
    '%(asctime)s %(levelname)s: %(message)s '
    '[in %(pathname)s:%(lineno)d]'
    ))

    file_handler.setLevel(logging.ERROR)
    app.logger.addHandler(file_handler)

