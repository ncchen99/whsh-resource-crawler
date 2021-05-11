import requests
import json


class Widget:
    def __init__(self, sessid, request_urls):
        self.sessid = sessid
        self.request_urls = request_urls

    def get_news_list(self, board, max_rows):
        url = self.request_urls["base_url"] + \
            self.request_urls["board"][board]["general"]["request_url"]
        data = self.request_urls["board"][board]["query_string_parameters"]
        data["maxRows"] = max_rows
        if self.request_urls["board"][board]["general"]["request_method"] == "POST":
            res = requests.post(url, data=data)
        if self.request_urls["board"][board]["general"]["request_method"] == "GET":
            res = requests.get(url, params=data)
        news_list = json.loads(res.text)
        return news_list
