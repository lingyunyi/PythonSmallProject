import time
import pymysql
import datetime
import hashlib

class SqlManger(object):

    def __init__(self,sql_ip="",sql_user="",sql_passwd="",sql_DB="passworddata"):
        '''
            暂无初始化内容
        '''
        self.sql_ip = str(sql_ip)
        self.sql_user = str(sql_user)
        self.sql_passwd = str(sql_passwd)
        self.sql_DB = str(sql_DB)
        self.connect_result = self.connect()

    def connect(self):
        '''
            # connent(参数列表[“IP地址”，“数据库账号”， “数据库密码”， “数据库名称”])
        :return:
        '''
        try:
            self.db = pymysql.connect(self.sql_ip, self.sql_user, self.sql_passwd ,self.sql_DB )
            # 使用cursor游标，创建一个游标对象cursor
            self.cursor = self.db.cursor()
            return True
        except BaseException as e:
            return False

    def close(self):
        '''
        # connent(参数列表[“IP地址”，“数据库账号”， “数据库密码”， “数据库名称”])
        :return:
        '''
        self.cursor.close()
        # 数据库关闭
        self.db.close()
        return True

    def search(self,sql):
        try:
            # 执行SQL语句
            self.cursor.execute(sql)
            # 获取数据库中的表单
            results = self.cursor.fetchall()
            # 直接返回查询结果，返回的结果是一个元祖
            return results
        except:
            return False

    def insert(self, sql):
        try:
            # 执行sql语句
            self.cursor.execute(sql)
            # 提交到数据库执行
            self.db.commit()
            return True
        except:
            self.db.rollback()
            return False

    def is_can(self):
        '''
            当别调用时，查看是否可以用
        '''
        print("this （{}）moddle is ok!!!".format(self.__class__))
        return True

class passwordHandle(object):
    def passwordIn(self,password,setNumber):
        finalStr = ""
        # 将输入的字符重做为字符串
        password = str(password)
        # 循环字符串中的每一个字符
        for tupleStr in password:
            # 循环用户输入的六位以上数字密码
            for num in str(setNumber):
                # 是偶尔数
                if (eval(num) % 2) == 0:
                    # 将每一个字符转换成相应的数字
                    tupleStr_Number = ord(tupleStr)
                    tupleStr_Number = tupleStr_Number - eval(num)
                    # 恢复成字符串并相加
                    finalStr += chr(tupleStr_Number)
                else:
                    # 将每一个字符转换成相应的数字
                    tupleStr_Number = ord(tupleStr)
                    tupleStr_Number = tupleStr_Number + eval(num)
                    # 恢复成字符串并相加
                    finalStr += chr(tupleStr_Number)
        finalStr = ' '.join(format(ord(one_str), 'b') for one_str in finalStr)
        # 道生一，一生二，二生三
        finalStr = str(finalStr).replace("1","2").replace('0','1').replace('2','0')
        return finalStr
    def passwordOut(self,binPassword,setNumber):
        password = ""
        finalStr = ""
        binPassword = str(binPassword).replace("1", "2").replace('0', '1').replace('2', '0')
        # 将二进制解码
        binList = binPassword.split(" ")
        for binNum in binList:
            strNum = int(binNum,2)
            password += chr(strNum)
        startNum = 0
        for tupleStr in password:
            if startNum % len(str(setNumber)) == 0:
                if int(str(setNumber)[0]) % 2 == 0:
                    oneStartNum = ord(tupleStr) + int(str(setNumber)[0])
                    finalStr += chr(oneStartNum)
                else:
                    oneStartNum = ord(tupleStr) - int(str(setNumber)[0])
                    finalStr += chr(oneStartNum)
            startNum += 1
        return finalStr

