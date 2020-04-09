from selenium import webdriver
from selenium.webdriver import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from PIL import Image
import re
import urllib.request
import time
import random,requests
import move_move


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
        self.db = pymysql.connect("127.0.0.1", "root", "root", "test")
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










class Reques(object):

    def get_request_headers(self):
        # 用户代理User-Agent列表
        USER_AGENTS = [
            "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36",
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:69.0) Gecko/20100101 Firefox/69.0"
        ]

        headers = {
            "User-Agent": random.choice(USER_AGENTS),
        }
        return headers



    def __init__(self,url):
        self.url = url


    def requesX(self):
        '''

        :return:
        '''
        try:
            response = requests.get(self.url, headers=self.get_request_headers(), verify=False, allow_redirects=True, timeout=5)
            first_url_temp = str(response.content.decode("utf-8"))
            # 未验证
            print(response.status_code)
            if response.status_code == 403:
                return False
            elif response.status_code == 200:
                first_url_temp2 = re.findall('<div class="company-title font-18 font-f1">(.*?)</div>',first_url_temp)[0]
                print(first_url_temp2)
                first_url_temp3 = re.findall('<a href="(.*?)"',first_url_temp2)[0]
                print(first_url_temp3)
                first_url = "https://www.qixin.com{}".format(first_url_temp3)
                print(first_url)
                response2 = requests.get(first_url, headers=self.get_request_headers(), verify=False,allow_redirects=True, timeout=5)
                print(response2.status_code)
                if response2.status_code == 403:
                    return False
                elif response2.status_code == 200:
                    content = response2.content.decode("utf-8")
                    url_data = {
                        "class_name":str(self.url).split("=")[-1],
                        "icinfo": re.findall('<div class="tab-content" id="icinfo">(.*)</div>', content)[0],
                        "partners": re.findall('<div class="tab-content" id="partners">(.*)</div>', content)[0],
                        "employees": re.findall('<div class="tab-content" id="employees">(.*)</div>', content)[0],
                        "changeInfo": re.findall('<div class="tab-content" id="changeInfo">(.*)</div>', content)[0],
                        "financeData": re.findall('<div class="tab-content" id="financeData">(.*)</div>', content)[0],
                    }

                    sql = '''INSERT INTO icinfox (class_name,icinfo,partners,employees,changeInfo,financeData) VALUES ('%s','%s','%s','%s','%s','%s');'''%(url_data.get("class_name").replace("'",""),url_data.get("icinfo").replace("'",""),url_data.get("partners").replace("'",""),url_data.get("employees").replace("'",""),url_data.get("changeInfo").replace("'",""),url_data.get("financeData").replace("'",""))
                    manager = SqlManger()
                    print(sql)
                    true_or_false = manager.insert(sql)
                    print(true_or_false)
        except BaseException as e :
            print(e)
            return False





    def click_click(self):
        '''

        :return:
        '''
        print("-----------------------click_click-----------------------")
        try:
            browser = webdriver.Firefox()
            # 请求url
            browser.get(self.url)
            time.sleep(3)
            button = browser.find_element_by_xpath("/html/body/div[2]/div/div/div/div/button")
            button.click()
            browser.close()
            return True
        except BaseException as e:
            print(e)
            return False


    def move_move(self):
        '''
        :return:
        '''
        print("-----------------------move_move-----------------------")
        try:
            move_move.main()
            return True
        except BaseException as e:
            print(e)
            return False


    def begin(self):
        resault1 = self.requesX()
        if resault1 == False:
            resault2 = self.click_click()
            if resault2 == False:
                resault3 = self.move_move()
                if resault3 == True:
                    self.requesX()
                else:
                    time.sleep(10)
            else:
                self.requesX()




if __name__ == "__main__":



    rex = Reques(url="https://www.qixin.com/search?key=360")
    rex.requesX()
    # print(rex.requesX())