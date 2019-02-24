# 导入自定义的mysql操作数据库
from mysqli import Mysqli
import random
# 添加加密函数
import hashlib

class Accoutadmin(object):
    def __init__(self):
        # 初始化函数
        # 连接数据库
        self.mysqli = Mysqli()
        # 登入次数
        self.login_num = 3
        # 是否登入
        self.is_login = False
        if(self.mysqli.connect()):
            print("数据库尝试连接...")
            print("数据库连接成功...")
        else:
            print("数据库连接失败...")
            # 数据库连接失败直接退出
            exit()
    def randomCode(self):
        '''
            验证码生成
        :return:
        '''
        list = ""
        # range(x)生成x个随机数的验证码
        for i in range(4):
            # 跟随循环生成一个0-4之间的随机数来决定生成的是大小写字母还是数字
            j = random.randrange(0, 4)
            # 随机产生的数字是1时，生成数字
            if j == 1:
                a = random.randrange(0, 10)
                list = list + str(a)
            # 随机产生的数字是2时，生成大写字母
            elif j == 2:
                a = chr(random.randrange(65, 91))
                list = list + a
            # 随机产生的数字是除了1和2时，生成小写字母
            else:
                a = chr(random.randrange(97, 127))
                list = list + a
        return str(list)
    def checkCode(self):
        '''
            验证码输入
        :return:
        '''
        input_num = 3
        checkCode = self.randomCode()
        print(checkCode)
        while str(input("请输入验证码：")) != checkCode:
            checkCode = self.randomCode()
            input_num -= 1
            if(input_num != 0):
                print(checkCode)
            else:
                return False
    def checkDuplicata(self, Duplicate_key, value):
        '''
            查询某字段中是否存在某值
        :param Duplicate_key:
        :param value:
        :return:
        '''
        # 数据库连接
        self.mysqli.connect()
        # duplicata v.复制 重复 n.副本
        # SQL语句
        sql = '''select * from userdb where %s="%s"''' %(Duplicate_key,value)
        # 数据库执行
        if(self.mysqli.execute(sql)):
            # 如果执行成功，并且返回的数据不等于空。
            return True
        else:
            return False
    def regist(self):
        '''
            账号注册
        :param username:
        :param password:
        :return:
        '''
        username = input("请输入账号：")
        frist_password = input("请输入密码：")
        second_password = input("请再次输入密码：")
        ''''''
        if (frist_password == "" or second_password == "" or username == ""):
            print("帐号密码不能为空")
            # 强制结束
            exit()
        input_num = 3
        # 判断输入的验证码是否相等
        if (self.checkCode() != False):
            # 判断两次密码是否相等，并且只有三次机会
            while frist_password != second_password:
                print("两次密码不匹配，请重新输入：")
                frist_password = input("请输入密码：")
                second_password = input("请再次输入密码：")
                input_num -= 1
                if(input_num == 1):
                    print("输入次数过多请重试")
                    return False
        # 查重
        if(self.checkDuplicata("username", username)):
            print("请不要重复注册：%s" %(username))
            return False
        # SQL语句
        hx = hashlib.md5()
        hx.update(second_password.encode(encoding='utf-8'))
        sql = '''insert into userdb(username, password) values("%s", "%s")''' %(username, hx.hexdigest())
        # 数据库执行
        if(self.mysqli.execute(sql)):
            print("注册成功，账号：%s，密码：%s" %(username, second_password))
        else:
            print("注册失败，请重试")
        # 数据库关闭
        self.mysqli.close()
        return True
    def login(self):
        '''
            登入功能
        :param username:
        :param password:
        :return:
        '''
        username = input("请输入账号：")
        password = input("请输入密码：")
        ''''''
        if (self.checkDuplicata("username", username)==False):
            print("该账号不存在")
            return False,False
            # 判断帐号密码是否为空
        if (password == ""  or username == ""):
            print("帐号密码不能为空")
            # 强制结束
            exit()
        # 查询语句
        hx = hashlib.md5()
        hx.update(password.encode(encoding='utf-8'))
        sql = '''select * from userdb where username="%s" and password = "%s"''' %(username,hx.hexdigest())
        results = self.mysqli.execute(sql)
        if(results):
            print("登入成功")
            self.is_login = True
            return True,username
        else:
            print("账号/密码错误")
            self.login_num -= 1
            if(self.login_num > 0):
                self.login()
            return False,False
    def changepassword(self):
        '''
            修改密码
        :return:
        '''
        print("*****请先登入*****")
        # 启动先登入功能
        (res,username) = self.login()
        if(res==True):
            ''''''
            frist_password = input("请输入新密码：")
            second_password = input("请再次输入新密码：")
            input_num = 3
            # 判断帐号密码是否为空
            if (frist_password == "" or second_password == ""):
                print("密码不能为空")
                # 强制结束
                exit()
            # 查看是否第一次密码与第二次密码相等
            while frist_password != second_password:
                print("两次密码不匹配，请重新输入：")
                frist_password = input("请输入新密码：")
                second_password = input("请再次输入新密码：")
                input_num -= 1
                if(input_num == 1):
                    print("输入次数过多请重试")
                    return False
            # 连接数据库，修改密码.
            ''''''
            try:
                self.mysqli.connect()
                # 更新Sql数据库语句
                hx = hashlib.md5()
                hx.update(second_password.encode(encoding='utf-8'))
                sql = '''update userdb set password = "%s" where userdb.username = "%s"''' %(hx.hexdigest(), username)
                # 数据库执行
                if(self.mysqli.execute(sql)):
                    # 数据库关闭
                    self.mysqli.close()
                    # 打印成功提示
                    print("密码修改成，新密码是 %s" %(second_password))
                    return True
                # 如果sql语句执行失败
                else:
                    print("系统异常，请重试")
                    return False
            # 如果try语句出现异常
            except BaseException as error:
                print(error)
                return False
        # 如果登入失败
        else:
            print("请重试")
            return False
if __name__ == "__main__":
    admin = Accoutadmin()
    admin.login()
