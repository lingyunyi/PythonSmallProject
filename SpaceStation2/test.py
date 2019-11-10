import requests
import re


def All_Bilibili_Img_Url():
    All_Url_List = [
        "https://www.bilibili.com/anime/",
        "https://www.bilibili.com/anime/",
        "https://www.bilibili.com/tv/",
        "https://www.bilibili.com/movie/",
        "https://www.bilibili.com/documentary/"

    ]
    return All_Url_List


def Get_BiliBili_Img_Url():
    All_Url_List = All_Bilibili_Img_Url()
    for bilibiliUrl in All_Url_List:
        try:
            r = requests.get(bilibiliUrl, timeout=5)
            # 获取网页所有HTML标签
            response = r.content.decode("utf-8")
            # 获取包含需要结果页面的DIV标签
            response_DIV = re.findall('<div class="carou-images">(.*?)</div>', response)
            # 获取所需要的所有A标签
            response_A = re.findall('a href="(.*?)"', str(response_DIV))
            # 获取所有需要的DIV标签
            response_IMG = re.findall('img src="(.*?)@', str(response_DIV))
            for i in range(len(response_A)):
                print("获得URL：%s" % (response_A[i]))
        except:
            print()


Get_BiliBili_Img_Url()