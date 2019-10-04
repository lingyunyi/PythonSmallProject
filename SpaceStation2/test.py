import re
import requests

def Get_Web_Status(webURL):
    header = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36"
    }
    r = requests.head(webURL, headers=header, verify=False, allow_redirects=True, timeout=5)
    # r.history != [] 就代表r.history有值， 但是这样并不能代表地址跳转成别的页面，我们还要验证他等于https的情况
    web_perfix = webURL.split(":")[0]
    webURLs = webURL.replace(web_perfix, "https")
    print(r.history)
    print(r.url)
    print(r.history != [])
    print(r.url != webURLs)
    if r.history != [] and r.url != webURLs:
        print("*************************",r.status_code)
    else:
        print("---------------------------",r.status_code)
    r.close()


Get_Web_Status("http://nicemoe1.com")