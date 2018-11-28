# 导入pymysql包
import pymysql
import time
import xlrd
import re
import os
class IndexSql(object):
    def __init__(self,serverIP="localhost"):
        self.phone_pat = re.compile('^(13\d|14[5|7]|15\d|166|17[3|6|7]|18\d)\d{8}$')
        self.serverIP = str(serverIP)
    # 定义一个连接数据库函数
    def connect(self):
        # connent(参数列表[“IP地址”，“数据库账号”， “数据库密码”， “数据库名称”])
        self.db = pymysql.connect(self.serverIP, "root", "root", "phone")
        # 使用cursor游标，创建一个游标对象cursor
        self.cursor = self.db.cursor()
        return True
    # 定义一个关闭数据库的函数
        # 游标关闭
    def close(self):
        self.cursor.close()
        # 数据库关闭
        self.db.close()
        return True
    # 定义一个插入数据库的函数
    def insertData(self, name, phone,allPhoneList):
        if allPhoneList != False:
            if str(phone) not in allPhoneList:
                if re.match(self.phone_pat,str(phone)) != None:
                    # time.time() 是时间戳 time.localtime 可以将时间戳转换成当地时间 time.strftime 是将localtime时间格式化
                    nowTime = time.strftime('%Y-%m-%d', time.localtime(time.time()))
                    # SQL插入语句 insert into 表名（数据） values（值）
                    sql = '''INSERT INTO phonedata (Date, Name, Phone) Values ("%s", "%s", "%s")''' % (nowTime, name, phone)
                    # 输出传入的值
                    # print(nowTime,name,phone)
                    try:
                        # 连接数据库
                        self.connect()
                        # 执行sql语句
                        self.cursor.execute(sql)
                        # 提交到数据库执行
                        self.db.commit()
                        # 关闭数据库
                        self.close()
                        return True ,"insertTure"
                    except:
                        self.db.rollback()
                    return False ,"inserFalse"
                return False ,"PhoneFalse"
            return False ,"Repeat"
        return False ,"SearchFalse"
    # 定义一个查询参数
    def search(self):
        sql = '''SELECT * FROM phonedata'''
        resultsList = []
        try:
            # 连接服务器
            self.connect()
            # 执行SQL语句
            self.cursor.execute(sql)
            # 获取数据库中的表单
            results = self.cursor.fetchall()
            # 将数据库中的表单分成一行行
            for row in results:
                # 遍历每一行中的下标为x的值
                resultsList.append(row[3])
            self.close()
        except:
            # 如果发生错误则回滚
            return False
            return False,"searchFalse"
        # 成功就返回插入的列表
        return resultsList
def readNameAndPhone(path,namecol,phonecol):
    # 打开excel表格
    worker = xlrd.open_workbook(u'%s' %(str(path)))
    # 获取所有的sheet
    ExcelTables = worker.sheet_names()
    # 使用下标为0的sheet
    sheetTable = worker.sheet_by_index(0)
    # 获取所有单元格中的手机号码
    nameList = []
    phoneList = []
    for i in range(sheetTable.nrows):
        # 获取Phone列的值
        phone = sheetTable.cell_value(i,phonecol)
        if re.match("[\\u4e00-\\u9fa5]+|[a-zA-z]+|\d{1,10}\s+|^\s+",str(phone)) != None:
            continue
        if phone != None and phone != "" and re.match(one.phone_pat,str(int(phone))) != None:
            #   同时获得该行的姓名
            name = sheetTable.cell_value(i,namecol)
            if name == "" :
                continue
            #   加入名字列表
            nameList.append(name)
            #   加入手机列表
            phoneList.append(phone)
    return nameList,phoneList
def repeatInsert(path,nameList,phoneList,allPhoneList):
    trueResult = 0
    falseResult = 0
    for i in range(len(nameList)):
        # 接受参数返回的结果以及提示
        # 执行数据库插入事件
        result, newfalseTip = one.insertData(str(nameList[i]), int(phoneList[i]), allPhoneList)
        if result == True:
            trueResult += 1
        else:
            falseResult += 1
    return trueResult,falseResult,newfalseTip
