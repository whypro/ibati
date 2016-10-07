from flask import g, current_app
from flask.ext.sqlalchemy import SQLAlchemy
from MySQLdb import connect

db = SQLAlchemy()

from flask.ext.uploads import UploadSet, IMAGES, DOCUMENTS


class UniqueUploadSet(UploadSet):

    def resolve_conflict(self, target_folder, basename):
        # do not resolve conflict
        return basename

upload_set = UniqueUploadSet(name='files', extensions=IMAGES+DOCUMENTS)
