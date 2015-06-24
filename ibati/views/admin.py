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
from ibati.models import Category, Label, Post, JobTitle, Member, Slider, User, Link
from werkzeug.datastructures import FileStorage
import json

admin = Blueprint('admin', __name__, url_prefix='/admin')


@admin.route('/')
@login_required
def index():
    return render_template('admin/index.html')


@admin.route('/upload/', methods=['POST'])
@login_required
def upload():
    # print request.form
    # print request.files['imgFile']
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


@admin.route('/post/<category>/', defaults={'page': 1})
@admin.route('/post/<category>/<int:page>/')
def post(category, page):
    cat = Category.query.filter_by(name=category).one()
    pagination = Post.query.filter_by(category_id=cat.id).order_by(Post.update_date.desc()).paginate(page, per_page=current_app.config['POSTS_PER_PAGE'])
    posts = pagination.items

    return render_template(
        'admin/posts.html',
        active='admin', label_active='post', posts=posts, pagination=pagination
    )


@admin.route('/post/<int:id>/edit/', methods=['GET', 'POST'])
def edit_post(id):
    p = Post.query.get_or_404(id)

    if request.method == 'POST':
        title = request.form.get('title')
        content = request.form.get('content')
        p.title = title
        p.content = content
        p.category_id = request.form.get('category_id')
        p.label_id = request.form.get('label_id')
        p.status = request.form.get('status')
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

    category_labels = Label.query.filter_by(category_id=p.category_id).all()

    return render_template('admin/post-edit.html', post=p, category_labels=category_labels)


@admin.route('/post/add/', methods=['GET', 'POST'])
@admin.route('/post/<category>/add/', methods=['GET'])
def add_post(category=None):
    if request.method == 'POST':
        p = Post()
        title = request.form.get('title')
        content = request.form.get('content')
        p.title = title
        p.content = content
        p.category_id = request.form.get('category_id')
        p.label_id = request.form.get('label_id')
        p.status = request.form.get('status')
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

        return redirect(url_for('admin.post', category=p.category.name))

    return render_template('admin/post-add.html')


@admin.route('/slider/')
def slider():
    sliders = Slider.query.order_by(Slider.order.asc()).all()
    return render_template('admin/sliders.html', sliders=sliders)


@admin.route('/link/')
def link():
    links = Link.query.order_by(Link.order.asc()).all()
    return render_template('admin/links.html', links=links)


@admin.route('/link/add/', methods=['POST'])
def add_link():
    name = request.form.get('name')
    href = request.form.get('href')
    order = request.form.get('order')
    l = Link(name=name, href=href, order=order)
    db.session.add(l)
    db.session.commit()
    return jsonify(result=200)


@admin.route('/link/<int:id>/edit/', methods=['POST'])
def edit_link(id):
    l = Link.query.get_or_404(id)
    name = request.form.get('name')
    href = request.form.get('href')
    order = request.form.get('order')
    # print name, href
    l.name = name
    l.href = href
    l.order = order

    db.session.add(l)
    db.session.commit()
    return jsonify(result=200)


@admin.route('/link/<int:id>/delete/')
def delete_link(id):
    l = Link.query.get_or_404(id)
    db.session.delete(l)
    db.session.commit()
    return redirect(url_for('admin.link'))


@admin.route('/link/delete/batch/')
def batch_delete_link():
    # print request.args
    ids = request.args.getlist('ids[]')
    # print ids
    for id_ in ids:
        l = Link.query.get_or_404(id_)
        db.session.delete(l)
    db.session.commit()

    return jsonify(result=200)


@admin.route('/slider/add/', methods=['POST'])
def add_slider():
    title = request.form.get('title')
    subtitle = request.form.get('subtitle')
    image = request.form.get('image')
    order = request.form.get('order')
    enable = True if request.form.get('enable') == 'true' else False

    s = Slider(title=title, subtitle=subtitle, image=image, order=order, enable=enable)
    db.session.add(s)
    db.session.commit()
    return jsonify(result=200)


