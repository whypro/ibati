# -*- coding: utf-8 -*-

from flask import Blueprint, render_template, request, jsonify, redirect, url_for, abort



home = Blueprint('home', __name__)


@home.route('/')
def index():
    return 'hello IBATI'
    # return render_template('index.html')
