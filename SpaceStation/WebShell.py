import requests
import re
import subprocess
import threading
import setting

class webShell(object):
    '''
        内存字典全部配置在配置文件中。
        获取到的内存列表也是从配置文件中获取。

        该类的功能是将内存列表中的所有url连接，进行状态码和FPS值的测试，并将更新到内存字典中
    '''
    def __init__(self):
        if len(setting.Golbals_SQL_Table_Data_List) < 0:
            return
        #   开始逐个处理内存列表中的URL连接
        for i in setting.Golbals_SQL_Table_Data_List:
            self.Get_Web_Status_AND_Web_PING(i[1])
        return

    def Get_Web_Status_AND_Web_PING(self, webURL):
        try:
            # 构造requests命令
            headers = {
                'User-Agent': '"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36'
            }
            r = requests.get("http://%s" % (webURL), headers=headers)
            setting.Golbals_WebUrl_Dict.setdefault(webURL, {"status_code": r.status_code, "ping_value": None})
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

            # 构造ping命令
            command = "ping -c 1 %s" % (webURL)

            p = subprocess.Popen([command],
                                 stdin=subprocess.PIPE,
                                 stdout=subprocess.PIPE,
                                 stderr=subprocess.PIPE, shell=True)

            out = p.stdout.read().decode('utf-8')

            # 提取返回值
            regex = r'time=(.+?)ms'
            ping_results = str(re.findall(regex, out)[0])
            ping_results = ping_results.replace(" ", '')
            if len(ping_results) <= 0:
                ping_results = None
            setting.Golbals_WebUrl_Dict[webURL]["ping_value"] = ping_results
        except BaseException as error:
            print(error)


if __name__ == '__main__':
    pass
