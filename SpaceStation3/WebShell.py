﻿import requests
import re
import subprocess
import threading
import random
import time
import Sqlmanager

class webShell(object):
    '''
        内存字典全部配置在配置文件中。
        获取到的内存列表也是从配置文件中获取。

        该类的功能是将内存列表中的所有url连接，进行状态码和FPS值的测试，并将更新到内存字典中
    '''
    def __init__(self,golbalData):
        self.golbalData = golbalData
        golbalData["SqlManger"]
        if len(self.golbalData["SqlManger"]) < 0:
            return
        #   开始逐个处理内存列表中的URL连接
        for i in self.golbalData["SqlManger"]:
            url = str(i[1])
            self.golbalData["WebShell"].setdefault(url, {"status_code": "wating...","ping_results": "wating..."})
            try:
                self.Get_Web_Status(url)
                self.Web_PING(url)
            except BaseException as error:
                print(error)
                continue
        return

    def Get_Web_Status(self, webURL):
        print("Get_Web_Status  开始处理  ------------------\n",webURL)
        try:
            r = requests.head(webURL, headers=self.get_request_headers(), verify=False, allow_redirects=True, timeout=5)
            # r.history != [] 就代表r.history有值， 但是这样并不能代表地址跳转成别的页面，我们还要验证他等于https的情况
            web_perfix = webURL.split(":")[0]
            # 将所有数据都处理成HTTPS，看看是不是只转换了HTTPS
            webURLs = webURL.replace(web_perfix,"https") + "/"
            # 如果有值就代表，并且改造过后的https还不相等的话，就代表是真的重定向了。
            if r.history != [] and r.url != webURLs:
                self.golbalData["WebShell"][webURL]["status_code"] = str(re.findall("\d+", str(r.history[0]))[0])
            else:
                self.golbalData["WebShell"][webURL]["status_code"] = r.status_code
            r.close()

            # # 构造Curl命令
            # command = "curl -I %s 2>/dev/null|awk 'NR==1{print $2}'" %(webURL)
            # p = subprocess.Popen([command],
            #                      stdin=subprocess.PIPE,
            #                      stdout=subprocess.PIPE,
            #                      stderr=subprocess.PIPE, shell=True)
            #
            # out = p.stdout.read().decode('utf-8')
            # out.replace("\n","")
            # if len(out) <= 0:
            #     out = None
            # Golbals_WebUrl_Dic.setdefault(webURL, {"status_code": out, "ping_value": None})

        except BaseException as error:
            print("Get_Web_Status----------\n",error)

    def Web_PING(self,webURL):
        print("Web_PING  开始处理  ------------------\n", webURL)
        try:
            # 构造ping命令
            # http: // www.baidu.com 带有HTTP:ping不了，解剖才行

            webURL2 = webURL.split("/")[2]

            command = "ping -c 2 %s" % (webURL2)

            p = subprocess.Popen([command],
                                 stdin=subprocess.PIPE,
                                 stdout=subprocess.PIPE,
                                 stderr=subprocess.PIPE, shell=True)

            out = p.stdout.read().decode('utf-8')


            # 提取返回值
            regex = r'time=(.+?)ms'
            ping_results = str(re.findall(regex, out)[0])
            ping_results = ping_results.replace(" ", '')
            self.golbalData["WebShell"][webURL]["ping_results"] = ping_results
        except BaseException as error:
            print("Web_PING222----------error:\n",error)


    def All_Bilibili_Img_Url(self):
        All_Url_List = [
            "https://www.bilibili.com/anime/",
            "https://www.bilibili.com/guochan/",
            # "https://www.bilibili.com/tv/",
            "https://www.bilibili.com/movie/",
            # "https://www.bilibili.com/documentary/"

        ]
        return All_Url_List

    def Get_BiliBili_Img(self,golbalData):
        All_Url_List = self.All_Bilibili_Img_Url()
        for bilibiliUrl in All_Url_List:
            try:
                r = requests.get(bilibiliUrl, headers=self.get_request_headers(), timeout=5)
                # 获取网页所有HTML标签
                response = r.content.decode("utf-8")
                # 获取包含需要结果页面的DIV标签
                response_DIV = re.findall('<div class="carou-images">(.*?)</div>', response)
                # 获取所需要的所有A标签
                response_A = re.findall('a href="(.*?)"', str(response_DIV))
                # 获取所有需要的DIV标签
                response_IMG = re.findall('img src="(.*?)@', str(response_DIV))
                for i in range(len(response_A)):
                    print("获得URL：%s" % (response_A[i]))
                    if i < 6:
                        golbalData["BiliBili"][response_A[i]] = response_IMG[i]
            except BaseException as error:
                print("Get_BiliBili_Img_Url----------\n", error)

    def get_request_headers(self):
        # 用户代理User-Agent列表
        USER_AGENTS = [
            "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36",
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:69.0) Gecko/20100101 Firefox/69.0"
        ]

        headers = {
            "User-Agent": random.choice(USER_AGENTS),
        }
        return headers




class ForGetAllUrlAndTitle(webShell):
    '''

    '''
    def __init__(self,xxx_xxx_xxx):
        # 输入某个域名
        self.domain = xxx_xxx_xxx
        # 类变量 set集合 目的是去掉重复的url
        self.getUrlSet = set()
        # 最终数据列表，用于传入其他class insert到数据库中
        self.finalList = []
        # 直接启动获取所有URL的函数
        self.getAllUrl_into_Set()
        self.getAllUrl_title()


    def getAllUrl_into_Set(self):
        domain = self.domain
        '''
            · 进行第一次请求获取该网站的所有 Url 连接
            · 将所有URL连接存入 SET集合 中
        '''

        try:
            # 发送一次 GET 请求
            respond = requests.get(domain, headers=self.get_request_headers(), verify=False, allow_redirects=True, timeout=5)
            # 将该请求转变成HTML内容
            html = respond.content.decode("utf-8")
            # 使用re正则提取所有URL
            allUrl = re.findall('http[s]?://(?:(?!http[s]?://)[a-zA-Z]|[0-9]|[$\-_@.&+/]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+',html)
            allUrl = map(self.mainDomain,allUrl)
            for i in allUrl:
                if i != None:
                    self.getUrlSet.add(i)
        except BaseException as Error:
            print(Error)
        return self.domain
    def get_request_headers(self):
        '''
            直接使用父类方法
        '''
        super().get_request_headers()
    def mainDomain(self,url):
        '''
            只要主域名
        '''
        if str(url).count("/") <= 3:
            return url
    def getAllUrl_title(self):
        '''
            将所有URL连接中的URL网站里面的标题提取出来
        '''
        for i in self.getUrlSet:
            try:
                # 发送一次 GET 请求
                respond = requests.get(i, headers=self.get_request_headers(), verify=False, allow_redirects=True,timeout=5)
                # 将该请求转变成HTML内容
                html = respond.content.decode("utf-8")
                # 使用re正则提取所有URL
                title = re.findall('<title>(.*?)</title>',html)
                if str(title) != " ":
                    title = str(title).replace("&#8211","")
                    if str(i).endswith("/"):
                        i = i[:-1]
                    self.finalList.append([i,"HH",title,time.strftime('%Y-%m-%d',time.localtime(time.time())),"admin",0])
            except BaseException as Error:
                print(Error)
                continue








if __name__ == "__main__":
    getAll = ForGetAllUrlAndTitle('http://other1.xyz')
    getAll.getAllUrl_into_Set()
    sqlmanager = Sqlmanager.SqlManger(golbalData=None)
    for i in getAll.finalList:
        sqlmanager.insert_into_webdata(i)