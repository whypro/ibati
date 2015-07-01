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
                return redirect(url_for('admin.index'))
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
        active='admin', label_active='post', posts=posts, category=cat, pagination=pagination
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
        label_id = int(request.form.get('label_id'))
        if label_id != -1:
            p.label_id = label_id
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
        label_id = int(request.form.get('label_id'))
        if label_id != -1:
            p.label_id = label_id
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

    return render_template('admin/post-add.html', category_name=category)


@admin.route('/post/<int:id>/delete/')
def delete_post(id):
    p = Post.query.get_or_404(id)
    category_name = p.category.name
    db.session.delete(p)
    db.session.commit()

    return redirect(url_for('admin.post', category=category_name))


@admin.route('/post/delete/batch/')
def batch_delete_post():
    # print request.args
    ids = request.args.getlist('ids[]')
    # print ids
    for id_ in ids:
        p = Post.query.get_or_404(id_)
        db.session.delete(p)
    db.session.commit()

    return jsonify(result=200)


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
    file_storage.filename = file_storage.filename.lower()
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
            children.append(dict(id=label.id, name=label.cname, custom=label.custom))
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
            if not label:
                # new label
                label = Label()
                label.custom = True
                db.session.add(label)

            if label.custom:
                label.name = label_node['name']

            label.cname = label_node['name']
            label.order = j * 100
            label.category_id = category.id

    db.session.commit()
    return jsonify(result=200)


@admin.route('/api/label/<int:id>/delete/')
def delete_label_json(id):
    l = Label.query.get(id)
    db.session.delete(l)
    db.session.commit()
    return jsonify(result=200)


@admin.route('/api/label/get/')
def get_label_json():
    category_id = request.args.get('category_id')
    cat = Category.query.get(category_id)
    print cat.cname
    labels = [dict(id=label.id, name=label.name, cname=label.cname) for label in cat.labels]
    return jsonify(result=200, labels=labels)


