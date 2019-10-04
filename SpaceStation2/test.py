import requests

header = {
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36"
            }
r = requests.head("http://nicemoe1.com", headers=header, verify=False, allow_redirects=True, timeout=5)
print(r)
print(r.history)
print(r.status_code)
print(r.url)