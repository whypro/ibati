# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from flask import Blueprint, render_template, request, jsonify, redirect, url_for, abort, current_app
from ibati.models import Slider, Category, Post, Label


home = Blueprint('home', __name__)


@home.route('/')
def index():
    sliders = Slider.query.filter_by(enable=True).order_by(Slider.order.asc()).all()

    research_cat = Category.query.filter_by(name='research').one()
    area_label = Label.query.filter_by(name='area').one()
    areas = Post.query.filter_by(category_id=research_cat.id, label_id=area_label.id).limit(current_app.config['INDEX_NEWS_NUM'])

    news_cat = Category.query.filter_by(name='news').one()
    dispatch_label = Label.query.filter_by(name='dispatch').one()
    notice_label = Label.query.filter_by(name='notice').one()
    report_label = Label.query.filter_by(name='report').one()
    dispatches = Post.query.filter_by(category_id=news_cat.id, label_id=dispatch_label.id).limit(current_app.config['INDEX_NEWS_NUM'])
    notices = Post.query.filter_by(category_id=news_cat.id, label_id=notice_label.id).limit(current_app.config['INDEX_NEWS_NUM'])
    reports = Post.query.filter_by(category_id=news_cat.id, label_id=report_label.id).limit(current_app.config['INDEX_NEWS_NUM'])
    return render_template('index.html', active='index', sliders=sliders, areas=areas, dispatches=dispatches, notices=notices, reports=reports)
    # return render_template('index.html')


@home.route('/contact-us/')
def contact_us():
    return render_template('contact-us.html', active='contact_us')


@home.route('/team/')
def team():
    return render_template('team.html', active='team')


@home.route('/links/')
def links():
    return redirect(url_for('home.index'))
