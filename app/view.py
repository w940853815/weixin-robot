# -*- coding: utf-8 -*-
# coding=utf-8
__author__ = 'ruidong.wang@tsingdata.com'

from flask import render_template, g, abort, redirect, url_for, flash, request
from flask_babel import gettext
from app import app, db, lm ,babel
from .model import User, AimlData
from .forms import LoginForm, ConversationForm
from flask_login import current_user, login_required, login_user, logout_user
from datetime import datetime
from config_web import LANGUAGES

@lm.token_loader
def get_auth_token():
    return User.query.get(int(id))


@lm.user_loader
def load_user(id):
    return User.query.get(int(id))

@babel.localeselector
def get_locale():
    return request.accept_languages.best_match(LANGUAGES.keys())

@app.before_request
def before_request():
    g.user = current_user
    if g.user.is_authenticated:
        g.user.last_seen = datetime.utcnow()
        db.session.add(g.user)
        db.session.commit()
        g.locale = get_locale()

@app.errorhandler(403)
def not_allow_error(error):
    return render_template('403.html'), 403


@app.errorhandler(404)
def not_found_error(error):
    return render_template('404.html'), 404


@app.errorhandler(500)
def internal_error(error):
    db.session.rollback()
    return render_template('500.html'), 500

@app.route("/")
@login_required
def index():
    current_user = g.user
    return render_template('index.html',current_user = current_user)

@app.route('/login', methods=['GET','POST'])
def login():
    if g.user is not None and g.user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if request.method == 'POST':
        username = form.username.data
        password = form.password.data
        return validate_login({
            "username"    : username,
            "password"   : password,
        })
    return render_template('login.html', form=form, title=u'请登录')


def validate_login(resp):
    if resp['username'] is None or resp['username'] == "":
        flash(gettext('请输入你的用户名'))
        return redirect(url_for('login'))
    if resp['password'] is None or resp['password'] == "":
        flash(gettext('请输入你的密码'))
        return redirect(url_for('login'))
    user = User.query.filter(User.username == resp['username']).first()
    if user is None:
        flash(gettext(u"账号不存在！请检查重试！"))
        return redirect(url_for('login'))
    user = User.query.filter(User.username == resp['username'], User.password == resp['password']).first()
    if user is None:
        flash(gettext(u'密码错误！'))
        return redirect(url_for('login'))
    '''
    bug:g.user为anonymous，和数据库user表字段active值是null有关系
    '''
    login_user(user)
    return redirect(request.args.get('next') or url_for('index'))

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))


@app.route('/lockscreen')
def lockscreen():
    current_user = g.user.username
    return render_template('lockscreen.html', current_user=current_user)


@app.route('/conversation')
def conversation():
    conversation = AimlData.query.filter(AimlData.id > 0)
    return render_template('conversation_list.html',conversation=conversation)

@app.route('/view/conversation')
def view_conversation():
    form = ConversationForm()
    return render_template('create_conversation.html', form=form)