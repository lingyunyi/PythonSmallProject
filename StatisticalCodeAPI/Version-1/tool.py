import socket
import zipfile,tarfile
import re
class tool(object):

    def get_host_ip(self):
        """
        查询本机ip地址
        :return:
        """
        try:
            s = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
            s.connect(('8.8.8.8',80))
            ip=s.getsockname()[0]
        finally:
            s.close()
        return ip

    def zip(self,filePath,folderPath):
        # It is necessary to determine whether it is a disc symbol of windos system or not.
        # if ":" in filePath:
        #     filePath = filePath.split(":")[0] + ":" + filePath.split(":")[-1]
        # if ":" in folderPath:
        #     folderPath = folderPath.split(":")[0] + ":" + folderPath.split(":")[-1]
        filePath = filePath.replace('\u202a',"")
        folderPath = folderPath.replace('\u202a',"")
        z = zipfile.ZipFile(filePath, 'r')
        z.extractall(folderPath)
        z.close()

    def tar(self,filePath,folderPath):
        # It is necessary to determine whether it is a disc symbol of windos system or not.
        # if ":" in filePath:
        #     filePath = filePath.split(":")[0] + ":" + filePath.split(":")[-1]
        # if ":" in folderPath:
        #     folderPath = folderPath.split(":")[0] + ":" + folderPath.split(":")[-1]
        filePath = filePath.replace('\u202a', "")
        folderPath = folderPath.replace('\u202a', "")
        t = tarfile.open(filePath, 'r')
        t.extractall(folderPath)  # 可设置解压地址
        t.close()
