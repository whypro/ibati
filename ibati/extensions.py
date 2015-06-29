from flask import g, current_app
from flask.ext.sqlalchemy import SQLAlchemy
from MySQLdb import connect

db = SQLAlchemy()


from flask.ext.uploads import UploadSet, IMAGES, DOCUMENTS

upload_set = UploadSet(name='files', extensions=IMAGES+DOCUMENTS)
