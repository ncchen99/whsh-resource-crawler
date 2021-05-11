from selenium import webdriver
import requests
import time


def get_PHPSESSID(url):
    # ==========================================================================
    #     driver = webdriver.Chrome("./crawler/chromedriver")
    #     driver.get(url)

    #     # 获得cookie信息
    #     cookies = driver.get_cookies()

    #     # 将获得cookie的信息打印
    #     for item in cookies:
    #         if(item["name"] == "PHPSESSID"):
    #             PHPSESSID = item["value"]
    #     driver.quit()
    # ===========================================================================
    # 不用使用 selenium
    res = requests.get(url)
    return res.cookies["PHPSESSID"]
