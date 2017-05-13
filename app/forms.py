# -*- coding: utf-8 -*-
# coding=utf-8
__author__ = 'ruidong.wang@tsingdata.com'
from flask_wtf import Form
from wtforms import StringField, BooleanField, TextAreaField, PasswordField, \
    validators
from wtforms.validators import DataRequired, Length

class LoginForm(Form):
    username = StringField('username', validators=[DataRequired()])
    password = PasswordField('password', validators=[DataRequired()])

class ConversationForm(Form):
    question = StringField('question', validators=[DataRequired()])
    repley = StringField('repley', validators=[DataRequired()])
    label = StringField('label', validators=[DataRequired()])