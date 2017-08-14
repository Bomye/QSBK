# -*- coding:UTF-8 -*-
__author__ = 'YQ'


import urllib
import urllib2
import re
import thread
import time

class QSBK:
    def __init__(self):
        self.pageIndex = 1
        self.user_agent = 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.133 Safari/537.36'
        self.headers = {'User-Agent':self.user_agent}
        #存放段子的变量，每一个元素是每一页的段子
        self.stories = []
        #存放程序是否继续运行的变量
        self.enable = False

    #获取页面源码
    def getPage(self,pageIndex):
        try:
            url = 'https://www.qiushibaike.com/hot/' + str(pageIndex)
            request = urllib2.Request(url,headers = self.headers)
            response = urllib2.urlopen(request)
            pageCode = response.read().decode('utf-8')
            return pageCode
        except urllib2.URLError,e:
            if hasattr(e,"reason"):
                print u"连接糗事百科失败,错误原因",e.reason
                return None

    #传入页码，返回不带图片的段子列表
    def getPageItems(self,pageIndex):
        pageCode = self.getPage(pageIndex)
        if not pageCode:
            print '页面加载失败......'
            return None
        pattern = re.compile('<div class="author clearfix">.*?<h2>(.*?)</h2>.*?<div class="content">.*?<span>(.*?)</span>.*?</a>(.*?)<div class="stats">.*?(\d+)</i>.*?<span class="stats-comments">.*?(\d+)</i>',re.S)
        items = re.findall(pattern,pageCode)
        #用来存储每页的段子
        pageStories = []
        for item in items:
            haveImg = re.search("img",item[3])
            if not haveImg:
                replaceBR = re.compile('<br/>')
                #替换
                text = re.sub(replaceBR,"\n",item[1])
                #item[0]是一个段子的发布者，item[1]是内容，item[3]是点赞数量,item[4]是评论数量
                pageStories.append([item[0].strip(),text.strip(),item[3].strip(),item[4].strip()])
                #for i in pageStories:
                    #print i
        return pageStories
   #加载并提取页面的内容，加入到列表中
    def loadPage(self):
        #如果当前未看的页数少于2页，则加载新一页
        if self.enable == True:
            if len(self.stories) < 2:
                #获取新一页
                pageStories = self.getPageItems(self.pageIndex)
                #将该页的段子存放到全局list中
                if pageStories:
                    self.stories.append(pageStories)
                    #获取完之后页码索引加一，表示下次读取下一页
                    self.pageIndex += 1

    #调用该方法，每次敲回车打印输出一个段子
    def getOneStory(self,pageStories,page):
        for story in pageStories:
            input = raw_input()
            self.loadPage()
            if input == "Q":
                self.enable = False
                return
            print u"第%d页\t发布人:%s\t赞:%s\t评论:%s\n%s" %(page,story[0],story[2],story[3],story[1])

    #开始方法
    def start(self):
        print u'正在读取糗事百科，按回车查看新段子，Q退出'
        self.enable = True
        self.loadPage()
        nowPage = 0
        while self.enable:
            if len(self.stories) > 0:
                pageStories = self.stories[0]
                nowPage += 1
                del self.stories[0]
                self.getOneStory(pageStories,nowPage)


spider = QSBK()
spider.start()