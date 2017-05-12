# -*- coding: utf-8 -*-
# coding=utf-8
__author__ = 'ruidong.wang@tsingdata.com'

from model import AimlData

def is_ask_to_db(input):
    if input[0] == '#':
        return True

def ask_to_db(input):
    aiml_data = AimlData.query.filter(AimlData.question.like('%' + input + '%'), AimlData.is_deleted == False)
    return aiml_data.first()

