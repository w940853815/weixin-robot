# -*- coding: utf-8 -*-
# coding=utf-8
__author__ = 'ruidong.wang@tsingdata.com'

from flask import render_template, g, jsonify, redirect, url_for, flash, request
from flask_babel import gettext
from app import app, db, lm ,babel
from .model import User, AimlData, Message
from .forms import LoginForm, ConversationForm, UserForm
from flask_login import current_user, login_required, login_user, logout_user
from datetime import datetime
from config_web import LANGUAGES
import os,time
from werkzeug.utils import secure_filename

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

@app.route("/introduction")
@login_required
def introduction():
    return render_template('introduction.html')

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

@app.route('/list/user')
@login_required
def list_user():
    user = User.query.filter(User.id > 0)
    return render_template('user_list.html',user=user)

@app.route('/create/user',methods=['GET','POST'])
@login_required
def create_user():
    form = UserForm()
    if request.method == 'POST':
        username = request.form['username']
        first_password = request.form['first_password']
        confirm_password = request.form['confirm_password']
        avatar_f =request.files['avatar']
        if avatar_f:
            flag = '.' in avatar_f.filename and avatar_f.filename.rsplit('.',1)[1] in app.config['ALLOWED_IMG_EXTENSIONS']
            if not flag:
                flash(u'只允许上传png,jpg,jpeg,gif格式的文件')
                return redirect(url_for('create_user'))
            filedir = os.path.join(
                app.config['UPLOAD_FOLDER'],'avatar',str(g.user.id),str(time.time())
            )
            if not os.path.exists(filedir):
                os.makedirs(filedir)
            filename = filedir.split(
                app.config['UPLOAD_FOLDER'])[-1]  + '/' + secure_filename(avatar_f.filename)
            avatar_f.save(os.path.join(
                app.config['UPLOAD_FOLDER'], filename
            ))

        user = User(
            username=username,
            password=first_password,
            avatar=filename
        )
        db.session.add(user)
        db.session.commit()
        return render_template('create_user.html', form=form)
    return render_template('create_user.html',form=form)

@app.route('/list/conversation')
@login_required
def list_conversation():
    form = ConversationForm()
    conversation = AimlData.query.filter(AimlData.id > 0)
    return render_template('conversation_list.html',conversation=conversation,form=form)

@app.route('/create/conversation', methods=['GET','POST'])
@login_required
def create_conversation():
    form = ConversationForm()
    if request.method == 'POST':
        question = request.form['question']
        replay = request.form['replay']
        label = request.form['label']
        aiml_data = AimlData(
            question = question,
            replay = replay,
            label = label
        )
        db.session.add(aiml_data)
        db.session.commit()
        return render_template('create_conversation.html', form=form)
    return render_template('create_conversation.html', form=form)


@app.route('/rest/edit/conversation',methods=['POST'])
@login_required
def edit_conversation():
    if request.method == 'POST':
        act = request.form.get('act','')
        print act
        if act == 'show':
            id = request.form['id']
            conversation = AimlData.query.filter(AimlData.id == id).first()
            question = conversation.question
            replay = conversation.replay
            label =conversation.label
            data = {
                'id':id,
                'question':question,
                'replay':replay,
                'label':label
            }
            return jsonify(data)
        if act == '':
            id = request.form['id']
            print id
            conversation = AimlData.query.filter(AimlData.id == id).first()
            conversation.question = request.form['question']
            conversation.replay = request.form['replay']
            conversation.label = request.form['label']
            db.session.add(conversation)
            db.session.commit()
            flash(u'对话数据修改成功！')
            return redirect(url_for('list_conversation'))
        # return 'success!'

@app.route('/list/message')
@login_required
def list_message():
    message = Message.query.filter(Message.id > 0)
    return render_template('message_list.html',message=message)

