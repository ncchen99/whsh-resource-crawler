from crawler import read_yaml, get_cookies, get_news, get_resource
from pprint import pprint
request_urls = read_yaml.get_request_urls("./crawler/request_urls.yml")
PHPSESSID = get_cookies.get_PHPSESSID(request_urls["base_url"])
news_widget = get_news.Widget(PHPSESSID, request_urls)
resource_widget = get_resource.Widget(PHPSESSID, request_urls)
query_boards = request_urls["board"].keys()
for board in query_boards:
    news_list = news_widget.get_news_list(board, 20)
    for news in news_list[1:]:
        img_list = resource_widget.get_all_img(news, board)
        for img in img_list:
            resource_widget.save_img(img)
        # attachment_list = resource_widget.get_all_attachment(news, board)
        # for attachment in attachment_list:
        #     resource_widget.save_attachment(attachment)
