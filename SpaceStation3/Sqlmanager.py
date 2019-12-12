import pymysql
import datetime

class SqlManger(object):

    def __init__(self,golbalData):
        self.golbalData = golbalData
        self.search_table_all_data()
        self.search_all_users()
    def connect(self):
        '''
            # connent(参数列表[“IP地址”，“数据库账号”， “数据库密码”， “数据库名称”])
        :return:
        '''
        self.db = pymysql.connect("47.107.57.166", "lingyunyi", "Lingyunyi00..", "UrlData")
        # 使用cursor游标，创建一个游标对象cursor
        self.cursor = self.db.cursor()
        return True

    def close(self):
        '''
        # connent(参数列表[“IP地址”，“数据库账号”， “数据库密码”， “数据库名称”])
        :return:
        '''
        self.cursor.close()
        # 数据库关闭
        self.db.close()
        return True

    def search_table_all_data(self):
        sql = ''' SELECT * FROM webdata '''
        try:
            # 连接服务器
            self.connect()
            # 执行SQL语句
            self.cursor.execute(sql)
            # 获取数据库中的表单
            results = self.cursor.fetchall()
            # 将数据库中的表单分成一行行
            for row in results:
                if row[-1] != 1:
                    row = list(row)
                    row[4] = str(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
                    # 遍历每一行中的下标为x的值
                    # 这里只是将数据添加入内存列表中，并没有刷新内存列表
                    self.golbalData["SqlManger"].append(row)
            self.golbalData["SqlManger"].sort()
            self.close()
        except:
            # 如果发生错误则回滚
            self.close()
            return False

    def search_all_users(self):
        sql = ''' SELECT * FROM users '''
        try:
            # 连接服务器
            self.connect()
            # 执行SQL语句
            self.cursor.execute(sql)
            # 获取数据库中的表单
            results = self.cursor.fetchall()
            # 将数据库中的表单分成一行行
            for row in results:
                self.golbalData["Users"].append(row)
            self.golbalData["Users"].sort()
            self.close()
        except:
            # 如果发生错误则回滚
            self.close()
            return False

    def insert_into_webdata(self,finallyData):
        sql = '''INSERT INTO webdata (URL, ClassA, ClassB,CreateTime,WhoeCreate,isDelete) Values ("%s", "%s", "%s", "%s", "%s", "%s")'''\
              % (finallyData[0], finallyData[1], str(finallyData[2]).replace("[","").replace("]","").replace("'",""), finallyData[3], finallyData[4], finallyData[5])
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
            return True, "insertTure"
        except:
            self.db.rollback()


