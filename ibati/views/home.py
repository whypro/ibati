# -*- coding: utf-8 -*-

from flask import Blueprint, render_template, request, jsonify, redirect, url_for, abort



home = Blueprint('home', __name__)


@home.route('/')
def index():
    return render_template('index.html', active='index')
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

@home.route('/login/')
def login():
    return render_template('login.html')

@home.route('/links/')
def links():
    return redirect(url_for('home.index'))