class mainProcess(object):



    def __init__(self,in_sql_ip,in_sql_user,in_sql_passwd,in_sql_DB):
        self.sqlmanager = SqlManger(in_sql_ip,in_sql_user,in_sql_passwd,in_sql_DB)
        self.passwordHandle = passwordHandle()
        self.islogin = False
        self.setNumber = None
        self.loginUser = None

    def is_number(self,str):
        try:
            float(str)
            return True
        except ValueError:
            pass
        return False

    def createAccount(self):
        account = input("请输入需要注册的账号：")
        # 来一条查询账号的sql
        sql = '''select user from users'''
        usersList = self.sqlmanager.search(sql)
        for userx in usersList:
            if account == userx[0]:
                exit("已存在相同账号.....")
        passwdx = input("请输入密码：")
        admin = input("邀请码：")
        if admin != "lingyunyi":
            print("不是邀请用户.....")
        else:
            # 如果走到这里，就可以注册了。
            # 注册语句
            passwd = hashlib.md5(passwdx.encode(encoding='UTF-8')).hexdigest()
            sql = '''INSERT INTO users (user, passwd) VALUES ('%s', '%s')''' %(account,passwd)
            self.sqlmanager.insert(sql)
            print("%s注册成功,密码为%s" %(account,passwdx))

    def loginAccount(self):
        if self.islogin == True:
            print("请你这个大笨蛋，不要多次重新登入，注销后再次登入......")
        else:
            account = input("请输入账号：")
            passwd = input("请输入密码：")
            passwd = hashlib.md5(passwd.encode(encoding='UTF-8')).hexdigest()
            sql = '''select * from users where user = '%s' and passwd = '%s' '''%(account,passwd)
            ishas = self.sqlmanager.search(sql)
            if ishas:
                print("欢迎登入成功.....")
                self.islogin = True
                print('提示：个人数字令牌十分重要，一旦不对，查询或者输入的密码，将不能被正常解密')
                setNumber = input("请输入加密数字（六位数以上）：")
                setNumber2 = input("请再次输入加密数字（六位数以上）：")
                self.loginUser = account
                if setNumber2 != setNumber:
                    print("两次密码有误，请重新，使用重置个人数字令牌，重新设置个人数字令牌。")
                elif setNumber2 == setNumber and self.is_number(setNumber2):
                    self.setNumber = setNumber2
                    print("个人数字加密令牌已设置：%s"% (self.setNumber))
                else:
                    print("不支持数字以外令牌，请重新，使用重置个人数字令牌，重新设置个人数字令牌。")
            else:
                print("账号或密码有误.....")

    def changeSetNumber(self):
        if self.islogin == False:
            print("未登入...或未设置加密数字...")
        else:
            print('提示：个人数字令牌十分重要，一旦不对，查询或者输入的密码，将不能被正常解密')
            setNumber = input("请输入加密数字（六位数以上）：")
            setNumber2 = input("请再次输入加密数字（六位数以上）：")
            if setNumber2 != setNumber:
                print("两次密码有误，请重新，使用重置个人数字令牌，重新设置个人数字令牌。")
            elif setNumber2 == setNumber and self.is_number(setNumber2):
                self.setNumber = setNumber2
                print("个人数字加密令牌已设置：%s" % (self.setNumber))
            else:
                print("不支持数字以外令牌，请重新，使用重置个人数字令牌，重新设置个人数字令牌。")

    def addMyPasswd(self):
        if self.islogin == False or self.setNumber == None:
            print("未登入...或未设置加密数字...")
        else:
            print('接下来开始进入添加个人密码流程')
            iswhere = input("为该账号所在的地方添加描述（尽量多填写，方便后续插叙）：")
            account = input("请输入账号：")
            passwd = input("请输入密码：")
            passwd2 = input("请再次输入密码：")
            if iswhere == "" or account == "" or passwd == "" or passwd != passwd2:
                print("小老弟，能不能不搞笑，不能输入空字符串。什么都不填，你想搞坏我数据库啊。")
                print("第一次，和，第二次输入的密码不对也不行，好好检查。")
            else:
                passwd = self.passwordHandle.passwordIn(passwd,self.setNumber)
                daytime = datetime.datetime.strftime(datetime.datetime.now(), '%Y-%m-%d %H:%M:%S')
                iswho = self.loginUser
                sql = '''INSERT INTO passwd (iswhere, account, passwd, daytime, iswho) VALUES ('%s', '%s', '%s', '%s', '%s')'''\
                      % (iswhere, account, passwd, daytime, iswho)
                self.sqlmanager.insert(sql)
                print("--------------------------------------------")
                print("登入地描述：%s" % iswhere)
                print("登入地账号：%s" % account)
                print("登入地密码：%s" % passwd2)
                print("--------------------------------------------")
                print("信息存储成功......")


    def searchMyPasswd(self):
        if self.islogin == False or self.setNumber == None:
            print("未登入...或未设置加密数字...")
        else:
            print('请输入需要查询账号的关键字,（不输入为全部查询）')
            iswhere = input("请输入需要查询账号的关键字（描述）省略输入比如，哔哩哔哩：")
            sql = '''select * from passwd where iswho = '%s' ''' % self.loginUser
            resault = self.sqlmanager.search(sql)
            showData = None
            if resault == ():
                print("老弟，先存一点密码吧，都没有密码你查个屁屁。")
            else:
                if iswhere != "":
                    for row in resault:
                        row = list(row)
                        if iswhere in row[1]:
                            row[3] = self.passwordHandle.passwordOut(row[3],self.setNumber)
                            showData = row
                            print("--------------------------------------------")
                            print("登入地描述：%s" %showData[1])
                            print("登入地账号：%s" %showData[2])
                            print("登入地密码：%s" %showData[3])
                            print("初次存储时：%s" %showData[4])
                            print("--------------------------------------------")
                            print("已经查询到结果.....，提示：若密码为乱码，则为数字令牌输入错误，请重置个人数字令牌。")
                    if showData == None:
                        print("并未查询到，相关结果，请重新查询后输入正常的，登入地简单描述。")
                else:
                    print("暂时不支持，全密码查询......")
                    # for show in resault:
                    #     show = list(show)
                    #     show[3] = self.passwordHandle.passwordOut(show[3],self.setNumber)
                    #     print(show)


