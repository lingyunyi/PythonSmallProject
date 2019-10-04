import requests,re


def Get_BiliBili_Img_Url():
    try:
        header = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36"
        }
        r = requests.get("https://www.bilibili.com/guochuang/", headers=header,timeout=5)
        # 获取网页所有HTML标签
        response = r.content.decode("utf-8")
        # 获取包含需要结果页面的DIV标签
        response_DIV = re.findall('<div class="carou-images">(.*?)</div>',response)
        # 先找到所有的LI
        response_LI = re.findall('<ul class="carou-images-wrapper clearfix">(.*?)</ui>',str(response_DIV))
        # 获取所需要的所有A标签
        response_A = re.findall('a href="(.*?)"',str(response_LI))
        # 获取所有需要的DIV标签
        response_IMG = re.findall('img src="(.*?)@',str(response_LI))
        print(response_A)
        print(response_IMG)
        print(len(response_A))
        print(len(response_IMG))




    except BaseException as error:
        print("Get_BiliBili_Img_Url----------\n", error)



Get_BiliBili_Img_Url()
