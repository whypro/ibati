# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from flask import Blueprint, render_template, request, redirect, url_for, abort, current_app, session, jsonify

from ibati.db import sadb as db
from ibati.models import Category, Label, Post, JobTitle, Member, Slider


admin = Blueprint('admin', __name__, url_prefix='/admin')


@admin.route('/')
def index():
    return render_template('admin/index.html')


@admin.route('/init/')
def create_all():
    db.drop_all()
    db.create_all()
    db.session.commit()

    init_post(db.session)
    init_member(db.session)
    init_home(db.session)

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
    teacher = JobTitle(name='教师')
    session.add(teacher)

    student = JobTitle(name='学生')
    session.add(student)

    zhaolinger = Member(name='赵灵儿', job_title=student, intro='西安交通大学软件学院学生', photo='uploads/200800000006.jpg')
    session.add(zhaolinger)
    linyueru = Member(name='林月如', job_title=student, intro='西安交通大学软件学院学生', photo='uploads/200800000012.jpg')
    session.add(linyueru)
    anu = Member(name='阿奴', job_title=student, intro='西安交通大学软件学院学生', photo='uploads/200800000020.jpg')
    session.add(anu)
    wuhou = Member(name='巫后', job_title=teacher, intro='西安交通大学软件学院老师', photo='uploads/200800000123.jpg')
    session.add(wuhou)

    session.commit()


def init_home(session):
    slider_1 = Slider(
        title='心肌细胞实验',
        subtitle='心肌细胞电学特性和力学特性就耦合起来。但由于心血管疾病会改变力学或电学特性，因此这就很有研究的价值。',
        image='img/demo/20134210431480357.jpg', order=100, enable=True
    )
    session.add(slider_1)

    slider_2 = Slider(
        title='皮肤热疼痛实验',
        subtitle='我们团队首次发现热刺激下组织的疼痛水平不仅取决于温度变化，而且受温度变化诱发的热应力的影响，力学因素在组织疼痛中发挥着关键作用，由此建立了热-力-电（疼痛）多场耦合行为理论，为有效指导激光、微波等临床热疗技术及镇痛方案提供了理论依据。',
        image='img/demo/201342121154745276.png', order=200, enable=True
    )
    session.add(slider_2)

    session.commit()

