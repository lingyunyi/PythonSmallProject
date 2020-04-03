import pymysql


class SqlManger(object):

    def __init__(self):
        '''
            暂无初始化内容
        '''
        pass

    def connect(self):
        '''
            # connent(参数列表[“IP地址”，“数据库账号”， “数据库密码”， “数据库名称”])
        :return:
        '''
        self.db = pymysql.connect("47.107.57.166", "lingyunyi", "Lingyunyi00..", "loves")
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

    def search(self,sql):
        try:
            # 连接服务器
            self.connect()
            # 执行SQL语句
            self.cursor.execute(sql)
            # 获取数据库中的表单
            results = self.cursor.fetchall()
            self.close()
            # 直接返回查询结果，返回的结果是一个元祖
            return results
        except:
            # 如果发生错误则回滚
            self.close()
            return False

    def insert(self, sql):
        try:
            # 连接数据库
            self.connect()
            # 执行sql语句
            self.cursor.execute(sql)
            # 提交到数据库执行
            self.db.commit()
            # 关闭数据库
            self.close()
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