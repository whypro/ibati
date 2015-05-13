# -*- coding: utf-8 -*-

from flask import Blueprint, render_template, request, jsonify, redirect, url_for, abort


member = Blueprint('member', __name__, url_prefix='/member')

@member.route('/')
def index():
    return render_template('member/members.html', active='member')

@member.route('/<int:id>/')
def detail(id):
    return render_template('member/member-detail.html', active='member')
