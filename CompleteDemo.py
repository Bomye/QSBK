__author__ = 'YQ'
#-*- coding:utf-8 -*-

import urllib2
import re

#糗事百科爬虫类
class QSBK:
    #初始化方法，定义一些变量
    def __init__(self):
        self.pageIndex = 1
        self.user_agent = 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.133 Safari/537.36'
        #初始化头信息
        self.headers = {'User-Agent':self.user_agent}
        #存放段子的变量
        self.storeies = []
        #存放程序是否继续运行的变量
        self.enable = False

    #传入某一页的索引 获得页面代码
    def getPage(self,pageIndex):
        url = 'https://www.qiushibaike.com/hot/' + str(pageIndex)
        headers = {'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.133 Safari/537.36'}
        try:
            #构建请求的request
            request = urllib2.Request(url,headers = headers)
            #利用urlopen获取页面代码
            response = urllib2.urlopen(request)
            #将页面转化为UTF-8编码
            html = response.read().decode('utf-8')
            return html
        except urllib2.URLError,e:
            #if hasattr(e,'code'):
                #print e.code
            if hasattr(e,'reason'):
                print u"连接糗事百科失败,错误原因",e.reason
                return None

    #传入某一页代码，返回不带图片的段子列表
    def getPageItems(self,pageIndex):
        pageCode = self.getPage(pageIndex)
        if not pageCode:
            print '页面加载失败....'
            return None
        pattern = re.compile('<div class="author clearfix">.*?<h2>(.*?)</h2>.*?<div class="content">.*?<span>(.*?)</span>.*?</a>(.*?)<div class="stats">.*?(\d+)</i>.*?<span class="stats-comments">.*?(\d+)</i>',re.S)
        items = re.findall(pattern,pageCode)
        #用来存储每页的段子们
        pageStories = []
        for item in items:
            #是否含有图片
            haveImg = re.search("img",item[3])
            #如果不含有图片，把它加入list中
            if not haveImg:
                replaceBR = re.compile('<br/>')
                text = re.sub(replaceBR,"\n",item[1])
                #item[0]是一个段子的发布者，item[1]是内容，item[2]是点赞数,item[4]是评论数
                pageStories.append([item[0].strip(),item[1].strip(),item[3].strip(),item[4].strip()])
        print item[0].strip(),item[1].strip(),item[3].strip(),item[4].strip()
        return pageStories



    #加载并提取页面的内容，加入到列表中
    def loadPage(self):
        #如果当前未看的页数少于2页，则加载新一页
        if self.enable == True:
            if len(self.storeies) < 2:
                #获取新一页
                pageStories = self.getPageItems(self.pageIndex)
                #将该页的段子存放到全局list中
                if pageStories:
                    self.storeies.append(pageStories)
                    #获取玩之后页码索引加一，表示读取下一页
                    self.pageIndex += 1

    #调用该方法，每次敲回车打印输出一个段子
    def getOneStory(self,pageStories,page):
        #便利每一页的段子
        for story in pageStories:
            #等待用户输入
            input = raw_input()
            #每当输入回车一次，判断一下是否要加载新页面
            self.loadPage()
            #如果输入Q则程序结束
            if input == "Q":
                self.enable = False
                return
            print u"第%d页\t发布人:%s\t赞:%s\t评论:%s\n%s" %(page,story[0],story[3],story[4],story[1])

    #开始方法
    def start(self):
        print u"正在读取糗事百科，按回车查看新段子，Q退出"
        #使变量为True，程序可以正常运行
        self.enable = True
        #先加载一夜内容
        self.loadPage()
        #局部变量，控制当前读到第几页
        nowPage = 0
        while self.enable:
            if len(self.storeies) > 0:
                #从全局list中获取一夜的段子
                pageStories = self.storeies[0]
                 #当前读到的页数加一
                nowPage += 1
                #将全局list中第一个元素删除，因为已经取出
                del self.stories[0]
                #输出该页的段子
                self.getOneStory(pageStories,nowPage)



spider = QSBK()
#spider.getPageItems(0)
spider.start()