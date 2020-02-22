import requests
from bs4 import BeautifulSoup
import package.db as db
import re
import io

user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.130 Safari/537.36'
headers = {'User-Agent': user_agent}

def getUrl(url):
    try:
        res = requests.get(url, headers=headers, allow_redirects=True)
        if res.status_code == 200:
            return res.text
        else:
            return None
    except:
        return None

def searchByName(keyword, gallId, search_pos=0, page=1):
    html = getUrl(f"https://gall.dcinside.com/board/lists/?id={gallId}&page={page}&search_pos={search_pos}&s_type=search_name&s_keyword={keyword}")
    if html.startswith("<script"):
        html = getUrl(f"https://gall.dcinside.com/mgallery/board/lists/?id={gallId}&page={page}&search_pos={search_pos}&s_type=search_name&s_keyword={keyword}")
    if html is None:
        return None
    soup = BeautifulSoup(html, 'html.parser')
    return soup
def searchGallId(keyword):
    html = getUrl(f"https://search.dcinside.com/combine/q/{keyword}")
    if html is None:
        return None
    return BeautifulSoup(
        html, 'html.parser')

def appendGallIdByName(keyword):
    soup = searchGallId(keyword)
    gallUrl = soup.find("ul", class_="integrate_cont_list").find("li").find("a")["href"]
    id = re.compile(r"(?:\?id=)(.*)").search(gallUrl).group(1)
    db.appendGallIdList(id)
    return id

def safe_int(value, default=0):
    try:
        return int(value)
    except:
        return default

def searchParse(author):
    gallIdList = db.getGallIdList()
    result = {}
    for gallId in gallIdList:
        oldPosts = db.getPostByAuthorAndGallId(author, gallId)
        newPosts = []
        search_pos = 0
        page = 1
        for i in range(5):
            soup = searchByName(author, gallId, search_pos, page)
            if soup is None:
                continue
            trPosts = soup.find_all("tr", class_="ub-content us-post")
            if len(trPosts) == 0:
                break
            try:
                temp = [
                    {
                        "number": int(e["data-no"]),
                        "link": "https://gall.dcinside.com{0}".format(e.find("td", class_="gall_tit ub-word").find("a")["href"]),
                        "name": "{0} {1}".format(e.find("td", class_="gall_tit ub-word").find("a").text, e.find("span").text) if "[" in e.find("span").text else e.find("td", class_="gall_tit ub-word").find("a").text,
                        "date": e.find("td", class_="gall_date")["title"],     
                        "file": io.BytesIO(getUrl("https://gall.dcinside.com{0}".format(e.find("td", class_="gall_tit ub-word").find("a")["href"])).encode('utf-8'))
                    }
                    for e in trPosts if e is not None and e.find("td", class_="gall_writer ub-writer")["data-nick"] == author
                ]
                dup = [e["number"] for e in temp if e["number"] in oldPosts]
                if dup:
                    temp = [e for e in temp if e["number"] not in dup]
                    newPosts += temp
                    break
                else:
                    newPosts += temp
                    botpagebox = soup.find("div", class_="bottom_paging_box")
                    pages = [safe_int(a.text) for a in botpagebox.find_all("a")]
                    maxPage = max(pages)
                    if maxPage > page:
                        page += 1
                        continue

                    if search_pos == 0:
                        href = soup.find("a", class_="search_next")["href"]
                        search_pos = int(re.compile(r"search_pos=(-\d*)").search(href).group(1))
                        page = 1
                    else:
                        search_pos += 10000
                        page = 1
            except Exception as e:
                try:
                    botpagebox = soup.find("div", class_="bottom_paging_box")
                    pages = [safe_int(a.text) for a in botpagebox.find_all("a")]
                    maxPage = max(pages)
                    if maxPage > page:
                        page += 1
                        continue

                    if search_pos == 0:
                        href = soup.find("a", class_="search_next")["href"]
                        search_pos = int(re.compile(r"search_pos=(-\d*)").search(href).group(1))
                        page = 1
                    else:
                        search_pos += 10000
                        page = 1
                except:
                    continue
            
        if newPosts:
            result.update({gallId: newPosts[::-1]})
    return result