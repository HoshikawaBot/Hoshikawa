import requests
from bs4 import BeautifulSoup

class Crawler:
    def getUrl(self, url):
        return requests.get(url).text

class Parser:
    pass
