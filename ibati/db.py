from flask import g, current_app
from flask.ext.sqlalchemy import SQLAlchemy
from MySQLdb import connect


sadb = SQLAlchemy()