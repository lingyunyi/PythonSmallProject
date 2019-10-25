import requests
import re
from bs4 import BeautifulSoup
import pymysql



class TouristCrawler(object):

    def __init__(self):
        self.SqlManger = SqlManger()
        self.MaFengWoListNum = 0

    def XieCheng(self, weburl):
        '''
            对基本的网站的内容进行获取和控制
        :param weburl:
        :return:
        '''
        print("Begin Start:%s" %(weburl))
        try:
            header = {
                "referer":"https://vacations.ctrip.com/list/grouptravel/d-guangxi-100052.html",
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36"
            }
            r = requests.get(weburl, headers=header, verify=False, allow_redirects=True, timeout=5)
            # 这时候我们就开始获取所有的当前页面的列表数据
            informationDataDict = re.findall('window.__INITIAL_STATE__ = {"html":(.*)}',r.content.decode("utf-8"))[0]
            # 这就变成Json数据咯
            # 存入文本，用本地进行信息提取，减少请求次数
            informationDataDict = informationDataDict.replace("\\",'')
            # 解析成所有的字典
            informationALLDict = re.findall('({.*?}),',informationDataDict)
            # 获取主要的数据,这次主要的是获取三种数据，第一种，名字，第二，图片，第三跳转连接。
            allImg = re.findall('"image":"(.*?)"',informationDataDict)
            allFontContent = re.findall('"key":"subName","value":"(.*?)"',informationDataDict)
            allFontDetailUrl  = re.findall('"detailUrl":"(.*?)"',informationDataDict)

            # 将数据持久化保存到文件中
            BigBigBigList = []
            with open("BigBigBigList.txt",mode="a+") as f:
                for i in range(len(allImg)):
                    f.write(str([allFontContent[i],str(allImg[i]).replace("_C_200_150",""),allFontDetailUrl[i]]))
                    f.write("\n")
                f.close()

        except BaseException as error:
            print("Error:",error)


    def QiongYou(self,searchCity):
        '''
            对穷游网站的旅游途径进行基本的解析和获取
        :param searchCity:
        :return:
        '''
        print("Begin Start:http://plan.qyer.com/api/v3/recommend/getpoilist")
        try:
            weburl = "http://plan.qyer.com/api/v3/recommend/getpoilist"
            header = {
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36",
                "Cookie":"_guid=Rb1f04c0-130e-8446-439d-55432d2122f8; new_uv=1; new_session=1; _qyeruid=CgIBAV2am8pfCx3zaFxbAg==; __guid=145335541.2242739499673084200.1570413515112.3357; PHPSESSID=2d9df7689269a548a1d0790fadf68d85; __utmc=253397513; __utmz=253397513.1570413517.1.1.utmcsr=(direct)|utmccn=(direct)|utmcmd=(none); ql_guid=QL4c1493-2116-41f8-b706-a00b7678729e; isnew=1570413524256; __utma=253397513.1340703000.1570413517.1570413517.1570422933.2; ql_created_session=1; ql_stt=1570422933465; ql_vts=2; plan_token=209557f74f8f1a9f1d064938abaf2bac; plan_code=V2YJYlFgBz9TZ1I4CmsNOg; ql_seq=5; __utmb=253397513.10.9.1570423148645; monitor_count=12"
            }
            allList = []
            for i in range(1,50):
                data = {
                    "plan_id":"21693774",
                    "oneday_id":"176639639",
                    "city_id":"11595",
                    "keyword":"",
                    "range":"1",
                    "page":"%s"%(i),
                    "type":"0"
                }
                r = requests.post(weburl, headers=header, verify=False, allow_redirects=True, timeout=5,data=data)
                listData = r.content.decode("utf-8")
                image = re.findall('"image":"(.*?)"',listData)
                citySign = re.findall('"cn_name":"(.*?)"',listData)
                comment = re.findall('"comment":"(.*?)"',listData)
                for i in range(len(image)):
                    citySignA = str(citySign[i]).replace(r"\\","\\").encode("utf-8").decode('unicode_escape')
                    imageA = str(image[i]).replace("\\","")[0:-1]
                    commentA = str(comment[i]).replace(r"\\","\\").encode("utf-8").decode('unicode_escape')
                    print(i,citySignA,imageA,commentA)
        except BaseException as error:
            print("Error:", error)


    def MaFengWo(self,cityMddid):
        '''
            接收来源于mafengwo3函数传来的mddid城市地址代数进行二次解析获取真实地址传给函数2进行再次过滤获取地址
        :param cityMddid:
        :return:
        '''
        try:
            weburl = "http://www.mafengwo.cn/mdd/base/routeline/pagedata_routelist"
            header = {
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36",
            }
            mdd_src_list = []
            for i in range(1, 10):
                data = {
                    "mddid":cityMddid,
                    "page":"%s"%(i),
                    "type":"2",
                    "_ts":"1570885642489",
                    "_sn":"b3f692eb14",

                }
                r = requests.post(weburl, headers=header, verify=False, allow_redirects=True, timeout=5, data=data)
                ALLHTML = r.text.replace('\\',"")
                ALLHTML2 = ALLHTML.encode("utf-8").decode('unicode_escape')
                DIV_A = re.findall('<a href="(.*?)" target="_blank">',ALLHTML2)
                for i in DIV_A:
                    if "/mdd/route" in i:
                        i = 'http://www.mafengwo.cn' + i
                        mdd_src_list.append(i)

            mdd_src_set = set(mdd_src_list)
            print(mdd_src_set)
            self.MaFengWoListNum += len(mdd_src_set)
            self.MafengWo2(mdd_src_set)
        except BaseException as error:
            print("Error:", error)

    def MafengWo2(self,urlSet):
        '''
            接受来源于，经过mafengwo函数解析过后传来的所有路线的网页地址，进行具体内容的破解和获取
        :param urlSet:
        :return:
        '''
        for i in urlSet:
            try:
                # 循环传入过来的所有连接
                print("BeginStatr:%s" %(i))
                # i = "http://www.mafengwo.cn/mdd/route/12810_101612.html"
                header = {
                    "referer":"%s" %(i),
                    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36"
                }
                r = requests.get(i, headers=header, verify=False, allow_redirects=True, timeout=5)
                # 替换掉被魔改的内容
                ALLHTML = r.content.decode("utf-8").replace('\\',"")
                # 获取该路径的标题
                title = re.findall("<h1>(.*?)</h1>",ALLHTML)[0]
                # 获取该路径，所需要的天数
                titleDay = re.findall("\d",title)[0] + "天"
                # 获取网页中的旅行权重
                quanzhong = re.findall('<p><em>(.*?)</em>',ALLHTML)[0]
                # 将获得的html文档进行一次文档整合
                ALLHTML = str(ALLHTML).encode("utf-8").decode("utf-8")
                # 使用BS4开始处理一些困难的html元素
                soup = BeautifulSoup(ALLHTML, 'html.parser')
                # 找到，旅游路径的简单基本时间路线的TAG标签
                dayWayAll = soup.select(".J_overview .day")
                if dayWayAll == []:
                    # 特殊情况，如果该页面没有含有day Class类。
                    dayWayAll = soup.select(".J_overview a")
                dayWayContent = []
                # 遍历该便签，将所有获得的内容存入列表中
                # 新添加一个路程路线字符串 String_DayWay
                for i in enumerate(dayWayAll):
                    dayWay_Time = "第" + str(i[0] + 1) + "天"
                    #     寻找所有的A元素
                    dayWay_Way = re.findall(">(.*?)</a>",str(i[1]))
                    dayWay_Way.insert(0,str(dayWay_Time))
                    dayWayContent.append(dayWay_Way)
                # 查找下一个具体内容的旅游路程列表
                wayAllContent = soup.select(".day-item")
                for i in enumerate(wayAllContent):
                    if i[0] < 4 :
                        # 将路径的评论内容添加到一个内容表格中
                        dayWay_Way_Content = re.findall('<div class="poi-txt">(.*?)</div>', str(i[1]))
                        dayWay_Way_Img = re.findall('<img class="lazy" data-original="(.*?)"', str(i[1]))
                        try:
                            if dayWayContent[i[0]] != False:
                                dayWayContent[i[0]].append([str(dayWay_Way_Content),dayWay_Way_Img])
                        except BaseException as e:
                            print("for i in enumerate(wayAllContent):", e)
                            continue
                # 再把之前的两个内容，添加到内容列表中
                dayWayContent.insert(0,quanzhong)
                dayWayContent.insert(0,titleDay)
                dayWayContent.insert(0,title)
                # 循环数据处理掉不必要的数据
                for i in dayWayContent:
                    if isinstance(i,list) == True and len(i) == 2:
                        dayWayContent.pop()
                self.SqlManger.begin_insert_data(dayWayContent)
            except BaseException as error:
                print("2Error:", error)
                continue
        print("实际数量总数量:%s" %self.MaFengWoListNum)

    def MAfengWo3_GetAllCityMddid(self):
        '''
            遍历该网站，强获取，所有网页的地址城市的mddid
        :return:
        '''
        try:
            weburl = "http://www.mafengwo.cn/mdd/"
            header = {
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36",
            }
            r = requests.post(weburl, headers=header, verify=False, allow_redirects=True, timeout=5,)
            ALLHTML = r.text.replace('\\',"")
            ALLHTML2 = ALLHTML.encode("utf-8").decode('unicode_escape')
            allCityMddidList = set(re.findall("/travel-scenic-spot/mafengwo/(.*?)\.html",ALLHTML2))
            for i in allCityMddidList:
                if i != "":
                    self.MaFengWo(i)
        except BaseException as error:
            print("Error:", error)


