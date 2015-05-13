# -*- coding: utf-8 -*-

from flask import Blueprint, render_template, request, jsonify, redirect, url_for, abort

from ibati.models import Category, Post

post = Blueprint('post', __name__, url_prefix='/post')



@post.route('/<category>/')
def index(category):
    result = Category.query.filter(Category.name==category).one()
    return render_template('post/posts.html', active=category, category=result)


@post.route('/<int:id>/')
def detail(id):
    result = Post.query.get_or_404(id)
    return render_template('post/post-left-sidebar.html', active=result.category.name, post=result)


@post.route('/add/', methods=['GET', 'POST'])
def add():
    if request.method == 'POST':
        print 'done'
        return redirect(url_for('post.add'))
    
    return render_template('post/post-add.html')

@post.route('/<int:id>/delete/')
def delete(id):
    pass

