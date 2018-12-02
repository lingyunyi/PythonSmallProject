import requests
import re
import time
class NewsScrapy(object):
    def __init__(self):
        # 全部内容的List
        self.allList = []
    def virusDynamics2017News(self):
        '''
            2017年的病毒动态新闻
        :return:
        '''
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) Chrome/50.0.2661.102'}
        url = "http://www.cverc.org.cn/content/bddt2017.htm"
        # 提交搜索数据获得回应
        respond = requests.get(url, headers=headers)
        # 获取回应中的html代码
        Html = respond.content.decode("utf-8")
        # 获的其中的所有连接以及内容
        HtmlcontentList = re.findall(r'<li><a href="(.*?)">(.*?)</a>', Html)
        resultsList = []
        for i in HtmlcontentList:
            url = i[0].replace("..","")
            newsUrl = str(i[0]).replace(i[0], "http://www.cverc.org.cn%s"%(url))
            newsName = i[1].replace("&nbsp; ","")
            resultsList.extend([newsName,newsUrl])
        return resultsList
    def virusDynamics2018News(self):
        '''
            2018年的新闻动态新闻
        :return:
        '''
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) Chrome/50.0.2661.102'}
        url = "http://www.cverc.org.cn/content/bddt2018.htm"
        # 提交搜索数据获得回应
        respond = requests.get(url, headers=headers)
        # 获取回应中的html代码
        Html = respond.content.decode("utf-8")
        HtmlcontentList = re.findall(r'<li><a href="(.*?)">(.*?)</a>', Html)
        resultsList = []
        for i in HtmlcontentList:
            url = i[0].replace("..", "")
            newsUrl = str(i[0]).replace(i[0], "http://www.cverc.org.cn%s" % (url))
            newsName = i[1].replace("&nbsp; ", "")
            resultsList.extend([newsName, newsUrl])
        return resultsList
    def blackmailSoftwareNews(self):
        '''
            勒索软件新闻
        :return:
        '''
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) Chrome/50.0.2661.102'}
        url = "http://www.cverc.org.cn/head/lesuoruanjian/mulu.htm"
        # 提交搜索数据获得回应
        respond = requests.get(url, headers=headers)
        # 获取回应中的html代码
        Html = respond.content.decode("utf-8")
        HtmlcontentList = re.findall(r'<li><a href="(.*?)">(.*?)</a>', Html)
        resultsList = []
        for i in HtmlcontentList:
            url = i[0].replace("..", "")
            newsUrl = str(i[0]).replace(i[0], "http://www.cverc.org.cn/head/lesuoruanjian/%s" % (url))
            newsName = i[1].replace("&nbsp; ", "")
            resultsList.extend([newsName, newsUrl])
        return resultsList
    def centerDynamicsNews(self):
        '''
            中心动态
        :return:
        '''
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) Chrome/50.0.2661.102'}
        url = "http://www.cverc.org.cn/index.htm"
        # 提交搜索数据获得回应
        respond = requests.get(url, headers=headers)
        # 获取回应中的html代码
        Html = respond.content.decode("utf-8")
        HtmlcontentList = re.findall(r'<li><a href="(.*?)">(.*?)</a>', Html)
        resultsList = []
        for i in HtmlcontentList:
            url = i[0].replace("..", "")
            newsUrl = str(i[0]).replace(i[0], "http://www.cverc.org.cn/%s" % (url))
            newsName = i[1].replace("&nbsp; ", "")
            resultsList.extend([newsName, newsUrl])
        return resultsList
    def testResultNews(self):
        '''
            检验结果网站
        :return:
        '''
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) Chrome/50.0.2661.102'}
        url = "http://www.cverc.org.cn//jianyan/jianyanjieguo.htm"
        # 提交搜索数据获得回应
        respond = requests.get(url, headers=headers)
        # 获取回应中的html代码
        Html = respond.content.decode("utf-8")
        HtmlcontentList = re.findall(r'<li><a href="(.*?)">(.*?)</a>', Html)
        resultsList = []
        for i in HtmlcontentList:
            url = i[0].replace("..", "")
            newsUrl = str(i[0]).replace(i[0], "http://www.cverc.org.cn/%s" % (url))
            newsName = i[1].replace("&nbsp; ", "")
            resultsList.extend([newsName, newsUrl])
        return resultsList
    def forensicsProductsNews(self):
        '''
            取证产品
        :return:
        '''
        resultsList = []
        for i in [2013,2014,2015]:
            headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) Chrome/50.0.2661.102'}
            url = "http://www.cverc.org.cn/head/quzhchanpin/quzhchanpin%s.htm"%(str(i))
            # 提交搜索数据获得回应
            respond = requests.get(url, headers=headers)
            # 获取回应中的html代码
            Html = respond.content.decode("utf-8")
            HtmlcontentList = re.findall(r'<li><a href="(.*?)">(.*?)</a>', Html)
            for i in HtmlcontentList:
                url = i[0].replace("..", "")
                newsUrl = str(i[0]).replace(i[0], "http://www.cverc.org.cn/head/quzhchanpin/%s" % (url))
                newsName = i[1].replace("&nbsp; ", "")
                resultsList.extend([newsName, newsUrl])
        return resultsList
    def saveText(self):
        '''
            文件保存
        :return:
        '''
        self.mainStart()
        fp = open("%s.txt"%(int(time.time())),"w+",encoding="utf-8")
        for i in self.allList:
            fp.write(i)
            fp.write("\n")
        fp.close()
        return True
    def mainStart(self):
        '''
            多层爬虫启动
        :return:
        '''
        start1 = self.virusDynamics2017News()
        self.allList.extend(start1)
        start2 = self.virusDynamics2018News()
        self.allList.extend(start2)
        start3 = self.blackmailSoftwareNews()
        self.allList.extend(start3)
        start4 = self.centerDynamicsNews()
        self.allList.extend(start4)
        start5 = self.testResultNews()
        self.allList.extend(start5)
        start6 = self.forensicsProductsNews()
        self.allList.extend(start6)
        return True
if __name__ == "__main__":
    one = NewsScrapy()
    # 开始爬虫并且直接下载
    one.saveText()
    # 只启用爬虫不下载
    # one.mainStart()
    # 开启爬虫并输出文件
    # print(one.allList)
