import requests
import re
import subprocess
import threading

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
            header = {
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36"
            }
            r = requests.head(webURL, headers=header, verify=False, allow_redirects=True, timeout=5)
            # r.history != [] 就代表r.history有值， 但是这样并不能代表地址跳转成别的页面，我们还要验证他等于https的情况
            webURLs = webURL.replace("http","https") + "/"
            if r.history != [] and r.url != webURLs:
                self.golbalData["WebShell"][webURL]["status_code"] = str(re.findall("\d+",str(r.history[0]))[0])
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

            webURL2 = webURL.split("/")[-1]

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

    def Get_BiliBili_Img_Url(self,golbalData):
        try:
            header = {
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36"
            }
            r = requests.get("https://www.bilibili.com/anime/", headers=header, timeout=5)
            # 获取网页所有HTML标签
            response = r.content.decode("utf-8")
            # 获取包含需要结果页面的DIV标签
            response_DIV = re.findall('<div class="carou-images">(.*?)</div>', response)
            # 获取所需要的所有A标签
            response_A = re.findall('a href="(.*?)"', str(response_DIV))
            # 获取所有需要的DIV标签
            response_IMG = re.findall('img src="(.*?)@', str(response_DIV))
            for i in range(len(response_A)):
                golbalData["BiliBili"][response_A[i]] = response_IMG[i]
        except BaseException as error:
            print("Get_BiliBili_Img_Url----------\n", error)