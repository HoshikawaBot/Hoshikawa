import requests
from bs4 import BeautifulSoup
from urllib.parse import urlencode

class Crawler:
    def getUrl(self, url):
        res = requests.get(url)
        if res.status_code == 200:
            return res.text
        else:
            return None
    def searchByName(self, keyword, gallid):
        return self.getUrl(f"https://gall.dcinside.com/board/lists/?id={gallid}&s_type=search_name&s_keyword={0}".format(urlencode(keyword)))

class Parser:
    def parse

