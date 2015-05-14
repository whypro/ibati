# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from flask import Blueprint, render_template, request, redirect, url_for, abort, current_app, session, jsonify

from ibati.db import sadb as db
from ibati.models import Category, Post

admin = Blueprint('admin', __name__, url_prefix='/admin')

@admin.route('/init')
def create_all():
    db.drop_all()
    db.create_all()
    db.session.commit()
    c1 = Category(name='news', cname='新闻', order=100)
    db.session.add(c1)
    c2 = Category(name='teaching', cname='教学', order=200)
    db.session.add(c2)

    c3 = Category(name='common', cname='一般', order=100)
    c3.parent = c2
    db.session.add(c3)
    c4 = Category(name='unique', cname='特殊', order=200)
    c4.parent = c2
    db.session.add(c4)

    db.session.commit()
    return 'created'