# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from flask import Blueprint, render_template, request, jsonify, redirect, url_for, abort, current_app

from ..models import Slider, Category, Post, Label, Advertisement
from ..extensions import db
from ..helpers import get_client_ip

home = Blueprint('home', __name__)


@home.route('/')
def index():
    sliders = Slider.query.filter_by(enable=True).order_by(Slider.order.asc()).all()
    advertisement = Advertisement.query.first()

    research_cat = Category.query.filter_by(name='research').one()
    area_label = Label.query.filter_by(name='area').one()
    areas = Post.query.filter_by(category_id=research_cat.id, label_id=area_label.id).limit(current_app.config['INDEX_AREA_NUM'])

    news_cat = Category.query.filter_by(name='news').one()
    dispatch_label = Label.query.filter_by(name='dispatch').one()
    notice_label = Label.query.filter_by(name='notice').one()
    report_label = Label.query.filter_by(name='report').one()
    dispatches = Post.query.filter_by(category_id=news_cat.id, label_id=dispatch_label.id).order_by(Post.create_date.desc()).limit(current_app.config['INDEX_NEWS_NUM'])
    notices = Post.query.filter_by(category_id=news_cat.id, label_id=notice_label.id).order_by(Post.create_date.desc()).limit(current_app.config['INDEX_NEWS_NUM'])
    reports = Post.query.filter_by(category_id=news_cat.id, label_id=report_label.id).order_by(Post.create_date.desc()).limit(current_app.config['INDEX_NEWS_NUM'])
    current_app.logger.info('user visit index, clinet_ip<%s>', get_client_ip())
    return render_template('index.html', active='index', sliders=sliders, areas=areas, dispatches=dispatches, notices=notices, reports=reports, advertisement=advertisement)
    # return render_template('index.html')


@home.route('/contact-us/')
def contact_us():
    cat = Category.query.filter(Category.name=='contact-us').one()
    p = cat.posts[0]
    p.click_count += 1
    db.session.add(p)
    db.session.commit()
    return render_template('contact-us.html', category='contact-us', post=p)


@home.route('/about-us/')
def about_us():
    cat = Category.query.filter(Category.name=='about-us').one()
    p = cat.posts[0]
    p.click_count += 1
    db.session.add(p)
    db.session.commit()
    return render_template('about-us.html', category='about-us', post=p)


@home.route('/team/')
def team():
    return render_template('team.html', active='team')


@home.route('/links/')
def links():
    return redirect(url_for('home.index'))