@admin.route('/slider/<int:id>/edit/', methods=['POST'])
def edit_slider(id):
    s = Slider.query.get_or_404(id)
    title = request.form.get('title')
    subtitle = request.form.get('subtitle')
    image = request.form.get('image')
    order = request.form.get('order')
    enable = True if request.form.get('enable') == 'true' else False
    print request.form.get('enable'), enable
    # print name, href
    s.title = title
    s.subtitle = subtitle
    s.image = image
    s.order = order
    s.enable = enable

    db.session.add(s)
    db.session.commit()
    return jsonify(result=200)


@admin.route('/slider/<int:id>/delete/')
def delete_slider(id):
    s = Slider.query.get_or_404(id)
    db.session.delete(s)
    db.session.commit()
    return redirect(url_for('admin.slider'))


@admin.route('/slider/delete/batch/')
def batch_delete_slider():
    # print request.args
    ids = request.args.getlist('ids[]')
    # print ids
    for id_ in ids:
        s = Slider.query.get_or_404(id_)
        db.session.delete(s)
    db.session.commit()

    return jsonify(result=200)

from urlparse import urlparse
@admin.route('/slider/upload/', methods=['POST'])
def upload_slider():
    print request.files
    if 'imageFile' not in request.files:
        abort(400)

    file_storage = request.files['imageFile']
    basename = hashlib.sha1(file_storage.read()).hexdigest()+os.path.splitext(file_storage.filename)[1]
    file_storage.seek(0)
    filename = upload_set.save(file_storage, name=basename)
    return jsonify(result=200, path=urlparse(upload_set.url(filename)).path)


@admin.route('/category/')
def category():
    return render_template('admin/categories.html')


@admin.route('/api/category/get/')
def get_category_ztree_json():
    nodes = []
    categories = Category.query.order_by(Category.order.asc()).all()
    for category in categories:
        children = []
        for label in category.labels:
            children.append(dict(id=label.id, name=label.cname))
        nodes.append(dict(id=category.id, name=category.cname, open=True, children=children))
    return json.dumps(nodes)


