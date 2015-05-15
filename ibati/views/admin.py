# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from flask import Blueprint, render_template, request, redirect, url_for, abort, current_app, session, jsonify

from ibati.db import sadb as db
from ibati.models import Category, Label, Post

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

    l1 = Label(name='common', cname='一般', order=100)
    l1.category = c2
    db.session.add(l1)
    l2 = Label(name='unique', cname='特殊', order=200)
    l2.category = c2
    db.session.add(l2)

    p1 = Post(title='今天是个好日子', content='呵呵，只是一个测试')
    p1.category = c1
    p1.label = None
    db.session.add(p1)

    db.session.commit()
    return 'created'