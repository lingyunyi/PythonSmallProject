import os,shutil
import datetime
import random
import tool

import zipfile

class statisticalCodeApi(object):

    def __init__(self):
        # folder Path
        self.folderPath = None
        # logFilePath
        self.logFilePath = None
        # tool
        self.tool = tool.tool()
        # code Number
        self.codeNumber = None
        # Initialization folder
        self.createFolder()
    def createFolder(self):
        '''
            Create folders in specified directories format(time + random string)
        :return:
        '''
        try:
            # get current Path
            currentPath = os.getcwd()
            # create random time + str as folders name
                # get now time
            nowTime = str(datetime.datetime.now().strftime('%Y%m%d%H%M%S'))
                # print( random.choice('tomorrow') )   # 从序列中随机选取一个元素
            randomString = ""
            for i in range(5):
                tempVar = random.choice('abcdefghijklmnopqrstuvwxyz')
                randomString += tempVar
            folderName = nowTime + randomString
                # os.path.sep is path spilt sign
                # Specify folders
            specifyFolders = "fileUpload"
            self.folderPath = currentPath + os.path.sep + specifyFolders + os.path.sep + folderName
            exists_specifyFoldersPath = currentPath + os.path.sep + specifyFolders
            	# if specifyFolders not exists
            if not os.path.exists(exists_specifyFoldersPath):
            	os.makedirs(exists_specifyFoldersPath)
            	# if foldPath not exists
            if not os.path.exists(self.folderPath):
                # create folder
                os.makedirs(self.folderPath)
                self.logFilePath = self.folderPath + os.path.sep + "log.log"
                if not os.path.exists(self.logFilePath):
                    f = open(self.logFilePath,"w")
                    f.close()
            # success
            self.logCenter("createFolder","success","sucess create folder")
        except BaseException as error:
            # write log
            self.logCenter("createFolder", "fail", "%s" %(str(error)))
    def logCenter(self,function,flag="success",content=None):
        '''
            log Center Handle
        :param function:
        :param flag:
        :param reason:
        :return:
        '''
        try:
            f = open(self.logFilePath,"a+")
            ip = self.tool.get_host_ip()
            f.write("%s - - ['%s   %s']  %s" %(ip,function,flag,content))
            f.write("\n")
            f.close()
        except BaseException as error:
            # fail is fail
            f = open(self.logFilePath, "a+")
            ip = self.tool.get_host_ip()
            f.write("%s - - ['%s   %s']  %s" % (ip, "logCenter", "fail", error))
            f.write("\n")
            f.close()
    def decompression(self,filePath):
        '''
            decompression center
            Traverse through all files in the specified directory
        :return:
        '''
        # if file move foler else if zip or tar decompression to foler
        try:
            if os.path.splitext(filePath)[1] == ".tar" or os.path.splitext(filePath)[1] == ".zip":
                if os.path.splitext(filePath)[1] == ".tar":
                    # It's still a string in the past life before it's passed as data,
                    # so string replacement is done here.
                    filePath = filePath.replace("\\", "//")
                    self.folderPath = self.folderPath.replace("\\", "//")
                    self.tool.tar(filePath,self.folderPath)
                if os.path.splitext(filePath)[1] == ".zip":
                    # It's still a string in the past life before it's passed as data,
                    # so string replacement is done here.
                    filePath = filePath.replace("\\","//")
                    self.folderPath = self.folderPath.replace("\\","//")
                    self.tool.zip(filePath,self.folderPath)
                self.logCenter("decompression", "success", "decompression file ok")
            else:
                if os.path.isfile(filePath):
                    # path and file name split
                    shutil.move(filePath,self.folderPath)
                    self.logCenter("decompression", "success", "moving file ok")
        except BaseException as error:
            self.logCenter("decompression", "fail", "%s" % (str(error)))


















if __name__ == "__main__":
    a = statisticalCodeApi()
    a.decompression(r"‪C:\Users\Administrator\Desktop\StatisticalCodeAPI.zip")