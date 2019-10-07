import requests
import re

class TouristCrawler(object):

    def XieCheng(self, weburl):
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



if __name__ == "__main__":

    get = TouristCrawler()
    # for i in range(1,2):
    #     weburl = "https://vacations.ctrip.com/list/grouptravel/d-guangxi-100052.html?p=%s" %(i)
    #     get.XieCheng(weburl)
    get.QiongYou("")
