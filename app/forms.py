# -*- coding: utf-8 -*-
# coding=utf-8
__author__ = 'ruidong.wang@tsingdata.com'
from flask_wtf import Form
from wtforms import StringField, FileField, TextAreaField, PasswordField, \
    validators,BooleanField
from wtforms.validators import DataRequired, Length

class LoginForm(Form):
    username = StringField('username', validators=[DataRequired()])
    password = PasswordField('password', validators=[DataRequired()])

class ConversationForm(Form):
    id = StringField('id',validators=[DataRequired()])
    question = StringField('question', validators=[DataRequired()])
    replay = StringField('repley', validators=[DataRequired()])
    label = StringField('label', validators=[DataRequired()])

class UserForm(Form):
    id = StringField('id',validators=[DataRequired()])
    username = StringField('username',validators=[DataRequired()])
    first_password = PasswordField('first_password',validators=[DataRequired()])
    confirm_password =PasswordField ('confirm_password',validators=[DataRequired()])
    avatar = FileField()
    is_active = BooleanField()