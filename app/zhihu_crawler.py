# -*- coding: utf-8 -*-
# coding=utf-8
__author__ = 'ruidong.wang@tsingdata.com'
from bs4 import BeautifulSoup
import urllib
def search_answer(question):
    url = 'https://www.zhihu.com/search?type=content&sort=upvote&q=' + question
    response = urllib.urlopen(url)
    if response.getcode() != 200:  # If crawing fails,start next url crawing
        print 'Crawing failed!'
        return {}
    data = response.read()
    soup = BeautifulSoup(data)
    data= soup.findAll('a',attrs={'class':'js-title-link'})
    list=[]
    for l in data:
        dict={}
        question_href = l.get('href')
        question_description = l.getText()
        dict['question_href'] = question_href
        dict['question_description'] = question_description
        list.append(dict)
    return list
def answer_list_to_str(list):
    str=''
    for l in list:
        str= str + l['question_description'].encode('utf-8') + '\n'+'详情请见' + 'https://www.zhihu.com'+\
             l['question_href'].encode('utf-8') + '\n'
    return str