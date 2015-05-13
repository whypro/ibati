# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from flask import Blueprint, render_template, request, redirect, url_for, abort, current_app, session, jsonify

from ibati.db import sadb as db


admin = Blueprint('admin', __name__, url_prefix='/admin')

@admin.route('/init')
def create_all():
    db.create_all()
    db.session.commit()
    return 'created'