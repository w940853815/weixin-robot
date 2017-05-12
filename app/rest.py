# -*- coding: utf-8 -*-
# coding=utf-8
__author__ = 'ruidong.wang@tsingdata.com'

import hashlib
import xml.etree.ElementTree as ET
import time
from flask import request, redirect, url_for
import urllib
import urllib2
import json

from app import app,db
from model import Message, Trained
from core import bot
from baike_crawler import baike_crawler
from zhihu_crawler import search_answer,answer_list_to_str
from askToDB import is_ask_to_db,ask_to_db
import sys
reload(sys)
sys.setdefaultencoding('utf8')

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

        def insert_img_db(self, xmlData):
            message = Message(
                ToUserName = self.ToUserName,
                FromUserName = self.FromUserName,
                CreateTime = self.CreateTime,
                MsgType = self.MsgType,
                MsgId = self.MsgId,
                PicUrl = self.PicUrl
            )
            db.session.add(message)
            db.session.commit()


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
        'key'    : 'b74a80570b614b8d971a91b00ce027af',
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
        return u'对不起，我可能生病了，暂时无法回答你的问题'




'''获取token只用于验证开发者服务器'''
@app.route('/wx', methods=['GET','POST'])
def verify_server():
    if request.method == 'GET':
        signature = request.args.get('signature' , "")
        timestamp = request.args.get("timestamp" , "")
        nonce = request.args.get("nonce" , "")
        echostr = request.args.get("echostr" , "")
        token = "wangruidong940853815"
        list = [token , timestamp , nonce]
        list.sort()
        sha1 = hashlib.sha1()
        map(sha1.update , list)
        hashcode = sha1.hexdigest()

        if hashcode == signature:
            return echostr
        else:
            return ""
    if request.method == 'POST':
        web_data = request.data
        rec_msg = parse_xml(web_data)
        to_user = rec_msg.FromUserName
        from_user = rec_msg.ToUserName
        msg_id = rec_msg.MsgId
        '''接受文本消息&被动回复文本消息'''
        if 'teach@' in rec_msg.Content:
            rec_msg.insert_trained_conversation_db(rec_msg.Content.split('@')[1])
            content = u"我记下来了^_^"
            replyMsg = Reply_TextMsg(to_user, from_user, content, rec_msg.MsgType, msg_id)
            return replyMsg.send()
        elif 'baike@' in rec_msg.Content:
            keyword = rec_msg.Content.split('@')[1]
            data = baike_crawler(keyword=keyword)
            content = data['summary'].encode('utf-8') + '\n' + '详情请见' + data['url']
            replyMsg = Reply_TextMsg(to_user, from_user, content, rec_msg.MsgType, msg_id)
            return replyMsg.send()
        elif 'zhihu@' in rec_msg.Content:
            question = rec_msg.Content.split('@')[1]
            question_list = search_answer(question=question)
            content = answer_list_to_str(question_list)
            replyMsg = Reply_TextMsg(to_user, from_user, content, rec_msg.MsgType, msg_id)
            return replyMsg.send()
        elif 'talk@' in rec_msg.Content:
            content = bot.respond(rec_msg.Content.split('@')[1])
            if is_ask_to_db(content):
                query = ask_to_db(rec_msg.Content.split('@')[1])
                if query is None:
                    content = '我暂时还不知道怎么回答你的问题，你可以来教我吗？请联系我q940853815'
                else:
                    content = query.replay

            replyMsg = Reply_TextMsg(to_user, from_user, content, rec_msg.MsgType, msg_id)
            return replyMsg.send()
        elif isinstance(rec_msg, Rec_Msg) and rec_msg.MsgType == 'text' and 'tuling@' in rec_msg.Content:
            rec_msg.insert_text_db(rec_msg)
            content = parse_content(rec_msg)
            replyMsg = Reply_TextMsg(to_user, from_user, content['text'].encode('utf-8'),rec_msg.MsgType,msg_id)
            replyMsg.insert_api_reply_db()
            return replyMsg.send()
        else:
            to_user = rec_msg.FromUserName
            from_user = rec_msg.ToUserName
            content = '我正在学习识别中。。。^_^敬请期待'
            replyMsg = Reply_TextMsg(to_user, from_user, content,rec_msg.MsgType,rec_msg.MsgId)
            return replyMsg.send()