@admin.route('/api/category/post/', methods=['POST'])
def post_category_ztree_json():
    nodes = request.get_json()
    # print json.dumps(nodes)
    for i, category_node in enumerate(nodes, start=1):
        category = Category.query.get(category_node['id'])
        category.cname = category_node['name']
        category.order = i * 100
        for j, label_node in enumerate(category_node['children'], start=1):
            label = Label.query.get(label_node['id'])
            label.cname = label_node['name']
            label.order = j * 100

    db.session.commit()
    return jsonify(result=200)


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

    about_us = Category(name='about-us', cname='单位简介', order=50)
    session.add(about_us)

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

    member = Category(name='member', cname='研究队伍', order=500)
    session.add(member)
    teacher = Label(name='teacher', cname='教师', order=100, category=member)
    session.add(teacher)
    postdoctor = Label(name='postdoctor', cname='博士后', order=150, category=member)
    session.add(postdoctor)
    professor = Label(name='professor', cname='客座教授', order=200, category=member)
    session.add(professor)
    visiting_scholar = Label(name='visiting-scholar', cname='访问学者', order=300, category=member)
    session.add(visiting_scholar)

    achievement = Category(name='achievement', cname='研究成果', order=520)
    session.add(achievement)
    paper = Label(name='paper', cname='论文', order=100, category=achievement)
    session.add(paper)
    patent = Label(name='patent', cname='专利', order=200, category=achievement)
    session.add(patent)
    monograph = Label(name='monograph', cname='专著', order=250, category=achievement)
    session.add(monograph)
    other = Label(name='other', cname='其他', order=300, category=achievement)
    session.add(other)

    postgraduate = Category(name='postgraduate', cname='研究生培养', order=600)
    session.add(postgraduate)
    enrolling = Label(name='enrolling', cname='研究生招生', order=100, category=postgraduate)
    session.add(enrolling)
    candidate = Label(name='candidate', cname='在读研究生', order=200, category=postgraduate)
    session.add(candidate)
    graduated = Label(name='graduated', cname='毕业研究生', order=300, category=postgraduate)
    session.add(graduated)

    teaching = Category(name='teaching', cname='教学工作', order=700)
    session.add(teaching)
    undergraduate = Label(name='undergraduate', cname='本科生教学', order=100, category=teaching)
    session.add(undergraduate)
    postgraduate = Label(name='postgraduate', cname='研究生教学', order=200, category=teaching)
    session.add(postgraduate)

    inter_coop = Category(name='inter-coop', cname='国际合作', order=720)
    session.add(inter_coop)

    recruitment = Category(name='recruitment', cname='人员招聘', order=800)
    session.add(recruitment)

    for _ in range(20):
        p = Post(
            title='西安交大参加教育部深化高等学校创新创业教育改革视频会议',
            content=('2015年6月2日，教育部组织召开深化高等学校创新创业教育改革视频会议，'
                     '西安交大校长王树国、党委副书记宫辉、副校长郑庆华以及'
                     '教务处、研究生院、就业中心、科研院、人力资源部、财务处、学生处、团委、工程坊、科技园、各书院负责人'
                     '和创新创业教育教师代表40余人全程参会。'
                     '为深入贯彻落实《国务院办公厅关于深化高等学校创新创业教育改革的实施意见》(以下简称《实施意见》)，'
                     '教育部组织召开深化高等学校创新创业教育改革视频会议，对深化高校创新创业教育改革工作进行动员部署，'
                     '努力造就大众创业、万众创新的生力军，为国家实施创新驱动发展战略提供人才智力支撑。'
                     '教育部袁贵仁部长等教育部负责同志、教育部相关部门机构、各省教育行政部门和教育部直属高校等'
                     '共7600余人参加大会。'),
            category=news, label=dispatch
        )
        db.session.add(p)

    p = Post(
        title='单位简介',
        content=('西安交通大学 生物医学分析技术与仪器研究所'
                 'Institute of Biomedical Analytical Technology and Instrumentation'
                 '生物医学分析技术及仪器研究所是根据国家十一五发展规划和生命科学与技术学院整体发展需要，'
                 '通过学院整合于2007年6月15日成立。目标是充分发挥学科交叉的作用，'
                 '在生物医学分析技术与仪器的基础理论研究、应用研究、人才培养、促进相应技术转化为生产力等方面取得显著进展。'
                 '该所现有教职工12人，其中教授5人，副教授3 人和高级工程师1人，讲师3位。'
                 '目前承担和完成了国家自然科学基金近30项（包括重点项目、国际合作）、国家科技部863项目、国家重大科学仪器设备开发项目、'
                 '陕西省自然科学基金项目、西安市科技攻关项目、横向课题数十项等。'
                 '目前的研究方向有生物医学光子学影像与光谱分析技术、基于多信息融合的生物荧光探针和光学传感器、先进敏感分析技术及仪器等。'
                 '目前研究的重点项目包括有：基于多光谱荧光成像的在体三维光学标测系统、基于新型光穿孔技术的纳米尺度细胞膜微手术研究、'
                 '金纳米棒靶向的激光细胞微手术及其机理研究、纳米材料的界观和微观效应及机理、基于纳米金探针的肿瘤细胞示踪等研究。'
                 '研究所现有博士和硕士研究生80多名。'),
        category=about_us
    )
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
        subtitle='由此建立了热-力-电（疼痛）多场耦合行为理论，为有效指导激光、微波等临床热疗技术及镇痛方案提供了理论依据。',
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

    init_links(session)


def init_links(session):
    for i in range(5):
        l = Link(name='友情链接', href='http://www.xjtu.edu.cn', order=i)
        session.add(l)
    session.commit()
