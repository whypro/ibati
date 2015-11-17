# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import datetime

from ..extensions import db


class Backup(db.Model):
    __tablename__ = 'ibati_backup'

    id = db.Column(db.Integer, primary_key=True)
    date_str = db.Column(db.String(14), nullable=False)
    zip_file = db.Column(db.String(255))
    size = db.Column(db.Integer)
