# -*- coding: utf-8 -*-
# coding=utf-8
__author__ = 'ruidong.wang@tsingdata.com'

from flask import render_template
from app import app
from .model import User


@app.route("/")
def index():
    current_user = User()
    return render_template('index.html',current_user = current_user)

@app.route('/login')
def login():
    return render_template('login.html', current_user=current_user)

@app.route('/lockscreen')
def lockscreen():
    return render_template('lockscreen.html', current_user=current_user)
