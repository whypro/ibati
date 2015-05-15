# -*- coding: utf-8 -*-
from ibati.db import sadb as db
import datetime


class Slider(db.Model):
    __tablename__ = 'ibati_slider'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.Unicode(50))
    subtitle = db.Column(db.Unicode(255))
    image = db.Column(db.String(255))
    order = db.Column(db.Integer)
    enable = db.Column(db.Boolean)
