# 导入自定义的mysql操作数据库
from mysqli import Mysqli

# 定义图书修改系统。
class Bookadmin(object):

    # 初始化函数
    def __init__(self):
        # 开启数据库
        self.mysqli = Mysqli()

    # 查询数据库中所有书籍的函数
    def selectAllbook(self):
        '''
        # 查询数据库中所有书籍的函数
        :return:
        '''
        # 尝试执行
        try:
            # 数据库连接
            self.mysqli.connect()
            # Sql语句
            sql = '''select * from bookdb'''
            # 执行sql语句并获取返回的数据
            results = self.mysqli.execute(sql)
            # 得到的results 是元祖类型
            if(results):
                # 从结果列表集合中
                for i in results:
                    # 输出结果
                    print(i)
                # 执行完代码快
                return True
            # 否则数据失败结果
            else:
                print("查询失败，请重试")
                # 执行完代码快
                return False
        except Exception as error:
            print("查询失败，请重试")
            print(error)
            # 执行完代码快
            return False
        # 最终一定要与数据库的连接
        finally:
            self.mysqli.close()
    # 通过书名查询一本书籍的函数
    def selectOneBookByName(self, bookName):
        '''
        # 通过书名查询一本书籍的函数
        :param bookName: 书名
        :return:
        '''
        try:
            # 现与数据库进行连接
            self.mysqli.connect()
            # sql语句
            sql = '''select * from bookdb where bookname = "%s"''' %(bookName)
            # 执行SQL语句
            results = self.mysqli.execute(sql)
            # 得到的results 是元祖类型
            if (results):
                # 从结果列表集合中
                for i in results:
                    # 输出结果
                    print(i)
                # 执行完代码快
                return True
                # 否则数据失败结果
            else:
                print("没有找到该书籍")
                # 执行完代码快
                return False
        except Exception as error:
            print("查询失败，请重试")
            print(error)
            # 执行完代码快
            return False
        finally:
            # 最终都关闭数据库
            self.mysqli.close()
    # 通过价格查询书籍
    def selectBooksByPrice(self, minPrice=0, maxPrice=99999):
        '''
        # 通过价格查询书籍
        :param minPrice: 最低价格间
        :param maxPrice: 最高价格区间
        :return:
        '''
        try:
            # 现与数据库进行连接
            self.mysqli.connect()
            # sql语句
            sql = '''select * from bookdb where price > "%s" AND price < "%s" order by price ASC''' %(minPrice,maxPrice)
            # 执行SQL语句
            results = self.mysqli.execute(sql)
            # 得到的results 是元祖类型
            if (results):
                # 从结果列表集合中
                for i in results:
                    # 输出结果
                    print(i)
                # 执行完代码快
                return True
                # 否则数据失败结果
            else:
                print("没有找到该书籍")
                # 执行完代码快
                return False
        except Exception as error:
            print("查询失败，请重试")
            print(error)
            # 执行完代码快
            return False
        finally:
            # 最终都关闭数据库
            self.mysqli.close()

    # 添加一本书
    def addOneBook(self, bookname, author, category, price, descs):
        '''
        # 添加一本书
        :param bookname: 书名
        :param author:  作者
        :param category:  类型
        :param price: 价格
        :param desc: 描述
        :param publish_data:
        :return:
        '''
        # 检验是否为空
        if(self.checkEmpty(bookname, author, category, price)):
            try:
                # 现与数据库进行连接
                self.mysqli.connect()
                # sql语句
                sql = '''insert into bookdb(bookname, author, category, price, descs) values("%s", "%s", "%s", "%s", "%s")''' % (bookname, author, category, price, descs)
                # 执行SQL语句
                results = self.mysqli.execute(sql)
                # 得到的results 是元祖类型
                if (results):
                    # 执行完代码快
                    print("添加成功......")
                    return True
                    # 否则数据失败结果
                else:
                    print("添加失败")
                    # 执行完代码快
                    return False
            except Exception as error:
                print("添加失败，请重试")
                print(error)
                # 执行完代码快
                return False
            finally:
                # 最终都关闭数据库
                self.mysqli.close()
        else:
            print("所传入的数据含有空")
            return False

    # 删除一本书
    def deleteOneBookByName(self, bookname):
        '''
        # 删除一本书
        :param bookName:  书名
        :return:
        '''
        try:
            # 现与数据库进行连接
            self.mysqli.connect()
            # 先查询书籍是否存在# sql语句
            sql = '''select * from bookdb where bookname = "%s"''' % (bookname)
            # 执行SQL语句
            if(self.mysqli.execute(sql)==False):
                print("该书籍不存在，修改失败")
                return False
            # sql语句
            sql = '''delete from bookdb where bookname = "%s"''' %(bookname)
            # 执行SQL语句
            results = self.mysqli.execute(sql)
            # 得到的results 是元祖类型
            if (results):
                print("删除成功......")
                # 执行完代码快
                return True
                # 否则数据失败结果
            else:
                print("没有找到该书籍")
                # 执行完代码快
                return False
        except Exception as error:
            print("删除失败，请重试")
            print(error)
            # 执行完代码快
            return False
        finally:
            # 最终都关闭数据库
            self.mysqli.close()

    # 修改一本书
    def modifyOneBookByName(self, bookname, author, category, price, descs):
        '''
        # 修改一本书
        :param bookname: 书名
        :param author:  作者
        :param category:  类型
        :param price: 价格
        :param desc: 描述
        :param publish_data:
        :return:
        '''
        if (self.checkEmpty(bookname, author, category, price)):
            try:
                # 现与数据库进行连接
                self.mysqli.connect()
                # sql语句
                sql = '''update bookdb set author = "%s", category = "%s", price = "%s", descs = "%s" where bookdb.bookname = "%s"''' %(author, category, price, descs, bookname)
                # 执行SQL语句
                results = self.mysqli.execute(sql)
                # 得到的results 是元祖类型
                if (results):
                    print("修改ok......")
                    # 执行完代码快
                    return True
                    # 否则数据失败结果
                else:
                    print("没有找到该书籍")
                    # 执行完代码快
                    return False
            except Exception as error:
                print("修改失败，请重试")
                print(error)
                # 执行完代码快
                return False
            finally:
                # 最终都关闭数据库
                self.mysqli.close()
        else:
            print("您输入的数据有空，请不要输入空数据")
            return False

    def checkEmpty(self,*args):
        '''
            检查传入参数是否为空
        :param args:
        :return:
        '''
        for i in args:
            if(i==""):
                return False
        return True
if __name__ == "__main__":
    admin = Bookadmin()
    # admin.selectAllbook()
    # admin.selectOneBookByName("1")
    # admin.selectBooksByPrice
    # admin.addOneBook("1","2","3","10.5","2")
    # admin.addOneBook("1", "2", "3", "", "2")
    admin.deleteOneBookByName("3")
    # admin.modifyOneBookByName("3","123","123","123", "")
