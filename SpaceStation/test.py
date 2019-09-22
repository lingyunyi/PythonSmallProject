import requests,time


def Get_Web_Status_AND_Web_PING(webURL):
        try:
            # 构造requests命令
            header = {
                "User-Agent":"Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36"
            }
            r = requests.head(webURL, headers=header, verify=False, allow_redirects=True, timeout=5)
            time.sleep(10)
            print(r.status_code)
            print("------------")
            print(r.history)
            print("------------")
            print(r.headers)
            print("------------")
            print(r.raise_for_status())
            print("------------")
            r.close()
        except BaseException as e:
            print(e)

p = "http://www.nicemoe1.com"
p1 = "http://www.nicemoe2.com"
p2 = "http://www.acgnt.org"
p3 = "http://www.baidu.com"

Get_Web_Status_AND_Web_PING(p2)
