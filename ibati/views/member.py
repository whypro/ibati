# -*- coding: utf-8 -*-

from flask import Blueprint, render_template, request, jsonify, redirect, url_for, abort
from ibati.models import JobTitle, Member

member = Blueprint('member', __name__, url_prefix='/member')

@member.route('/')
@member.route('/<job_title>/')
def index(job_title=None):
    job_titles = JobTitle.query.all()
    qry = Member.query
    if job_title:
        jt = JobTitle.query.filter_by(name=job_title).one()
        qry = qry.filter_by(job_title_id=jt.id)
    members = qry.all()
    return render_template(
        'member/members.html', 
        active='member', job_title_active=job_title, job_titles=job_titles, members=members
    )

@member.route('/<int:id>/')
def detail(id):
    return render_template('member/member-detail.html', active='member')
