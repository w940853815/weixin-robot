# -*- coding: utf-8 -*-
# coding=utf-8
__author__ = 'ruidong.wang@tsingdata.com'

from app import db

class Message(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    ToUserName = db.Column(db.String(128))
    FromUserName = db.Column(db.VARCHAR(64))
    CreateTime = db.Column(db.Integer)
    MsgType = db.Column(db.String(32))
    Content = db.Column(db.VARCHAR(1024))
    PicUrl = db.Column(db.Text)  #图片链接（由系统生成）
    MediaId = db.Column(db.VARCHAR(128)) #图片消息媒体id，可以调用多媒体文件下载接口拉取数据。
    Format = db.Column(db.String(16))#语音格式，如amr，speex等
    Title = db.Column(db.VARCHAR(32)) #消息标题
    Description = db.Column(db.VARCHAR(1024)) #消息描述
    Url = db.Column(db.Text) #消息链接
    MsgId =  db.Column(db.VARCHAR(64))

    def __repr__(self):
        return self.MsgType


class User(object):
    """
    Example User object.  Based loosely off of Flask-Login's User model.
    """
    full_name = "John Doe"
    avatar = "/static/img/user2-160x160.jpg"
    created_at = "November 12, 2012"
