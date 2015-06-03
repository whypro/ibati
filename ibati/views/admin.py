# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import hashlib
import datetime
import re
import os
from PIL import Image

from flask import Blueprint, render_template, request, redirect, url_for, abort, current_app, session, jsonify
from flask.ext.login import login_user, logout_user, login_required, current_user

from ibati.extensions import db, upload_set
from ibati.models import Category, Label, Post, JobTitle, Member, Slider, User


admin = Blueprint('admin', __name__, url_prefix='/admin')


@admin.route('/')
@login_required
def index():
    return render_template('admin/index.html')


@admin.route('/upload/', methods=['POST'])
@login_required
def upload():
    # print request.form
    # rint request.files['imgFile']
    if 'imgFile' in request.files:
        # TODO: 应该压缩一下图片
        file_storage = request.files['imgFile']
        basename = hashlib.sha1(file_storage.read()).hexdigest()+os.path.splitext(file_storage.filename)[1]
        file_storage.seek(0)
        filename = upload_set.save(file_storage, name=basename)
        # print upload_set.path(filename)
        # print upload_set.url(filename)
        return jsonify(error=0, url=upload_set.url(filename))
    return jsonify(error=1, message='upload failed')


@admin.route('/login/', methods=['GET', 'POST'])
def login():
    # 已登录用户则返回首页
    if current_user.is_authenticated():
        return redirect(url_for('home.index'))

    if request.method == 'POST':
        if 'username' in request.form and 'password' in request.form:
            user = User.query.filter_by(
                username=request.form['username'],
                password=hashlib.md5(request.form['password']).hexdigest()
            ).first()
            if user:
                login_user(user)
                return redirect(url_for('home.index'))
    return render_template('admin/login.html')


@admin.route('/logout/')
@login_required
def logout():
    logout_user()
    return redirect(url_for('home.index'))


@admin.route('/post/', defaults={'page': 1})
@admin.route('/post/<int:page>/')
def post(page):
    pagination = Post.query.paginate(page, per_page=current_app.config['POSTS_PER_PAGE'])
    posts = pagination.items

    return render_template(
        'admin/posts.html',
        active='admin', label_active='post', posts=posts, pagination=pagination
    )

from werkzeug.datastructures import FileStorage

@admin.route('/post/<int:id>/edit/', methods=['GET', 'POST'])
def edit_post(id):
    p = Post.query.get_or_404(id)

    if request.method == 'POST':
        title = request.form.get('title')
        content = request.form.get('content')
        p.title = title
        p.content = content
        p.update_date = datetime.datetime.now()
        pattern = re.compile(r'<img src="(.*?)".*>')
        match = pattern.search(p.content)
        if match:
            url = match.group(1)
            basename = os.path.basename(url)
            filename = upload_set.path(basename)
            # 生成缩略图 [filename].[ext] -> [filename]_thumb.[ext]
            _splitext = os.path.splitext(filename)
            tb_filename = _splitext[0] + '_thumb' + _splitext[1]
            tb_basename = os.path.basename(tb_filename)
            try:
                image = Image.open(filename)
                image.thumbnail(size=(135, 88))
                image.save(tb_filename)
            except IOError:
                print "cannot create thumbnail for", filename
            else:
                p.thumbnail = upload_set.url(tb_basename)

        db.session.add(p)
        db.session.commit()

    return render_template('admin/post-edit.html', post=p)


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

    news = Category(name='news', cname='新闻通知', order=100)
    session.add(news)
    dispatch = Label(name='dispatch', cname='快讯新闻', order=100, category=news)
    session.add(dispatch)
    notice = Label(name='notice', cname='通知公告', order=200, category=news)
    session.add(notice)
    report = Label(name='report', cname='学术报告', order=300, category=news)
    session.add(report)

    research = Category(name='research', cname='科学研究', order=400)
    session.add(research)
    area = Label(name='area', cname='研究方向', order=200, category=research)
    session.add(area)
    project = Label(name='project', cname='科研项目', order=300, category=research)
    session.add(project)
    equipment = Label(name='equipment', cname='科研设备', order=400, category=research)
    session.add(equipment)

    achievement = Category(name='achievement', cname='研究成果', order=500)
    session.add(achievement)

    paper = Label(name='paper', cname='论文', order=100, category=achievement)
    session.add(paper)
    patent = Label(name='patent', cname='专利', order=200, category=achievement)
    session.add(patent)
    other = Label(name='other', cname='其他', order=300, category=achievement)
    session.add(other)

    teaching = Category(name='teaching', cname='教学工作', order=600)
    session.add(teaching)

    inter_coop = Category(name='inter-coop', cname='国际合作', order=700)
    session.add(inter_coop)

    recruitment = Category(name='recruitment', cname='人员招聘', order=800)
    session.add(recruitment)

    for _ in range(20):
        p = Post(title='今天是个好日子', content='呵呵，只是一个测试', category=news, label=dispatch)
        db.session.add(p)

    user = User(username='whypro', password='whypro')
    db.session.add(user)

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
        image='images/content/052502.jpg', order=100, enable=True
    )
    session.add(slider_1)

    slider_2 = Slider(
        title='皮肤热疼痛实验',
        subtitle='我们团队首次发现热刺激下组织的疼痛水平不仅取决于温度变化，而且受温度变化诱发的热应力的影响，力学因素在组织疼痛中发挥着关键作用，由此建立了热-力-电（疼痛）多场耦合行为理论，为有效指导激光、微波等临床热疗技术及镇痛方案提供了理论依据。',
        image='images/content/052210.jpg', order=200, enable=True
    )
    session.add(slider_2)

    slider_3 = Slider(
        title='标题3',
        subtitle='',
        image='images/content/051903.jpg', order=300, enable=True
    )
    session.add(slider_3)

    session.commit()

