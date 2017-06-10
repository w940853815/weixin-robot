# -*- coding: utf-8 -*-
# coding=utf-8
__author__ = 'ruidong.wang@tsingdata.com'

from app import db
from datetime import datetime

class Message(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    ToUserName = db.Column(db.String(128))
    FromUserName = db.Column(db.VARCHAR(64))
    CreateTime = db.Column(db.DateTime,default=datetime.now)
    MsgType = db.Column(db.String(32))
    Content = db.Column(db.VARCHAR(512))
    MsgId =  db.Column(db.VARCHAR(64))

    def __repr__(self):
        return self.MsgType


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    avatar = db.Column(db.String(512))
    password = db.Column(db.String(30), index=True)
    last_seen = db.Column(db.DateTime,default=datetime.now)
    active = db.Column(db.Boolean(), default=True)

    @property
    def is_authenticated(self):
        return self.active

    @property
    def is_active(self):
        return self.active

    @property
    def is_anonymous(self):
        return False

    def get_id(self):
        try:
            return unicode(self.id)  # python 2
        except NameError:
            return str(self.id)  # python 3

    def get_auth_token(self):
        try:
            return unicode(self.id)  # python 2
        except NameError:
            return str(self.id)  # python 3

    def __repr__(self):  # pragma: no cover
        return '<User %r>' % (self.username)

class AimlData(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    create_time = db.Column(db.DateTime,default=datetime.now)
    is_deleted = db.Column(db.Boolean(),default=False)
    last_modify_time = db.Column(db.DateTime,default=datetime.now)
    question = db.Column(db.String(512),index=True)
    replay = db.Column(db.String(512))
    label =  db.Column(db.String(256))

    def __repr__(self):  # pragma: no cover
        return self.question

