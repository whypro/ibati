# -*- coding: utf-8 -*-
from ibati.db import sadb as db
import datetime


class JobTitle(db.Model):
    __tablename__ = 'ibati_job_title'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Unicode(20))
    order = db.Column(db.Integer)


class Member(db.Model):
    __tablename__ = 'ibati_member'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Unicode(20))
    job_title_id = db.Column(db.Integer, db.ForeignKey('ibati_job_title.id'))
    job_title = db.relationship('JobTitle', backref='members')
    intro = db.Column(db.UnicodeText)
