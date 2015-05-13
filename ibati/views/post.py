# -*- coding: utf-8 -*-

from flask import Blueprint, render_template, request, jsonify, redirect, url_for, abort


post = Blueprint('post', __name__)


@post.route('/news/')
def news():
    return render_template('post/posts.html')


@post.route('/news/<int:id>')
def detail(id):
    return render_template('post/post-left-sidebar.html')