from flask import Flask
import logging
from logging import FileHandler, Formatter

from ibati import views
from ibati.db import sadb as db
from ibati.models import Category

def create_app(config=None):
    app = Flask(__name__)
    
    # config
    app.config.from_object(config)

    # blueprint
    app.register_blueprint(views.home)
    app.register_blueprint(views.post)
    app.register_blueprint(views.member)
    app.register_blueprint(views.admin)
    #app.register_blueprint(views.error_log)
    #app.register_blueprint(views.error_log_status)

    # database
    db.init_app(app)

    # logger
    init_app_logger(app)

    # app context
    init_app_context(app)

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


def init_app_context(app):

    @app.context_processor
    def inject_categories():
        categories = Category.query.order_by(Category.order.asc()).all()
        return dict(categories=categories)