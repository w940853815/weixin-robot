# -*- coding: utf-8 -*-
# coding=utf-8
__author__ = 'ruidong.wang@tsingdata.com'
from app import db
from app.model import Message, Trained
import xml.etree.ElementTree as ET
import time
import urllib
import urllib2
import json
from config_web import TULING_API_KEY

class Rec_Msg(object):
    def __init__(self, xmlData):
        self.ToUserName = xmlData.find('ToUserName').text
        self.FromUserName = xmlData.find('FromUserName').text
        self.CreateTime = xmlData.find('CreateTime').text
        self.MsgType = xmlData.find('MsgType').text
        self.MsgId = xmlData.find('MsgId').text

class Rec_TextMsg(Rec_Msg):
    def __init__(self, xmlData):
        Rec_Msg.__init__(self, xmlData)
        self.Content = xmlData.find('Content').text.encode("utf-8")

    def insert_text_db(self,xmlData):
        message = Message(
            ToUserName = self.ToUserName,
            FromUserName = self.FromUserName,
            CreateTime = self.CreateTime,
            MsgType = self.MsgType,
            MsgId = self.MsgId,
            Content = self.Content
        )
        db.session.add(message)
        db.session.commit()

    def insert_trained_conversation_db(self,conversation):
        data = Trained(
            conversation = conversation

        )
        db.session.add(data)
        db.session.commit()

class Rec_ImageMsg(Rec_Msg):
    def __init__(self, xmlData):
        Rec_Msg.__init__(self, xmlData)
        self.PicUrl = xmlData.find('PicUrl').text

class Reply_Msg(object):
    def __init__(self):
        pass

    def send(self):
        return "success"


class Reply_TextMsg(Reply_Msg):
    def __init__(self, toUserName, fromUserName, content, MsgType, MsgId):
        self.__dict = dict()
        self.__dict['ToUserName'] = toUserName
        self.__dict['FromUserName'] = fromUserName
        self.__dict['CreateTime'] = int(time.time())
        self.__dict['Content'] = content
        self.MsgType = MsgType
        self.MsgId = MsgId

    def insert_api_reply_db(self):
        message = Message(
            ToUserName=self.__dict['ToUserName'],
            FromUserName=self.__dict['FromUserName'],
            CreateTime=int(time.time()),
            MsgType=self.MsgType,
            MsgId=self.MsgId,
            Content= self.__dict['Content']
        )
        db.session.add(message)
        db.session.commit()
    def send(self):
        XmlForm = """
        <xml>
        <ToUserName><![CDATA[{ToUserName}]]></ToUserName>
        <FromUserName><![CDATA[{FromUserName}]]></FromUserName>
        <CreateTime>{CreateTime}</CreateTime>
        <MsgType><![CDATA[text]]></MsgType>
        <Content><![CDATA[{Content}]]></Content>
        </xml>
        """
        return XmlForm.format(**self.__dict)


class Reply_ImageMsg(Reply_Msg):
    def __init__(self, toUserName, fromUserName, mediaId):
        self.__dict = dict()
        self.__dict['ToUserName'] = toUserName
        self.__dict['FromUserName'] = fromUserName
        self.__dict['CreateTime'] = int(time.time())
        self.__dict['MediaId'] = mediaId

    def send(self):
        XmlForm = """
        <xml>
        <ToUserName><![CDATA[{ToUserName}]]></ToUserName>
        <FromUserName><![CDATA[{FromUserName}]]></FromUserName>
        <CreateTime>{CreateTime}</CreateTime>
        <MsgType><![CDATA[image]]></MsgType>
        <Image>
        <MediaId><![CDATA[{MediaId}]]></MediaId>
        </Image>
        </xml>
        """

def parse_xml(web_data):
    if len(web_data) == 0:
        return None
    xmlData = ET.fromstring(web_data)
    msg_type = xmlData.find('MsgType').text
    if msg_type == 'text':
        return Rec_TextMsg(xmlData)
    elif msg_type == 'image':
        return Rec_ImageMsg(xmlData)
        return XmlForm.format(**self.__dict)


def parse_content(rec_msg):

    api_url = 'http://www.tuling123.com/openapi/api'

    values = {
        'key'    : TULING_API_KEY,
        'info': rec_msg.Content,
        'userid': rec_msg.FromUserName
    }

    data = urllib.urlencode(values)  # 编码工作
    req = urllib2.Request(api_url, data)  # 发送请求同时传data表单
    response = urllib2.urlopen(req)  # 接受反馈的信息
    res_data_str = response.read()  # 读取反馈的内容
    res_data_dict = json.loads(res_data_str)
    if res_data_dict['code'] == 100000:
        return res_data_dict
    else:
        return u'对不起，我可能故障了，暂时无法回答你的问题'

