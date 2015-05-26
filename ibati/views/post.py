# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from flask import Blueprint, render_template, request, jsonify, redirect, url_for, abort

from ibati.extensions import db
from ibati.models import Category, Label, Post

post = Blueprint('post', __name__, url_prefix='/post')



@post.route('/<category>/')
@post.route('/<category>/<label>/')
def index(category, label=None):
    cat = Category.query.filter(Category.name==category).one()

    qry = Post.query.filter(Post.category_id==cat.id)
    if label:
        lab = Label.query.filter(Label.name==label).one()
        qry = qry.filter(Post.label_id==lab.id)
    else:
        lab = None
    posts = qry.all()
    return render_template(
        'post/posts.html', 
        active=cat.name, label_active=label, category=cat, label=lab, posts=posts
    )


@post.route('/<int:id>/')
def detail(id):
    p = Post.query.get_or_404(id)
    return render_template('post/post-detail.html', category=p.category, post=p)


@post.route('/add/', methods=['GET', 'POST'])
def add():
    if request.method == 'POST':
        print 'done'
        return redirect(url_for('post.add'))
    
    return render_template('post/post-add.html')

@post.route('/<int:id>/delete/')
def delete(id):
    p = Post.query.get_or_404(id)
    db.session.delete(p)
    db.session.commit()

    return '删除成功'

