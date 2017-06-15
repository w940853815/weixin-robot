# -*- coding: utf-8 -*-
# coding=utf-8
__author__ = 'ruidong.wang@tsingdata.com'

import hashlib
from flask import request

from app import app,db
from core import bot
from baike_crawler import baike_crawler
from zhihu_crawler import search_answer,answer_list_to_str
from askToDB import is_ask_to_db,ask_to_db
from config_web import WEI_XIN_TOKEN
from weixin_utils.message import Rec_Msg,Reply_TextMsg,parse_content,parse_xml
import sys
reload(sys)
sys.setdefaultencoding('utf8')


'''获取token只用于验证开发者服务器'''
@app.route('/wx', methods=['GET','POST'])
def verify_server():
    if request.method == 'GET':
        signature = request.args.get('signature' , "")
        timestamp = request.args.get("timestamp" , "")
        nonce = request.args.get("nonce" , "")
        echostr = request.args.get("echostr" , "")
        token = WEI_XIN_TOKEN
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
        '''接受文本消息&被动回复文本消息'''
        if rec_msg.MsgType == "event":
            event=rec_msg.Event
            msg_id='1234567890123456'
            if event == "subscribe":
                # replayText = 'talk@你要说的话-------->和机器人聊天   tuling@你要说的话----->和图灵机器人聊天 \
                #                                                    baike@关键字------------>查看百度百科相关解释  \
                #                                                    zhihu@问题---------------->查看知乎相关回答 \
                #                                                            想要教机器人说话------->请访问网址http://123.207.139.130'
                replayText = 'talk@你要说的话---->和机器人聊天******tuling@你要说的话---->和图灵机器人聊天' \
                             '******baike@关键字---->查看百度百科相关解释******zhihu@问题' \
                             '---->查看知乎相关回答******想要教机器人说话---->请访问网址http://123.207.139.130'
                replyMsg = Reply_TextMsg(to_user, from_user, replayText,rec_msg.MsgType,msg_id)
                return replyMsg.send()
        elif 'baike@' in rec_msg.Content:
            msg_id = rec_msg.MsgId
            rec_msg.insert_text_db(rec_msg)
            keyword = rec_msg.Content.split('@')[1]
            data = baike_crawler(keyword=keyword)
            content = data['summary'].encode('utf-8') + '\n' + '详情请见' + data['url']
            replyMsg = Reply_TextMsg(to_user, from_user, content, rec_msg.MsgType, msg_id)
            replyMsg.insert_reply_db()
            return replyMsg.send()
        elif 'zhihu@' in rec_msg.Content:
            msg_id = rec_msg.MsgId
            rec_msg.insert_text_db(rec_msg)
            question = rec_msg.Content.split('@')[1]
            question_list = search_answer(question=question)
            content = answer_list_to_str(question_list)
            replyMsg = Reply_TextMsg(to_user, from_user, content, rec_msg.MsgType, msg_id)
            replyMsg.insert_reply_db()
            return replyMsg.send()
        elif 'talk@' in rec_msg.Content:
            msg_id = rec_msg.MsgId
            rec_msg.insert_text_db(rec_msg)
            content = bot.respond(rec_msg.Content.split('@')[1])
            if is_ask_to_db(content):
                query = ask_to_db(rec_msg.Content.split('@')[1])
                if query is None:
                    content = '我暂时还不知道怎么回答你的问题，你可以来教我吗？请联系我q940853815'
                else:
                    content = query.replay
            replyMsg = Reply_TextMsg(to_user, from_user, content, rec_msg.MsgType, msg_id)
            replyMsg.insert_reply_db()
            return replyMsg.send()
        elif isinstance(rec_msg, Rec_Msg) and rec_msg.MsgType == 'text' and 'tuling@' in rec_msg.Content:
            msg_id = rec_msg.MsgId
            rec_msg.insert_text_db(rec_msg)
            content = parse_content(rec_msg)
            replyMsg = Reply_TextMsg(to_user, from_user, content['text'].encode('utf-8'),rec_msg.MsgType,msg_id)
            replyMsg.insert_reply_db()
            return replyMsg.send()
        else:
            to_user = rec_msg.FromUserName
            from_user = rec_msg.ToUserName
            # content = 'talk@你要说的话-------->和机器人聊天   tuling@你要说的话----->和图灵机器人聊天 \
            #                                         baike@关键字------------>查看百度百科相关解释  \
            #                                         zhihu@问题---------------->查看知乎相关回答 \
            #                                                 想要教机器人说话------->请访问网址http://123.207.139.130'
            content = 'talk@你要说的话---->和机器人聊天******tuling@你要说的话---->和图灵机器人聊天' \
                         '******baike@关键字---->查看百度百科相关解释******zhihu@问题' \
                         '---->查看知乎相关回答******想要教机器人说话---->请访问网址http://123.207.139.130'
            replyMsg = Reply_TextMsg(to_user, from_user, content,rec_msg.MsgType,rec_msg.MsgId)
            return replyMsg.send()

