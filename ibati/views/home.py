# -*- coding: utf-8 -*-
from flask import Blueprint, render_template, request, jsonify, redirect, url_for, abort, current_app
from ibati.models import Slider, Category, Post


home = Blueprint('home', __name__)


@home.route('/')
def index():
    sliders = Slider.query.filter_by(enable=True).order_by(Slider.order.asc()).all()

    cat = Category.query.filter_by(name='news').one()
    news = Post.query.filter_by(category_id=cat.id).limit(current_app.config['INDEX_NEWS_NUM'])
    return render_template('index.html', active='index', sliders=sliders, news=news)
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


@home.route('/links/')
def links():
    return redirect(url_for('home.index'))
