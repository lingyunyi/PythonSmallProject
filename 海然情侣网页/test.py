import requests, random, re


class Qixinbao(object):

    def __init__(self):
        self.begin_url = "https://www.qixin.com/search?key={}&page=1"

    def get_frist_url(self, key):
        '''
            获取查询的第一条url
        '''
        if key == "":
            return False
        search_url = self.begin_url.format(str(key))
        r = requests.get(search_url, headers=self.get_request_headers(), verify=False, allow_redirects=True, timeout=5,)
        print(r.status_code)
        if r.status_code == 200:
            tempstr1 = re.findall(r'<div class="company-title font-18 font-f1">(.*?)</div>', r.text)
            tempstr2 = re.findall(r'<a href="(.*?)"', tempstr1[0])
            tempstr3 = tempstr2[0]
            self.url = "https://www.qixin.com{}".format(tempstr3)
            url = self.url
            print(self.url,url)
        url = None
        self.r_cookies = r.cookies
        return url

    def get_url_content(self):
        '''
        获取url内的内容
        '''
        if self.url != "":
            print(self.url)
            r = requests.get(self.url, headers=self.get_request_headers(), verify=False, allow_redirects=True, timeout=5,
                             cookies=self.r_cookies)
            print(r.text)

    def get_request_headers(self):
        '''
            # 用户代理User-Agent列表
        '''
        USER_AGENTS = [
            "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36",
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:69.0) Gecko/20100101 Firefox/69.0"
        ]

        headers = {
            "User-Agent": random.choice(USER_AGENTS),
        }
        return headers


if __name__ == "__main__":
    a = Qixinbao()
    print(a.get_frist_url("奇安信"))
