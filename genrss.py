#!/usr/bin/env python3

FILENAME= './posts/index.html'
OUTFILE = './posts/rss.xml'

import sys
from bs4 import BeautifulSoup
import datetime as dt
from email.utils import formatdate

base = 'https://astrologer.cc'

sys.stdout = open(OUTFILE, "w")

def xmlesc(s):
    s = s.replace('&', '&amp;')
    s = s.replace('<', '&lt;')
    s = s.replace('>', '&gt;')
    s = s.replace("'", "&apos;")
    s = s.replace('"', '&quot;')
    return s;

def parse():
    htmldoc = str()
    fp = open(FILENAME)
    htmldoc = fp.read();
    fp.close()
    soup = BeautifulSoup(htmldoc, 'html.parser')
    
    entries = soup.find_all('span')
    i = 0
    posts = list()
    while i < len(entries):
        date = entries[i].string.strip()
        i = i + 1
        link = entries[i].a.attrs['href']
        title = entries[i].a.string
        i = i + 1
        posts.append((date, link, title))
    return posts

def emailDate(date):
    time = dt.datetime.fromisoformat(date)
    time = time + dt.timedelta(hours=12)
    return formatdate(float(time.strftime('%s')))

def output(posts):
    print("""<?xml version="1.0" encoding="utf-8"?>
<rss version="2.0" xmlns:atom="http://www.w3.org/2005/Atom">
   <channel>
      <title>Astrologer</title>
      <link>""" + base + """/posts/</link>
      <description>Blog</description>
      <atom:link href=\"""" + base + """/posts/rss.xml" rel="self" type="application/rss+xml" />
""")
    for post in posts:
        date = post[0]
        link = post[1]
        title = post[2]
        fulllink = base + '/posts/' + link
        content = "<p><a href=\"" + fulllink + "\">" + fulllink + "</a></p>"
        print("<item><title>" + title + "</title>")
        print("<link>" + fulllink + "</link>")
        print("<guid>" + fulllink + "</guid>")
        print("<description>" + xmlesc(content) + "</description>")
        print("<pubDate>" + emailDate(date) + "</pubDate></item>")
    print("""
   </channel>
</rss>
""")

posts = parse()
output(posts)

