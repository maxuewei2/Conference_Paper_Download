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
sss=r"""
\documentclass{article}
\usepackage{geometry}
\geometry{a4paper,centering,scale=0.8}
\usepackage{listings}
\usepackage{color}
\usepackage{amsmath}
\usepackage{amssymb}
%\usepackage{hyperref}
\definecolor{lightgray}{gray}{0.9}

\lstset{
    showstringspaces=false,
    basicstyle=\ttfamily,
    keywordstyle=\color{blue},
    commentstyle=\color[grey]{0.6},
    stringstyle=\color[RGB]{255,150,75}
}

\newcommand{\inlinecode}[2]{\colorbox{lightgray}{\lstinline[language=#1]$#2$}}
\newcommand{\incode}[1]{\colorbox{lightgray}{\texttt{#1}}}

\usepackage{hyperref}
\hypersetup{
    colorlinks=true,
    linkcolor=blue,
    filecolor=black,      
    urlcolor=blue,
    bookmarks=true,
    bookmarksopen=true,
}

\usepackage[depth=4,open]{bookmark}% Show up to level 4 (\paragraph) in bookmarks

\setcounter{tocdepth}{3}% Show up to level 3 (\subsubsection) in ToC


\begin{document}


%\tableofcontents
"""

paper_j={}

def get_url(url):
    user_agent = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5)'
    headers = {'User-Agent': user_agent}
    sess = requests.session()
    sess.headers.update(headers)
    proxy=None
    try:
        response = sess.get(url, proxies=proxy, timeout=10, verify=False)  
        #print(response.text)  
        return response
    except Exception:
        print('wrong')
re_em=re.compile('<em>([^<]+?)</em>')
def handle_page(page,i):
    p_j={}
    pattern='<article class="post-content">(.+?)</article>'
    fs=re.findall(pattern,page.text,re.S)
    article=fs[0]
    title=re.findall('<h1>([^<]+)</h1>',article,re.S)[0]
    #title=str(i)+". "+title
    p_j['title']=title
    stitle="\subsection*{"+title+"}\n"
    bookmark=r'\hypertarget{title_'+str(i)+'}{}\n'
    bookmark+=r'\bookmark[level=section,dest=title_'+str(i)+']{'+str(i)+'. '+title+'}'
    author=re.findall('<div id="authors" class="authors">(.+?)</div>',article,re.S)[0]
    author=' '.join([e.strip() for e in author.split('\n') if e.strip()!=''])
    p_j['author']=author
    author=r"\footnotesize{\textit{"+author+"}}\n"
    author=r'\begin{quote}'+'\n'+author+'\end{quote}\n'
    abstract=re.findall('<div id="abstract" class="abstract">(.+?)</div>',article,re.S)[0]+'\n'
    abstract=abstract.replace(r'&lt;','<')
    abstract=abstract.replace(r'&gt;','>')
    abstract=abstract.replace(r'&le;','\leq')
    abstract=abstract.replace(r'&ge;','\geq')
    p_j['abstract']=abstract.replace('\n','')
    abstract=re_em.sub(r'\\textit{\1}',abstract)
    abstract=r'\begin{quote}'+'\n'+abstract+'\end{quote}\n'
    pdf=re.findall('<a href="([^"]+)" target="_blank" onclick="ga\(\'send\', \'event\', \'PDF Downloads\'',article,re.S)[0]
    p_j['pdf']=pdf
    pdf=r"\href{"+pdf+"}{pdf}\n"
    paper_j[i]=p_j
    with open('page.tex','a')as f:
        f.write('\n'.join([stitle,bookmark,author,abstract,pdf,'']))
    with open('paper.json','w')as f:
        json.dump(paper_j,f,indent=1)

def handle_fs(fs):
    with open('page.tex','a')as f:
        f.write(sss)
    for i,a in enumerate(fs):
        if i+1 in paper_j:
            continue
        page=get_url(a)
        handle_page(page,i+1)
        time.sleep(1)
        print(i)
    with open('page.tex','a')as f:
        f.write('\end{document}')
    
        
def handle_home(text):
    pattern='<a href="([^"]*)" class="btn btn-default btn-xs href_PDF" title="PDF">'
    fs=re.findall(pattern,text)
    for a in fs:
        print(a)
    print(len(fs))
    return fs
    
if __name__=='__main__':
    if os.path.exists('paper.json'):
        with open('paper.json')as f:
            paper_j=json.load(f)
    url="https://2017.icml.cc/Conferences/2017/Schedule?type=Poster"
    response = get_url(url)  
    fs=handle_home(response.text)
    handle_fs(fs)
    with open('paper.json','w')as f:
        json.dump(paper_j,f,indent=1)