class SqlManger(object):

    def connect(self):
        '''
            # connent(参数列表[“IP地址”，“数据库账号”， “数据库密码”， “数据库名称”])
        :return:
        '''
        self.db = pymysql.connect("120.27.144.96", "root", "Aa123456", "luxing")
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

    def begin_insert_data(self,data):
        dayWayContent = data

        biaoti = dayWayContent[0]
        typex = dayWayContent[3][1]
        quanzhong = dayWayContent[2]
        dayx = dayWayContent[1]
        string_luxian = "出发地"
        for i in dayWayContent:
            if isinstance(i, list) == True:
                string_luxian += "->"
                string_luxian += i[1]
        Amap = ""
        img = ""
        cs1 = dayWayContent[3][1]

        try:
            ywgl1 = dayWayContent[3][2][0]
        except BaseException as e:
            print("赋值有误，ywgl1")
            ywgl1 = ["",""]
        luxian = string_luxian
        try:
            img1 = dayWayContent[3][2][1]
        except BaseException as e:
            print("赋值有误，img1")
            img1 = ["",""]
        try:
            zsgl1 = dayWayContent[3][2][0]
        except BaseException as e:
            print("赋值有误，zsgl1")
            zsgl1 = ["",""]
        try:
            zsmap1 = dayWayContent[3][2][1]
        except BaseException as e:
            print("赋值有误，zsmap1")
            zsmap1 = ["",""]

        cs2 = dayWayContent[4][1]
        try:
            ywgl2 = dayWayContent[4][2][0]
        except BaseException as e:
            print("赋值有误，ywgl2")
            ywgl2 = ["",""]
        luxian = string_luxian
        try:
            img2 = dayWayContent[4][2][1]
        except BaseException as e:
            print("赋值有误，img2")
            img2 = ["",""]
        try:
            zsgl2 = dayWayContent[4][2][0]
        except BaseException as e:
            print("赋值有误，zsgl2")
            zsgl2 = ["",""]
        try:
            zsmap2 = dayWayContent[4][2][1]
        except BaseException as e:
            print("赋值有误，zsmap2")
            zsmap2 = ["",""]

        cs3 = dayWayContent[5][1]
        try:
            ywgl3 = dayWayContent[5][2][0]
        except BaseException as e:
            print("赋值有误，ywgl3")
            ywgl3 = ["",""]
        luxian = string_luxian
        try:
            img3 = dayWayContent[5][2][1]
        except BaseException as e:
            print("赋值有误，img3")
            img3 = ["",""]
        try:
            zsgl3 = dayWayContent[5][2][0]
        except BaseException as e:
            print("赋值有误，zsgl3")
            zsgl3 = ["",""]
        try:
            zsmap3 = dayWayContent[5][2][1]
        except BaseException as e:
            print("赋值有误，zsmap3")
            zsmap3 = ["",""]

        cs4 = dayWayContent[6][1]
        try:
            ywgl4 = dayWayContent[6][2][0]
        except BaseException as e:
            print("赋值有误，ywgl4")
            ywgl4 = ["",""]
        luxian = string_luxian
        try:
            img4 = dayWayContent[6][2][1]
        except BaseException as e:
            print("赋值有误，img4")
            img4 = ["",""]
        try:
            zsgl4 = dayWayContent[6][2][0]
        except BaseException as e:
            print("赋值有误，zsgl4")
            zsgl4 = ["",""]
        try:
            zsmap4 = dayWayContent[6][2][1]
        except BaseException as e:
            print("赋值有误，zsmap4")
            zsmap4 = ["",""]
        sql = '''INSERT INTO data (biaoti,type,bl,day,lx,map,img,cs1,ywgl1,lx1,img1,zsgl1,zsmap1,cs2,ywgl2,lx2,img2,zsgl2,zsmap2,cs3,ywgl3,lx3,img3,zsgl3,zsmap3,cs4,ywgl4,lx4,img4,zsgl4,zsmap4  ) Values ("%s", "%s", "%s", "%s", "%s","%s", "%s", "%s", "%s", "%s","%s", "%s", "%s", "%s", "%s","%s", "%s", "%s", "%s", "%s","%s", "%s", "%s", "%s", "%s","%s", "%s", "%s", "%s", "%s","%s")''' % (
            biaoti,
            typex,
            quanzhong,
            dayx,
            luxian,
            Amap,
            img,
            cs1,
            str(ywgl1).replace("[","").replace("]","").replace("'",""),
            luxian,
            img1[0],
            str(zsgl1).replace("[", "").replace("]", "").replace("'", ""),
            zsmap1[1],
            cs2,
            str(ywgl2).replace("[","").replace("]","").replace("'",""),
            luxian,
            img2[0],
            str(zsgl2).replace("[", "").replace("]", "").replace("'", ""),
            zsmap2[1],
            cs3,
            str(ywgl3).replace("[","").replace("]","").replace("'",""),
            luxian,
            img3[0],
            str(zsgl3).replace("[", "").replace("]", "").replace("'", ""),
            zsmap3[1],
            cs4,
            str(ywgl4).replace("[","").replace("]","").replace("'",""),
            luxian,
            img4[0],
            str(zsgl4).replace("[", "").replace("]", "").replace("'", ""),
            zsmap4[1],
        )

        try:
            # 连接数据库
            self.connect()
            # 执行sql语句
            self.cursor.execute(sql)
            # 提交到数据库执行
            self.db.commit()
            # 关闭数据库
            self.close()
        except BaseException as error:
            print("Sql insert Error:",error)
            self.db.rollback()



if __name__ == "__main__":

    get = TouristCrawler()
    # for i in range(1,2):
    #     weburl = "https://vacations.ctrip.com/list/grouptravel/d-guangxi-100052.html?p=%s" %(i)
    #     get.XieCheng(weburl)
    # get.QiongYou("")
    get.MAfengWo3_GetAllCityMddid()
