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
import sys

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

\setcounter{secnumdepth}{0}
\title{\textbf{Accepted Papers}}
\begin{document}
\addcontentsline{toc}{section}{Accepted Papers}
\maketitle
\tableofcontents
\pagebreak
"""


paper_j={}
re_em=re.compile('<em>([^<]+?)</em>')

def handle_one(i,p_j):
    title=p_j['title']
    author=p_j['author']
    abstract=p_j['abstract']
    pdf=p_j['pdf']
    #title=title.replace(r'&',r'\&')
    title=str(i)+". "+title    
    stitle="\subsection{"+title+"}\n"
    bookmark=r'\hypertarget{title_'+str(i)+'}{}\n'
    bookmark+=r'\bookmark[level=section,dest=title_'+str(i)+']{'+title+'}'
    author=r"\footnotesize{\textit{"+author+"}}\n"
    author=r'\begin{quote}'+'\n'+author+'\n\end{quote}\n'
    #author=author.replace(r'&',r'\&')
    abstract=re_em.sub(r'\\textit{\1}',abstract)
    #abstract=abstract.replace(r'&',r'\&')
    abstract=r'\begin{quote}'+'\n'+abstract+'\n\end{quote}\n'
    pdf=r"\href{"+pdf+"}{"+pdf+"}\n"
    with open(tex_filename,'a')as f:
        f.write('\n'.join([stitle,author,abstract,pdf,'']))
        
if __name__=='__main__':
    args=sys.argv
    if len(args)!=4:
        print('error: args not given.\n\tie. python generate_tex.py KDD/paper.json KDD/paper.tex "KDD Accepted Papers"')
        exit(1)
    json_filename=args[1]
    tex_filename=args[2]
    sss=sss.replace('Accepted Papers',args[3])
    if not os.path.exists(json_filename):
        print('error: data file not found.')
        exit(1)    
    json_filename=os.path.abspath(json_filename)
    tex_filename=os.path.abspath(tex_filename)
    
    with open(json_filename)as f:
        paper_j=json.load(f)
    with open(tex_filename,'w')as f:
        f.write(sss)
    for k in sorted([int(x) for x in list(paper_j.keys())]):
        handle_one(k,paper_j[str(k)])
    with open(tex_filename,'a')as f:
        f.write('\end{document}')
