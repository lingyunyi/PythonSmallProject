import pymysql
import datetime

class SqlManger(object):

    def __init__(self,setting):
        self.setting = setting
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
                    row[1] = str("http://{}".format(row[1]))
                    row[4] = str(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
                    # 遍历每一行中的下标为x的值
                    # 这里只是将数据添加入内存列表中，并没有刷新内存列表
                    self.setting.Golbals_SQL_Table_Data_List.append(row)
            self.close()
        except:
            # 如果发生错误则回滚
            self.close()
            return False

