import pickle
import time
import threading


class ReportingCenter(object):
    '''
        报警、上报中心，处理一些奇怪的异常，或者上报一些奇怪的数据
    '''
    _instance_lock = threading.Lock()

    def __new__(cls, *args, **kwargs):
        '''
        单例模式，确保每一次启动该类都是原先的类，原先的类所运行的内容并不会产生任何变化
        '''
        if not hasattr(ReportingCenter, "_instance"):
            with ReportingCenter._instance_lock:
                if not hasattr(ReportingCenter, "_instance"):
                    ReportingCenter._instance = object.__new__(cls)
        return ReportingCenter._instance


    def __init__(self,tempLostURL):
        self.tempLostURL = tempLostURL
        self.TempLostURL(self.tempLostURL)



    def TempLostURL(self,Data):
        '''
            将临时失效URL存入文件中
        '''
        WriteList = []
        try:
            fileRead = open('TempTxt/TempLostURL.txt', 'rb')
            # 打开序列化过后的文件，进行反序列化处理
            ComparativeList = pickle.load(fileRead)
            fileRead.close()
        except:
            ComparativeList = []
        finally:
            # 如果是新数据则写入，不是新数据则不写入
            for i in Data:
                if i not in ComparativeList:
                    WriteList.append(i)
            if WriteList != []:
                for i in WriteList:
                    ComparativeList.append(i)
        fileOpen = open('TempTxt/TempLostURL.txt', 'wb')
        pickle.dump(ComparativeList, fileOpen)
        fileOpen.close()


