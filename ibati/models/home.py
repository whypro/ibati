# -*- coding: utf-8 -*-
import datetime

from ..extensions import db


class Slider(db.Model):
    __tablename__ = 'ibati_slider'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.Unicode(50))
    subtitle = db.Column(db.Unicode(255))
    image = db.Column(db.String(255))
    order = db.Column(db.Integer)
    enable = db.Column(db.Boolean)


class Link(db.Model):
    __tablename__ = 'ibati_link'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Unicode(100))
    href = db.Column(db.String(255))
    order = db.Column(db.Integer)


class Advertisement(db.Model):
    __tablename__ = 'ibati_advertisement'

    id = db.Column(db.Integer, primary_key=True)
    url = db.Column(db.String(255), default='')
    image = db.Column(db.String(255), default='')
    enable = db.Column(db.Boolean)
    type = db.Column(db.String(50))
