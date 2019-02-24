# 导入pymysql包
import pymysql

class Mysqli(object):

    def __init__(self, ip="localhost", user="root", passwd="root", database='libararysystem'):
        '''
        # 初始化
        :param ip: 数据库IP地址
        :param user: 数据库登入账号
        :param passwd:数据库登入密码
        :param database: 所被使用的数据库
        '''
        self.ip = ip
        self.user = user
        self.passwd = passwd
        self.database = database
    def connect(self):
        # 连接
        try:
            self.db = pymysql.connect(self.ip, self.user, self.passwd, self.database)
            # 创建游标cursor
            self.cursor = self.db.cursor()
            return True
        except BaseException as error:
            # baseException 是所有错误的基类
            return False

    def execute(self,query):
        # query n.询问 vi.查询
        # 执行
        sql = query
        try:
            # 使用游标对象执行sql语句
            self.cursor.execute(sql)
            if "SELECT" in sql or "select" in sql:
                # in 属于A in B A是B的子集，A被B包含
                results = self.cursor.fetchall()
                if(results!=()):
                    return results
                else:
                    return False
            # 提交到数据库执行
            self.db.commit()
            return True
        except BaseException as error:
            # 回滚
            self.db.rollback()
            print(error)
            return False
    def close(self):
        # 关闭
        # 关闭cursor游标对象
        try:
            self.cursor.close()
            # 关闭数据库连接
            self.db.close()
            return True
        except BaseException as error:
            print(error)
            return False
if __name__ == "__main__":
    mysqli = Mysqli()
    print(mysqli.connect())
    # sql = '''select * from userdb where userdb.username = "%s"''' %("admin")
    sql = '''insert into userdb(username, password) values("%s", "%s")''' %("lingyunyi","123")
    print(sql)
    print((mysqli.execute(sql)))
