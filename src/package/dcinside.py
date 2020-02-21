import requests
from bs4 import BeautifulSoup
from urllib.parse import urlencode
import package.db as db
import re

user_agent = 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/36.0.1985.143 Safari/537.36'
headers = {'User-Agent': user_agent}

def getUrl(url):
    res = requests.get(url, headers=headers)
    if res.status_code == 200:
        return res.text
    else:
        return None

def searchByName(keyword, gallId, page=1):
    return BeautifulSoup(
        getUrl(f"https://gall.dcinside.com/board/lists/?id={gallId}&page={page}&s_type=search_name&s_keyword={keyword}"), 'html.parser')

def searchGallId(keyword):
    return BeautifulSoup(
        getUrl(f"https://search.dcinside.com/combine/q/{keyword}"), 'html.parser')

def appendGallIdByName(keyword):
    soup = searchGallId(keyword)
    gallUrl = soup.find("ul", class_="integrate_cont_list").find("li").find("a")["href"]
    id = re.compile(r"(?:\?id=)(.*)").search(gallUrl).group(1)
    db.appendGallIdList(id)

def searchParse(author):
    gallIdList = db.getGallIdList()
    result = {}
    for gallId in gallIdList:
        gallId = gallId[0]
        oldPosts = [e[0] for e in db.getPostByAuthorAndGallId(author, gallId)]
        newPosts = []
        for page in range(1, 6):
            soup = searchByName(author, gallId, page)
            trPosts = soup.find_all("tr", class_="ub-content us-post")
            newPosts += [
                {
                    "number": e["data-no"],
                    "link": "https://gall.dcinside.com{0}".format(e.find("td", class_="gall_tit ub-word").find("a")["href"]),
                    "name": "{0} {1}".format(e.find("td", class_="gall_tit ub-word").find("a").text, e.find("span").text) if "[" in e.find("span").text else "",
                    "date": e.find("td", class_="gall_date")["title"]
                }
                for e in trPosts
                if e.find("td", class_="gall_writer ub-writer")["data-nick"] == author
                and int(e["data-no"]) not in oldPosts
            ]
        if newPosts:
            result.update({gallId: newPosts})
    return result