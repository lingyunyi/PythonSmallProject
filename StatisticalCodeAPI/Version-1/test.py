import os
import datetime
import random
import socket
import re


def readFile_returnPath(pathFile,pathList):
    '''
        获取传入目录下的所有文件以及目录
    :param pathFile:
    :param pathList:
    :return:
    '''
    # 获取目录文件下的所有文件
    allFiles = os.listdir(pathFile)
    # 遍历所有文件
    for i in range(len(allFiles)):
        try:
            # 获得所有文件的单个文件，并且合并路径
            path = os.path.join(pathFile,allFiles[i])
            # 如果是文件
            if os.path.isfile(path):
                # 判断是否是Excel文件
                if path.split(".")[-1] == "xls" or path.split(".")[-1] == "xlsx":
                    # 加入文件列表
                    pathList.append(path)
                    continue # 跳出此次循环
            # 如果是目录
            if os.path.isdir(path):
                # 再次遍历传入的文件夹
                readFile_returnPath(path,pathList)
        except BaseException as tip:
            print("read-function-BedFalse：",tip)
            continue
    return pathList