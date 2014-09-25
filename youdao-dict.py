#!/bin/python2
# -*- coding: utf-8 -*-

'''
基于有道Web端的在线命令行词典
因为有道Web端相对API的释义比较丰富，所以这里用爬虫的方法来抓取释义..
'''

import urllib2
import re
import sys
from subprocess import Popen, PIPE
from bs4 import BeautifulSoup


def escape(s):
    def _print(x):
        x = x.group()
        code, x = x[0:2], x[2:]
        if code != '\\x':
            return x
        return ('%'+str(x)).upper()

    s = repr(s)
    return re.sub(r'\\x[0-9a-fA-F]{2}', _print, s)


def get_url(s):
    # API interface
    # url = ('http://fanyi.youdao.com/openapi.do?keyfrom=tinxing'
    # &key=1312427901&type=data&doctype=json&version=1.1&q=')
    # Web interface
    url = 'http://dict.youdao.com/search?keyfrom=dict.index&q='
    s = escape(s)
    return url+s[1:-1]


def output(data):
    if 'translation' in data:
        print('Traslation:')
        for i in data['translation']:
            print('  '+i)
        print
    if 'basic' in data and 'explains' in data['basic']:
        print('Explains: ')
        for i in data['basic']['explains']:
            print('  '+i)
        print
    if 'web' in data:
        for item in data['web']:
            print(item['key']),
            print(':'),
            for i, v in enumerate(item['value']):
                print(v),
                print(';' if i != len(item['value'])-1 else ''),
            print


def lookup(s):
    p1 = Popen(['echo', s], stdout=PIPE)
    p2 = Popen(['/usr/bin/sticky.py'], stdin=p1.stdout, stdout=PIPE)
    p2.communicate()[0]
    data = urllib2.urlopen(get_url(s)).read().decode('utf-8')
    soup = BeautifulSoup(data)

    prons = soup.find_all('span', {'class': 'pronounce'})
    if prons:
        for pron in prons:
            text = pron.text.replace(' ', '').replace('\n', '')
            print(text+'\t'),
        print

    content = \
        soup.find('div', {'class': 'results-content', 'id': 'results-contents'})
    definitions = \
        content.find('div', {'class': 'trans-container'}).ul.find_all('li')
    if not definitions:
        definitions = \
            content.find('div', {'class': 'trans-container'}).ul.find_all('span')
    additional = content.find('p', {'class': 'additional'})

    if definitions:
        for define in definitions:
            text = define.text.strip()
            if text:
                print(define.text.replace('\n', '')),
                if text[-1] != '.':
                    print
        if additional:
            text = additional.text.strip()
            text = re.sub(r'\s+', ' ', text)
            if text[0] == '[' and text[-1] == ']':
                print(text)
        print

    word_groups = content.find('div', {'class': 'pr-container more-collapse'})
    word_groups = word_groups.find_all('p', {'class': r'wordGroup'})
    if word_groups:
        print(u'[短语]')
        for group in word_groups:
            if len(group['class']) != 1:
                break
            phras = group.span.a.text.strip()
            text = group.text.replace(phras, '')
            text = re.sub(r'\s+', ' ', text)
            text = text.strip().split(';')
            print(phras+':'),
            for i, t in enumerate(text[1:]):
                print(t.strip()+(';' if i != len(text)-2 else '')),
            print


if __name__ == '__main__':
    if len(sys.argv) > 1:
        for i, s in enumerate(sys.argv[1:]):
            lookup(s)
            if i != len(sys.argv)-2:
                print('-------------------------')
    else:
        while True:
            s = raw_input()
            if s.strip():
                lookup(s.strip())
            if s == '':
                break
