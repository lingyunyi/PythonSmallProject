import os
import datetime
import random
import socket
import re

listx= []
def rmdir(path,listx):
    # 删除空文件夹
    try:
        while len(listx):
            for s_child in os.listdir(path):
                s_child_path = os.path.join(path, s_child)
                if os.path.isdir(s_child_path):
                    if not os.listdir(s_child_path):
                        listx.append(s_child_path)
                        continue
                    rmdir(s_child_path)
            for delete_file in range(len(listx)):
                os.rmdir(delete_file)
                listx.remove(delete_file)

    except BaseException as error:
        print(error)

rmdir(r'F:\PythonItems\StatisticalCodeAPI\fileUpload\20190726165956tzpqv',listx)
