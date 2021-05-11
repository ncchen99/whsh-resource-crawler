import requests
import os
import json
import urllib.parse
from bs4 import BeautifulSoup
from pprint import pprint


class Widget:
    def __init__(self, sessid, request_urls):
        self.headers = {
            'referer': 'https://www.whsh.tc.edu.tw/ischool/widget/site_news/news_pop_content.php?newsId=14028&maxRows_rsResult=15&fh=0&bid=0&uid=WID_0_2_518cd2a7e52b7f65fc750eded8b99ffcc2a7daca', 'sec-ch-ua': '" Not A;Brand";v="99", "Chromium";v="90", "Google Chrome";v="90"',
            'sec-ch-ua-mobile': '?0',
            'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.72 Safari/537.36'}

        self.cookie = {"PHPSESSID": sessid}
        self.request_urls = request_urls

    def get_all_img(self, news, board):
        url = self.request_urls["base_url"] + \
            self.request_urls["query_news_content"]["general"]["request_url"]
        data = self.request_urls["query_news_content"][board]["query_string_parameters"]
        data["nid"] = news["newsId"]
        r = requests.get(url, params=data)
        res_dict = json.loads(r.text)
        soup = BeautifulSoup(urllib.parse.unquote(
            res_dict[0]["content"]), 'html.parser')
        imgs = soup.findAll('img')
        imgs_list = []
        for img in imgs:
            if "https://www.whsh.tc.edu.tw/ischool/" in img["src"]:
                imgs_list.append(img["src"])
        return imgs_list

    def get_all_attachment(self, news, board):
        print("under dev!")

    def save_img(self, url):
        dirs = url.replace(
            "https://www.whsh.tc.edu.tw/ischool/", "").split("/")[:-1]
        path = dirs[0]
        for dir in dirs[1:]:
            if not os.path.exists(path):
                os.makedirs(path)
            path += "/" + dir
        if not os.path.exists(path):
            os.makedirs(path)

        print("downloading: ", url.replace(
            "https://www.whsh.tc.edu.tw/ischool/resources/", ""), end=" ")
        r = requests.get(url, headers=self.headers, cookies=self.cookie)
        with open(url.replace("https://www.whsh.tc.edu.tw/ischool/", ""), 'wb') as f:
            # 將圖片下載下來
            f.write(r.content)
        print("... done")

    def save_attachment(self, attachment):
        print("under dev!!")
