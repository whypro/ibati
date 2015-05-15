# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from flask import Blueprint, render_template, request, redirect, url_for, abort, current_app, session, jsonify

from ibati.db import sadb as db
from ibati.models import Category, Label, Post, JobTitle, Member


admin = Blueprint('admin', __name__, url_prefix='/admin')

@admin.route('/init')
def create_all():
    db.drop_all()
    db.create_all()
    db.session.commit()

    init_post(db.session)
    init_member(db.session)

    return 'created'


def init_post(session):
    news = Category(name='news', cname='新闻', order=100)
    session.add(news)
    dispatch = Label(name='dispatch', cname='快讯新闻', order=100, category=news)
    session.add(dispatch)

    notice = Category(name='notice', cname='通知公告', order=200)
    session.add(notice)

    report = Category(name='report', cname='学术报告', order=300)
    session.add(report)

    area = Category(name='area', cname='研究方向', order=400)
    session.add(area)

    achievement = Category(name='achievement', cname='研究成果', order=500)
    session.add(area)
    project = Label(name='project', cname='承担项目', order=100, category=achievement)
    session.add(project)
    paper = Label(name='paper', cname='文章', order=200, category=achievement)
    session.add(paper)
    patent = Label(name='patent', cname='专利', order=300, category=achievement)
    session.add(patent)

    inter_coop = Category(name='inter-coop', cname='国际合作', order=600)
    session.add(inter_coop)

    teaching = Category(name='teaching', cname='教学工作', order=700)
    session.add(teaching)

    recruitment = Category(name='recruitment', cname='研究生招生', order=800)
    session.add(recruitment)

    p1 = Post(title='今天是个好日子', content='呵呵，只是一个测试', category=news, label=dispatch)
    db.session.add(p1)

    db.session.commit()



def init_member(session):

    job_title_teacher = JobTitle(name='教师')
    session.add(job_title_teacher)

    job_title_student = JobTitle(name='学生')
    session.add(job_title_student)

    haoyuwang = Member(name='王浩宇', job_title=job_title_student, intro='西安交通大学软件学院学生')
    session.add(haoyuwang)

    session.commit()
