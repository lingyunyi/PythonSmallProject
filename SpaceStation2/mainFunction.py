import WebShell
import Sqlmanager
import pickle
import threading
import time,random

golbalData = {}

def DataMaker():
    while True:
        # 引用全局变量作为数据存储站
        global golbalData
        '''
            第一步，首先将，数据存储在传入Sqlmanager中进行处理获得相应来自于数据库的数据，做成JSon形式，方便后续处理。
            第二部，将获得的数据，传入Webshell中进行处理。将得到的数据一并传入全局数据中
        :return: 
        '''
        # 全局数据存储站传入，等待获得从数据库中提取到的数据
        # 再次之前，现在数据格式处理好，即将要存储的数据是，来源于数据库的数据，格式为，mysqlData = []
        golbalData["SqlManger"] = []
        golbalData["Users"] = []
        SQL_manager = Sqlmanager.SqlManger(golbalData)
        # 到这里，已经获得来源于数据库中所有的数据，格式为golbalData["mysqlData"] = ["111","222","333","444"]
        # 接下来数据交由WebShell管理，并将数据也传入golbalData这个大字典中。
        golbalData["WebShell"] = {}
        Web_Shell = WebShell.webShell(golbalData)
        # 获取BILIBILI的IMG数据，用来设计HTML
        golbalData["BiliBili"] = {}
        Web_Shell.Get_BiliBili_Img(golbalData)
        # 到这里，又获得了经过WebShell处理的数据，这样数据就收集齐了。接下来就是序列化之后，导入文件中。
        fileOpen = open('TemplateData.txt', 'wb')
        pickle.dump(golbalData, fileOpen)
        fileOpen.close()
        # 好了，数据经过pickle序列化之后，已经成功存入临时文件中。
        print(golbalData)
        time.sleep(random.randint(5,10) * 60)


def IntervalProduction():
    '''
        定时启动，定时洗刷数据。
        使用子进程进行数据处理
    :return:
    '''
    # 生成一个子进程
    t = threading.Thread(target=DataMaker)
    # 子进程启动
    t.start()

if __name__ == "__main__":
    IntervalProduction()


