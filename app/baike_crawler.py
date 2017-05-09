# -*- coding: utf-8 -*-
# coding=utf-8
__author__ = 'ruidong.wang@tsingdata.com'

import urllib
from bs4 import BeautifulSoup

def data_collect(url, soup):
    data_want = {}
    data_want['url'] = url
    title_node = soup.find('dd', attrs = {'class' : 'lemmaWgt-lemmaTitle-title'}).find('h1')
    data_want['title'] = title_node.getText()

    # <div class="lemma-summary" label-module="lemmaSummary">
    sum_node = soup.find('div', attrs = {'class' : 'lemma-summary'})
    data_want['summary'] = sum_node.getText()

    return data_want

def baike_crawler(keyword):
    url = 'http://baike.baidu.com/item/' + keyword
    response = urllib.urlopen(url)
    if response.getcode() != 200 : #If crawing fails,start next url crawing
        print 'Crawing failed!'
        return {}
    data = response.read()
    soup = BeautifulSoup(data)
    my_data = data_collect(url, soup)
    return my_data

if __name__ == "__main__":
    data = baike_crawler(keyword='python')
    print data['title']