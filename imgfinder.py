# !/usr/bin/env python3
# -*- coding: utf-8 -*-
'''
由于依赖了urllib.parsem模块，该脚本暂时只支持python3+。

使用方式：
1. 导出一篇印象笔记中的md笔记，导出的内容包含两部分:
    导出目录
    ├── note.resources
    └── note.html
2. 在印象笔记中复制该md文本，并保存到导出目录下
3. 执行此程序:
    python3 imgfinder.py 导出目录路径
'''

import sys
import os
from urllib import parse
import re

def get_note(export_dir):
    note_html = None
    note_md = None
    files = os.listdir(export_dir)
    for f in files:
        if f.endswith('.html'):
            note_html = f
        if f.endswith('.md'):
            note_md = f
    return note_html, note_md


if len(sys.argv) < 2:
    print('需要指定笔记导出目录路径!')
    sys.exit(-1)
export_dir = sys.argv[1]
note_html, note_md = get_note(export_dir)
if note_html is None or note_md is None:
    print('未能找到html笔记和md笔记')
    sys.exit(-2)

img_urls = []
with open(export_dir + '/' + note_html, 'r') as f_note_html:
    lines = f_note_html.readlines()
    for line in lines:
        if 'img src=' in line:
            img_url = line.split('img src=')[1].split('"')[1]
            img_urls.append(img_url)
# 关于url解码, 参见: https://www.cnblogs.com/jessicaxu/p/7977277.html
img_urls = [parse.unquote(url) for url in img_urls]

with open(export_dir + '/' + note_md, 'r') as f_note_md:
    lines = f_note_md.readlines()
    img_num = 0
    for line in lines:
        if '(evernotecid:' in line:
            print(line.split('(evernotecid:')[0]+'(%s)' % img_urls[img_num], end='')
            img_num = img_num + 1
        else:
            print(line, end='')



