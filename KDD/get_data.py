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
        response = sess.get(url, proxies=proxy, timeout=20, verify=False)
        # print(response.text)
        return response
    except Exception:
        print('error-on-get-url')


def handle_page(page, i):
    p_j = {}
    article=page.text
    #print(article)
    title = re.findall(r'<div class="entry-content notopmargin">\s+?<h3>(.+?)</h3>', article, re.S)[0]
    p_j['title'] = title
    print(title)
    author = re.findall(r'<strong>(.+?)</strong>', article, re.S)[0]
    author = ' '.join([e.strip() for e in author.split('\n') if e.strip() != ''])
    p_j['author'] = author
    abstract_pdf = re.findall(r'<h4>Abstract</h4>\s+(<div .+?</div>)?\s+(.+?)<a href="(.+?)"', article, re.S)
    abstract=abstract_pdf[0][1]
    abstract = abstract.replace(r'<p>', '\n')
    abstract = abstract.replace(r'</p>', '\n')
    abstract = abstract.replace(r'&lt;', '<')
    abstract = abstract.replace(r'&gt;', '>')
    abstract = abstract.replace(r'&le;', '\leq')
    abstract = abstract.replace(r'&ge;', '\geq')
    abstract = abstract.replace('\n', '\n\n')
    p_j['abstract'] = abstract.strip()
    pdf = abstract_pdf[0][2]
    p_j['pdf'] = pdf
    paper_j[i] = p_j
    with open('paper.json', 'w')as f:
        json.dump(paper_j, f, indent=1)


def handle_fs(fs):
    for i, a in enumerate(fs):
        if str(i + 1) in paper_j:
            continue
        page = get_url(a)
        
        handle_page(page, i + 1)
        time.sleep(1)
        print(i)


def handle_home(text):
    pattern = '<a href="(http://www.kdd.org/kdd2017/papers/view/[^"]+?)">'
    fs = re.findall(pattern, text)
    for a in fs:
        print(a)
    print(len(fs))
    return fs


if __name__ == '__main__':
    if os.path.exists('paper.json'):
        with open('paper.json')as f:
            paper_j = json.load(f)
    url = "http://www.kdd.org/kdd2017/accepted-papers"
    response = get_url(url)
    fs = handle_home(response.text)
    handle_fs(fs)
    with open('paper.json', 'w')as f:
        json.dump(paper_j, f, indent=1)
