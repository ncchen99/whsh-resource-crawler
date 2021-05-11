import requests
import os
import json
import urllib.parse
import re
from bs4 import BeautifulSoup
from pprint import pprint


class Widget:
    def __init__(self, sessid, request_urls):
        self.headers = {
            'referer': 'https://www.whsh.tc.edu.tw/ischool/widget/', 'sec-ch-ua': '" Not A;Brand";v="99", "Chromium";v="90", "Google Chrome";v="90"',
            'sec-ch-ua-mobile': '?0',
            'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.72 Safari/537.36'}

        self.cookie = {"PHPSESSID": sessid}
        self.request_urls = request_urls
        self.percent_encode = {"%21": "!", "%23": "#", "%24": "$", "%26": "&", "%27": "'", "%28": "(", "%29": ")", "%2A": "*", "%2B": "+", "%2C": ",", "%2F": "/",
                               "%3A": ":", "%3B": ";", "%3D%": "=", "%3F": "?", "%40": "@", "%5B": "[", "%5D": "]", "%20": " "}

    def hex_to_char(self, hex_str):
        """ converts a single hex-encoded character 'FFFF' into the corresponding real character """
        return chr(int(hex_str, 16))

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
            if self.request_urls["base_url"] in img["src"]:
                imgs_list.append(img["src"])
        return imgs_list

    def get_all_attachment(self, news, board):
        url = self.request_urls["base_url"] + \
            self.request_urls["query_news_content"]["general"]["request_url"]
        data = self.request_urls["query_news_content"][board]["query_string_parameters"]
        data["nid"] = news["newsId"]
        r = requests.get(url, params=data)
        res_dict = json.loads(r.text)

        attachment_list = []
        attachments = json.loads(res_dict[0]["attachedfile"])
        for attachment in attachments:
            match_percent_decode = re.findall(
                r"%([0-9a-fA-F]{2})", attachment[-1])
            for sign in match_percent_decode:
                attachment[-1] = attachment[-1].replace(
                    "%"+sign, self.percent_encode["%"+sign])
            attachment_list.append(
                self.request_urls["base_url"]
                + "resources/"+res_dict[0]["uid"] + "/"
                + res_dict[0]["resources"] + "/attached/"
                + re.compile(r"%u([0-9a-fA-F]{4})").sub(
                    lambda m: self.hex_to_char(m.group(1)), attachment[-1]))
            print(attachment_list[-1])
        return attachment_list

    def save_img(self, url):
        dirs = url.replace(
            self.request_urls["base_url"], "").split("/")[:-1]
        path = dirs[0]
        for dir in dirs[1:]:
            if not os.path.exists(path):
                os.makedirs(path)
            path += "/" + dir
        if not os.path.exists(path):
            os.makedirs(path)

        print("downloading: ", url.replace(
            self.request_urls["base_url"] + "resources/", ""), end=" ")
        r = requests.get(url, headers=self.headers, cookies=self.cookie)
        with open(url.replace(self.request_urls["base_url"], ""), 'wb') as f:
            # 將圖片下載下來
            f.write(r.content)
        print("... done")

    def save_attachment(self, url):
        dirs = url.replace(
            self.request_urls["base_url"], "").split("/")[:-1]
        path = dirs[0]
        for dir in dirs[1:]:
            if not os.path.exists(path):
                os.makedirs(path)
            path += "/" + dir
        if not os.path.exists(path):
            os.makedirs(path)
        print("downloading: ", url.replace(
            self.request_urls["base_url"] + "resources/", ""), end=" ")
        r = requests.get(url, headers=self.headers, cookies=self.cookie)
        with open(url.replace(self.request_urls["base_url"], ""), 'wb') as f:
            # 將圖片下載下來
            f.write(r.content)
        print("... done")
