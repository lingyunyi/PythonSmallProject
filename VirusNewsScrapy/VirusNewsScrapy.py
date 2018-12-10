import requests
import re
import time
class NewsScrapy(object):
    def __init__(self):
        # 全部内容的List
        self.allList = []
        self.headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) Chrome/50.0.2661.102'}
        self.allDict = {}
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
            newsUrl = str(i[0]).replace(i[0], "http://www.cverc.org.cn/head/lesuoruanjian%s" % (url))
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
            newsUrl = str(i[0]).replace(i[0], "http://www.cverc.org.cn%s" % (url))
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
            newsUrl = str(i[0]).replace(i[0], "http://www.cverc.org.cn%s" % (url))
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
                newsUrl = str(i[0]).replace(i[0], "http://www.cverc.org.cn%s" % (url))
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
    def toDict(self):
        self.allDict = {}
        for i in range(0,len(self.allList),2):
            self.allDict[self.allList[i]] = self.allList[i+1]
        return self.allDict
    def allDownLoad(self):
        self.toDict()
        for i in range(len(self.allDict)):
            time.sleep(1)
            try:
                with open("%s.txt" % (list(one.allDict.keys())[i]), "w+") as fp:
                    htmlContent = requests.get(list(one.allDict.values())[i], headers=self.headers,timeout=0.5,verify=False).content.decode('utf-8').replace('<!--内容部分开始-->', "<begin>").replace('<!--内容部分结束-->', "<end>")
                    contentText = re.findall(r'<begin>(.*?)<end>', htmlContent,re.S)
                    out_fir_contentText = str(contentText).replace(r"\r\n", "").replace('<h2 class="subject">', "").replace('&nbsp;', '').replace("<p>", '').replace('</td>', "").replace('div', "").replace(r'\t', "").replace('<td><p align="center"><song><font size="2"><br />', "")
                    out_sen_contentText = out_fir_contentText.replace('</p>', "").replace("</h2>", "").replace("<br/>",'').replace("<a href="">", "").replace('</a>', "").replace('tr', "").replace('</td>', "").replace(r'<td><p align="center"><song><font size="2"><br />', "")
                    out_thr_contentText = out_sen_contentText.replace('<p class="label">', '').replace('<  class="table_style">', '').replace('<table>', "").replace("/span", "").replace('/b',"").replace(' <p class="MsoNormal"><b><span style="font-size: 10.0pt"><b><span style="font-size: 10.0pt"', "")
                    out_for_contentText = out_thr_contentText.replace('<a href="mailto:contact@cverc.org.cn">',"").replace('<a href="mailto:avtest@cverc.org.cn">',"")
                    fp.write(out_for_contentText)
                    fp.close()
            except BaseException:
                print("Connection refused by the server..")
                print("Let me sleep for 5 seconds")
                print("ZZzzzz...")
                time.sleep(5)
                print("Was a nice sleep, now let me continue...")
                continue
        return True
if __name__ == "__main__":
    one = NewsScrapy()
    # 开始爬虫并且直接下载
    # one.saveText()
    # 只启用爬虫不下载
    one.mainStart()
    # 下载大量文件
    one.allDownLoad()
    # one.toDict()
    # print(one.allDict)
