from selenium import webdriver
from time import sleep

# browser = webdriver.Chrome()  # 谷歌浏览器


def getcookies(account,password):
    try:
        # driver = webdriver.PhantomJS(executable_path= r"D:\Backup\Downloads\phantomjs-2.1.1-windows(1)\phantomjs-2.1.1-windows\bin\phantomjs.exe")  # 火狐浏览器
        # driver = webdriver.Firefox(executable_path=r"D:\Software\Mozilla Firefox\firefox.exe")
        # driver = webdriver.Chrome(executable_path="C:\Program Files (x86)\Google\Chrome\Application\chrome.exe")
        driver = webdriver.Firefox()
        driver.get("http://e.huya.com/")
        driver.find_element_by_xpath("/html/body/div[1]/div/div/div[1]/div/div/a").click()
        sleep(5)
        driver.switch_to_frame(driver.find_element_by_xpath('//*[@id="UDBSdkLgn_iframe"]'))
        driver.find_element_by_xpath("/html/body/div[1]/div[1]/div[2]/div[1]/div[1]/div[1]/div[1]/input").send_keys(account)
        driver.find_element_by_xpath("/html/body/div[1]/div[1]/div[2]/div[1]/div[1]/div[1]/div[2]/input").send_keys(password)
        # driver.find_element_by_class_name("udb-input udb-input-account").send_keys(account)
        # driver.find_element_by_class_name("udb-input udb-input-pw").send_keys(password)
        sleep(1)
        driver.find_element_by_xpath('//*[@id="login-btn"]').click()
        cookies = driver.get_cookies()
        return cookies
    except BaseException as er:
        print(er)
        getcookies(account,password)



def re_getcookies(account,password):





    pass
    return


if __name__ == "__main__":
    account = "ywhy004"
    password = "Yw123456"
    cookies = getcookies(account,password)
    print(cookies)