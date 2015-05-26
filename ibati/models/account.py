# -*- coding: utf-8 -*-
# from __future__ import unicode_literals
from flask.ext.login import UserMixin
from ibati.extensions import db

class User(db.Model, UserMixin):
    __tablename__ = 'ibati_user'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20))
    password = db.Column(db.String(80), nullable=False)

    def __init__(self, username, password):
        self.username = username
        self.password = hashlib.md5(password).hexdigest()
