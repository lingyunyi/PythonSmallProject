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
        # 解压文件的路径
        self.decompression_file_path = None
        # file path list
        self.pathList = []
        # code file all lines
        self.code_all_lines = 0
        # code file type
        self.codeFileTypeList = [
            "html","css","js","py"
        ]
        self.ignorefile = [
            "txt",
        ]
        self.decompression_E = [
            'zip','tar'
        ]
        self.emptydir = []
    def mainStart(self,path):
        '''
        启动函数
        :return:
        '''
        if path.split('.')[-1] not in self.decompression_E:
            exit('暂为支持该扩展文件......')
        # 解压文件的路径开始赋值
        self.decompression_file_path = path
        # 首先自动创建所属文件夹
        self.createFolder()
        # 解压传入的文件到指定目录
        self.decompression(filePath=self.decompression_file_path)
        # 销毁掉源解压文件
        self.destroying()
        # 取出指定目录下的所有代码文件，传入的开始查询参数是指定的文件
        self.file_path_list(self.folderPath)
        # 最终获取所有代码数量
        self.code_lines_Number()
        # 删除所有空文件
        self.rmdir(path=self.folderPath)
        # 删除所有空文件
        self.rmdirs()
        # 最后记录一次代码数量
        self.logCenter("code_lines_Number", "success", "%s" % (self.code_all_lines))
        return self.code_all_lines
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
        self.filePath = None
        # if file move foler else if zip or tar decompression to foler
        try:
            if os.path.splitext(filePath)[1] in ".tar.zip":
                # 在这里不得不用中文讲解一下，不知道是BUG的问题，还是系统问题。
                # 有个隐藏的字符串得去除，不然BUG问题贼多。
                filePath = filePath.replace('\u202a', "").replace("\\", "//")
                self.folderPath = self.folderPath.replace('\u202a', "").replace("\\", "//")
                if os.path.splitext(filePath)[1] == ".tar":
                    # It's still a string in the past life before it's passed as data,
                    # so string replacement is done here.
                    self.tool.tar(filePath,self.folderPath)
                    self.filePath = filePath
                if os.path.splitext(filePath)[1] == ".zip":
                    # It's still a string in the past life before it's passed as data,
                    # so string replacement is done here.
                    self.tool.zip(filePath,self.folderPath)
                    self.filePath = filePath
                self.logCenter("decompression", "success", "decompression file ok")
            else:
                if os.path.isfile(filePath):
                    # path and file name split
                    shutil.move(filePath,self.folderPath)
                    self.logCenter("decompression", "success", "moving file ok")
        except BaseException as error:
            self.logCenter("decompression", "fail", "%s" % (str(error)))

    def destroying(self):
        '''
            Destroying documents
        :return:
        '''
        try:
            if self.filePath != None and os.path.isfile(self.filePath):
                # Destroying documents
                os.remove(self.filePath)
                self.logCenter("Destroying", "success", "Destroying file yes")
        except BaseException as error:
            self.logCenter("Destroying", "fail", "%s" % (str(error)))

    def file_path_list(self,folderPath):
        '''
            获取指定文件下面的所有代码文件
        :return:
        '''
        try:
            allFiles = os.listdir(folderPath)
            # 遍历所有文件
            for i in range(len(allFiles)):
                # 获得所有文件的单个文件，并且合并路径
                path = os.path.join(folderPath, allFiles[i])
                path = path.replace('\u202a', "").replace("\\", "//")
                # 如果是文件
                if os.path.isfile(path):
                    if path.split(".")[-1] in self.codeFileTypeList:
                        # 加入文件列表
                        self.pathList.append(path)
                        self.logCenter("file_path_list", "success", "%s" %(os.path.basename(path)))
                        continue  # 跳出此次循环
                    else:
                        if path.split(".")[-1] not in self.ignorefile:
                            # 如果不是代码文件也不是忽视文件
                            os.remove(path)
                # 如果是目录
                if os.path.isdir(path):
                    # 再次遍历传入的文件夹
                    self.file_path_list(path)
        except BaseException as error:
            self.logCenter("file_path_list", "fail", "%s" % (str(error)))

    def code_lines_Number(self):
        '''
         get code line
        :return:
        '''
        for fileName in self.pathList:
            try:
                f = open(fileName,"r",encoding="utf-8")
                for index, line in enumerate(f):
                    self.code_all_lines += 1
                f.close()
            except BaseException as error:
                self.logCenter("code_lines_Number", "fail", "%s" % (str(error)))
                continue
        self.logCenter("code_lines_Number", "success", "%s" % (self.code_all_lines))
    def rmdir(self,path):
        # 删除空文件夹
        try:
            for s_child in os.listdir(path):
                s_child_path = os.path.join(path,s_child)
                if os.path.isdir(s_child_path):
                    if not os.listdir(s_child_path):
                        os.rmdir(s_child_path)
                        self.logCenter("rmdir", "success", "%s" % (os.path.basename(s_child_path)))
                        continue
                    else:
                        self.emptydir.append(s_child_path)
                    self.rmdir(s_child_path)
        except BaseException as error:
            self.logCenter("rmdir", "fail", "%s" % (str(error)))

    def rmdirs(self):
        for dir in self.emptydir:
            try:
                os.removedirs(dir)
                self.logCenter("rmdirs", "success", "%s" % (os.path.basename(dir)))
            except BaseException as error:
                continue

if __name__ == "__main__":
    path = str(input("BigTip：请输入路径 :"))
    getCodeNumber = statisticalCodeApi()
    print("您写得代码数量共为:%s"%(getCodeNumber.mainStart(path)))

