#!/bin/python2
#-*- coding: utf-8 -*-
'''
Python2用有道给的API写的在线命令行词典
'''
import json
import urllib2
import re
import sys


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
    url = 'http://fanyi.youdao.com/openapi.do?keyfrom=tinxing&key=1312427901&type=data&doctype=json&version=1.1&q='
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
    data = urllib2.urlopen(get_url(s)).read()
    if data:
        data = json.loads(data)
        output(data)


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
