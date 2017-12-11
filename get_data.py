#!/usr/bin/env python
# encoding=utf-8
"""
created by maxuewei
"""
import requests
import re
import time
import json
import os

paper_j = {}


def get_url(url):
    user_agent = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5)'
    headers = {'User-Agent': user_agent}
    sess = requests.session()
    sess.headers.update(headers)
    proxy = None
    try:
        response = sess.get(url, proxies=proxy, timeout=10, verify=False)
        # print(response.text)
        return response
    except Exception:
        print('error-on-get-url')


def handle_page(page, i):
    p_j = {}
    article_pattern = '<article class="post-content">(.+?)</article>'
    article = re.findall(article_pattern, page.text, re.S)[0]
    title = re.findall('<h1>([^<]+)</h1>', article, re.S)[0]
    p_j['title'] = title
    author = re.findall('<div id="authors" class="authors">(.+?)</div>', article, re.S)[0]
    author = ' '.join([e.strip() for e in author.split('\n') if e.strip() != ''])
    p_j['author'] = author
    abstract = re.findall('<div id="abstract" class="abstract">(.+?)</div>', article, re.S)[0]
    abstract = abstract.replace(r'&lt;', '<')
    abstract = abstract.replace(r'&gt;', '>')
    abstract = abstract.replace(r'&le;', '\leq')
    abstract = abstract.replace(r'&ge;', '\geq')
    p_j['abstract'] = abstract.replace('\n', '')
    pdf = re.findall('<a href="([^"]+)" target="_blank" onclick="ga\(\'send\', \'event\', \'PDF Downloads\'', article, re.S)[0]
    p_j['pdf'] = pdf
    paper_j[i] = p_j
    with open('paper.json', 'w')as f:
        json.dump(paper_j, f, indent=1)


def handle_fs(fs):
    for i, a in enumerate(fs):
        if str(i + 1) in paper_j:
            continue
        page = get_url(a)
        try:
            handle_page(page, i + 1)
        except Exception:
            print('error',i)
        time.sleep(1)
        print(i)


def handle_home(text):
    pattern = '<a href="([^"]*)" class="btn btn-default btn-xs href_PDF" title="PDF">'
    fs = re.findall(pattern, text)
    for a in fs:
        print(a)
    print(len(fs))
    return fs


if __name__ == '__main__':
    if os.path.exists('paper.json'):
        with open('paper.json')as f:
            paper_j = json.load(f)
    url = "https://2017.icml.cc/Conferences/2017/Schedule?type=Poster"
    response = get_url(url)
    fs = handle_home(response.text)
    handle_fs(fs)
    with open('paper.json', 'w')as f:
        json.dump(paper_j, f, indent=1)
