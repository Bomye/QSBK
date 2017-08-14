#-*- coding:utf-8 -*-
import re
import urllib2

def url_downloader():#下载器
    page = 1
    url = 'https://www.qiushibaike.com/hot/' + str(page)
    headers = {'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.133 Safari/537.36'}

    try:
        request = urllib2.Request(url,headers = headers)
        response = urllib2.urlopen(request)
        html = response.read()
        #print html
        return html
    except urllib2.URLError,e:
        if hasattr(e,'code'):
            print e.code
        if hasattr(e,'reason'):
            print e.reason
        return



def html_parser():
    content = url_downloader()
    pattern = re.compile('<div class="author clearfix">.*?<h2>(.*?)</h2>.*?<div class="content">.*?<span>(.*?)</span>.*?</a>(.*?)<div class="stats">.*?(\d+)</i>.*?<span class="stats-comments">.*?(\d+)</i>',re.S)
    items = re.findall(pattern,content)

    for item in items:
        haveImg = re.search("img",item[3])
        if not haveImg:
            print item[0]
            print item[1]
            print item[3],item[4]




html_parser()