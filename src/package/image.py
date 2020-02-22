import requests


user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.130 Safari/537.36'
ref = "https://gall.dcinside.com/board/view/?id=game_classic1&no=3760620&page=1"

            # {
            #   "name": "Host",
            #   "value": "dcimg7.dcinside.co.kr"
            # },
            # {
            #   "name": "Connection",
            #   "value": "keep-alive"
            # },
            # {
            #   "name": "User-Agent",
            #   "value": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.130 Safari/537.36"
            # },
            # {
            #   "name": "DNT",
            #   "value": "1"
            # },
            # {
            #   "name": "Accept",
            #   "value": "image/webp,image/apng,image/*,*/*;q=0.8"
            # },
            # {
            #   "name": "Sec-Fetch-Site",
            #   "value": "cross-site"
            # },
            # {
            #   "name": "Sec-Fetch-Mode",
            #   "value": "no-cors"
            # },
            # {
            #   "name": "Referer",
            #   "value": "https://gall.dcinside.com/board/view/?id=game_classic1&no=3760620&page=1"
            # },
            # {
            #   "name": "Accept-Encoding",
            #   "value": "gzip, deflate, br"
            # },
            # {
            #   "name": "Accept-Language",
            #   "value": "ko-KR,ko;q=0.9,en-US;q=0.8,en;q=0.7,ja;q=0.6"
            # }
headers = {
    'User-Agent': user_agent,
    "Accept-Language": "ko-KR,ko;q=0.9,en-US;q=0.8,en;q=0.7,ja;q=0.6",
    "Accept": "image/webp,image/apng,image/*,*/*;q=0.8",
    "Connection": "keep-alive",
    "Host": "dcimg7.dcinside.co.kr",
    "Referer": ref
}
res = requests.get("https://dcimg7.dcinside.co.kr/viewimage.php?no=24b0d769e1d32ca73ced83fa11d0283109f613b0c2e59fad7a6296a8113182d70e40de0b7c0002e66741d7d9cdbe9a515f332b8a730026c0efe3adfaa74d409074e3ae7d5bd6ae5d56367a7441ba7efa7b46bdc49b620e307b&orgExt")

print(res.status_code)
if res.status_code == 200:
    with open("image.png", "wb+") as w:
        w.write(res.content)