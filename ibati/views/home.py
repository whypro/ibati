# -*- coding: utf-8 -*-
import hashlib
from flask import Blueprint, render_template, request, jsonify, redirect, url_for, abort
from flask.ext.login import login_user, logout_user, login_required, current_user
from ibati.models import Slider, User


home = Blueprint('home', __name__)


@home.route('/')
def index():
    sliders = Slider.query.order_by(Slider.order.asc()).all()
    return render_template('index.html', active='index', sliders=sliders)
    # return render_template('index.html')


@home.route('/about-us/')
def about_us():
    return render_template('about-us.html', active='about_us')


@home.route('/contact-us/')
def contact_us():
    return render_template('contact-us.html', active='contact_us')


@home.route('/team/')
def team():
    return render_template('team.html', active='team')


@home.route('/login/', methods=['GET', 'POST'])
def login():
    # 已登录用户则返回首页
    if current_user.is_authenticated():
        return redirect(url_for('home.index'))

    if request.method == 'POST':
        username = request.form.get('username', '')
        password = hashlib.md5(request.form.get('password', '')).hexdigest()
        user = User.query.filter_by(username=username, password=password).first()
        if user:
            login_user(user)
            return redirect(url_for('home.index'))
    return render_template('login.html')


@home.route("/logout/")
@login_required
def logout():
    logout_user()
    return redirect(url_for('home.index'))


@home.route('/links/')
def links():
    return redirect(url_for('home.index'))