def search_NameCol_Or_PhoneCol(path):
    # 打开excel表格
    worker = xlrd.open_workbook(u'%s' %(str(path)))
    # 使用下标为0的sheet
    sheetTable = worker.sheet_by_index(0)
    # 获得sheet1中所有的列数：
    colsLen = sheetTable.ncols
    nameCol = 0
    phoneCol = 0
    for i in range(colsLen):
        nameS = sheetTable.col_values(i)
        for name in nameS:
            if str(name) == "本人姓名" or str(name) == "姓名" or str(name) == "名字" or str(name) == "本人名字":
                nameCol = i
    for j in range(colsLen):
        phoneS = sheetTable.col_values(j)
        for phone in phoneS:
            if str(phone) == "联系方式" or str(phone) == "电话号码" or str(phone) == "联系电话" or str(phone) == "电话":
                phoneCol = j
                break
    return nameCol,phoneCol
def readFile_returnPath(pathFile,pathList):
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
            # 如果是目录
            if os.path.isdir(path):
                # 再次遍历传入的文件夹
                readFile_returnPath(path,pathList)
        except BaseException as tip:
            print("BedFalse：",tip)
            continue
    return pathList
def mainFunction(pathFile):
    for path in pathList:
        #   判断文件是否为Excel文件
        if path.split(".")[-1] == "xls" or path.split(".")[-1] == "xlsx":
            #   执行一次数据库搜索
            allPhoneList = one.search()
            #   如果数据库搜索错误直接打断
            if allPhoneList == False:
                print("BigTip：错误的数据库连接以及搜索。")
                break
            print("Tip：----------开始检索[     %s     ]文件----------" %(str(path).split("\\")[-1]))
            #   获取该文件的名字列，和手机列。
            (nameCol,phoneCol) = search_NameCol_Or_PhoneCol(path)
            #   判断手机列或者号码列是否有错误。
            if nameCol >= phoneCol or phoneCol == 0 or phoneCol == None or nameCol == None:
                print("BigTip：Excel表格中未包含有姓名以及电话的列表。")
            else:
                #   获取名字列表，还有，手机列表。
                (nameList,phoneList) = readNameAndPhone(path,nameCol,phoneCol)
                #   判断获得的名字列表或者手机列表的长度是否大于0
                if len(nameList) > 0 and len(phoneList) > 0:
                    trueResult = 0
                    falseResult = 0
                    if phoneList == 0:
                        break
                    # 开始执行插入，以名字列表的长度为插入次数。
                    for i in range(len(nameList)):
                        result,falseTip = one.insertData(str(nameList[i]),int(phoneList[i]),allPhoneList)
                        if result == True:
                            trueResult += 1
                        else:
                            falseResult += 1
                    print("Tip：第一次结果提示 :",falseTip)
                    print("Tip：成功次数 :%s\nTip：错误次数 :%s" % (trueResult, falseResult))
                    # 在执行一次重复插入数据库的函数，如果错误次数大于5次的话。
                    for i in range(1):
                        if falseResult >= 5 and str(falseTip) != "Repeat":
                            print("Tip：----------再次检索[     %s     ]文件----------" % (str(path).split("\\")[-1]))
                            #   再次执行数据库查询
                            allPhoneList = one.search()
                            #   重复插入函数执行
                            (trueResult, falseResult,falseTip) = repeatInsert(path, nameList, phoneList, allPhoneList)
                    print("Tip：第二次错误提示 :",falseTip)
                else:
                    print("BigTip：Excle表格中含有姓名和电话的列表--->可惜没有数据。")
        else:
            print("BigTip：文件错误。")
            continue
def loginAdmin():
    adminAccount = input("BigTip：请登入管理员账号 :")
    if adminAccount == "lingyunyi":
        return True
    else:
        return False
if __name__ == "__main__":
    if loginAdmin() == True:
        try:
            serverIP = input("BigTip：请输入服务器IP地址 :")
            # 实例化插入数据库类
            one = IndexSql(serverIP)
            # 创建空列表
            pathList = []
            # 输入文件来源
            pathFile = str(input("BigTip：请输入路径 :"))
            # 获取文件列表
            pathList = readFile_returnPath(pathFile,pathList)
            # 检索文件链表并且插入数据库
            mainFunction(pathList)
        except BaseException as falseTop:
            print(falseTop)
        while True:
            anyKey = input("\nBigTip：异常--->请输入任意字符关闭:")
            if anyKey != None:
                break
    else:
        print("BigTip：错误--->程序将在5秒钟后关闭……")
        time.sleep(5)