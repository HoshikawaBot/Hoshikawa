import requests
from bs4 import BeautifulSoup
from urllib.parse import urlencode
import db

def getUrl(url):
    res = requests.get(url)
    if res.status_code == 200:
        return res.text
    else:
        return None

def searchByName(keyword, gallId):
    return BeautifulSoup(
        getUrl(f"https://gall.dcinside.com/board/lists/?id={gallId}&s_type=search_name&s_keyword={0}"
        .format(urlencode(keyword)))
        , 'html-parser')

def searchParse(author):
    gallIdList = db.getGallIdList()
    result = {}
    for gallId in gallIdList:
        soup = searchByName(author, gallId)
        trPosts = soup.find_all("tr", class_="ub-content us-post")
        oldPosts = set(db.getPostByAuthorAndGallID(author, gallId))
        newPosts = [
            {
                "number": e["data-no"],
                "link": "https://gall.dcinside.com{0}".format(e.find("td", class_="gall_tit ub-word")),
                "name": "{0} {1}".format(e.find("em").text, e.find("span").text)
            }
            for e in trPosts
            if e.find("td", class_="gall_writer ub-writer")["data-nick"] == author
            and e["data-no"] not in oldPosts
        ]
        if newPosts:
            result.update(gallId, newPosts)
    return result