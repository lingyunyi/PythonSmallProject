import re
import requests
import random


def get_request_headers():
    # 用户代理User-Agent列表
    USER_AGENTS = [
        "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:69.0) Gecko/20100101 Firefox/69.0"
    ]

    headers = {
        "User-Agent": random.choice(USER_AGENTS),
    }
    return headers

def Get_BiliBili_Img_Url_guochan():
    try:
        r = requests.get("https://www.bilibili.com/guochuang",headers=get_request_headers(),timeout=5)
        # 获取网页所有HTML标签
        response = r.content.decode("utf-8")
        # 获取包含需要结果页面的DIV标签
        response_DIV = re.findall('<li class="chief-recom-item">(.*?)</li>', response)
        # 获取所需要的所有A标签
        response_A = re.findall('a href="(.*?)"', str(response_DIV))
        # 获取所有需要的DIV标签
        response_IMG = re.findall('img src="(.*?)@', str(response_DIV))
        for i in range(len(response_A)):
            if i < 6:
                golbalData["BiliBili"][response_A[i]] = response_IMG[i]
    except BaseException as error:
        print("Get_BiliBili_Img_Url_guochan----------\n", error)



Get_BiliBili_Img_Url_guochan()