class show(object):

    def __init__(self):
        # 展示系统版本
        self.printVersion()
        # 开始让用户选择数据库
        self.printSelectDB()

    def printVersion(self):

        '''
            版本界面
        :return:
        '''
        print("\n")
        print("*************************************************")
        print("****                                         ****")
        print("****           欢迎使用密码查询系统           ****")
        print("****                                         ****")
        print("****              版本：V3.5                 ****")
        print("****              作者：水兔工作室            ****")
        print("****                                         ****")
        print("*************************************************")
        time.sleep(1)
        print("\n")


    def printSelectDB(self):

        '''
            版本界面
        :return:
        '''
        print("*************************************************")
        print("****                                         ****")
        print("****             请选择使用的数据库            ****")
        print("****                                         ****")
        print("****              1.默认选择数据库            ****")
        print("****              2.手动选择数据库            ****")
        print("****                                         ****")
        print("*************************************************")
        time.sleep(1)
        changeNumber = input("您的操作是？：")
        # 1.默认选择数据库
        if changeNumber == "1":
            sql_ip = "139.159.236.66"
            sql_user = "lingyunyi"
            sql_passwd = "lingyunyi00"
            sql_DB = "passworddata"
            self.mainProcess = mainProcess(sql_ip,sql_user,sql_passwd,sql_DB)
        # 2.手动选择数据库
        elif changeNumber == "2":
            sql_ip = input("请输入数据库地址：")
            sql_user = input("请输入数据库账号：")
            sql_passwd = input("请输入数据库密码：")
            sql_DB = input("请输入数据库名称(默认为：passworddata)：")
            print("请耐心等待，正在尝试连接......")
            self.mainProcess = mainProcess(sql_ip,sql_user,sql_passwd,sql_DB)
        else:
            self.printSelectDB()
        while self.mainProcess.sqlmanager.connect_result != True:
            print("数据库异常，暂时无法连接，请检测网络配置......")
            self.printSelectDB()
        if self.mainProcess.sqlmanager.connect_result == True:
            print("恭喜您，成功进入数据库：%s"%(sql_ip))
            while True:
                self.showintoFunction()

    def showintoFunction(self):
        print("*************************************************")
        print("****                                         ****")
        print("*******           %s          ********" %self.mainProcess.loginUser)
        print("****              1、注册账号                 ****")
        print("****              2、登入账号                 ****")
        print("****              3、重置个人数字令牌          ****")
        print("****              4、添加个人密码             ****")
        print("****              5、查询个人密码             ****")
        print("****              6、注销当前用户             ****")
        print("****              q、按q退出                  ****")
        print("****                                         ****")
        print("*************************************************")
        time.sleep(1)
        changeNumber = input("您的操作是？：")
        if changeNumber == "1":
            self.mainProcess.createAccount()
        elif changeNumber == "2":
            self.mainProcess.loginAccount()
        elif changeNumber == "3":
            self.mainProcess.changeSetNumber()
        elif changeNumber == "4":
            self.mainProcess.addMyPasswd()
        elif changeNumber == "5":
            self.mainProcess.searchMyPasswd()
        elif changeNumber == "6":
            if self.mainProcess.islogin == True:
                print("注销当前登入用户：%s" %(self.mainProcess.loginUser))
                self.mainProcess.islogin = False
                self.mainProcess.loginUser = None
                print("注销成功，欢迎使用......")
            else:
                print("没有登入你注销个鬼啊！")
        elif changeNumber == "q":
            exit("欢迎使用....")
        else:
            print("小老弟你搞什么，不要乱按。")
if __name__ == "__main__":
    a = show()