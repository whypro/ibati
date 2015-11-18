# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from flask import Blueprint, render_template, request, jsonify, redirect, url_for, abort, current_app

from ..extensions import db
from ..models import Category, Label, Post
from .home import about_us, contact_us

post = Blueprint('post', __name__, url_prefix='/post')


@post.route('/<category>/', defaults={'page': 1})
@post.route('/<category>/page/<int:page>/')
@post.route('/<category>/<label>/', defaults={'page': 1})
@post.route('/<category>/<label>/page/<int:page>/')
def index(category, page, label=None):

    cat = Category.query.filter(Category.name==category).one()

    # 单位简介
    if cat.name == 'about-us':
        return redirect(url_for('home.about_us'))
    # 联系我们
    elif cat.name == 'contact-us':
        return redirect(url_for('home.contact_us'))

    # 其他页面
    qry = Post.query.filter_by(category_id=cat.id, status="公开")
    # 子类别筛选
    if label:
        lab = Label.query.filter_by(name=label).one()
        qry = qry.filter_by(label_id=lab.id)
    else:
        lab = None
    # 排序
    if cat.name == 'member':
        qry = qry.order_by(Post.create_date.asc())
    else:
        qry = qry.order_by(Post.create_date.desc())

    pagination = qry.paginate(page, per_page=current_app.config['POSTS_PER_PAGE'])
    posts = pagination.items

    return render_template(
        'post/posts.html', 
        active=cat.name, label_active=label, category=cat, label=lab, posts=posts, pagination=pagination
    )


@post.route('/<int:id>/')
def detail(id):
    p = Post.query.get_or_404(id)
    p.click_count += 1
    db.session.add(p)
    db.session.commit()
    return render_template('post/post-detail.html', category=p.category, label=p.label, post=p)


