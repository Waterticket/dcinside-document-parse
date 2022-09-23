import requests, re
from bs4 import BeautifulSoup

# 봇 차단을 위한 헤더 설정
headers = {
    "Connection": "keep-alive",
    "Cache-Control": "max-age=0",
    "sec-ch-ua-mobile": "?0",
    "DNT": "1",
    "Upgrade-Insecure-Requests": "1",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.37 (KHTML, like Gecko) Chrome/90.0.4430.93 Safari/537.36",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
    "Sec-Fetch-Site": "none",
    "Sec-Fetch-Mode": "navigate",
    "Sec-Fetch-User": "?1",
    "Sec-Fetch-Dest": "document",
    "Accept-Encoding": "gzip, deflate, br",
    "Accept-Language": "ko-KR,ko;q=0.9"
}

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import re

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# 글 파싱 함수
@app.get("/list")
@app.get("/list/{search_keyword}")
def article_parse(search_keyword: str = ""):
    g_type = "mgallery/board"
    url = f"https://gall.dcinside.com/{g_type}/lists/?id=pjsekai&page=1&s_type=search_subject_memo&s_keyword={search_keyword}"
    res = requests.get(url, headers=headers)
    soup = BeautifulSoup(res.text, "lxml")

    article_list = soup.select(".us-post")  # 글 박스 전부 select
    article = []
    for element in article_list:
        # 글 박스를 하나씩 반복하면서 정보 추출
        link = "https://gall.dcinside.com" + element.select("a")[0]['href'].strip()
        num = int(re.sub(r'[^0-9]', '', element.select(".gall_num")[0].text))
        subject = element.select('.gall_subject')[0].text
        title = element.select(".ub-word > a")[0].text
        reply = element.select(".ub-word > a.reply_numbox > .reply_num")
        if reply:
            reply = int(re.sub(r'[^0-9]', '', reply[0].text))
        else:
            reply = 0
        nickname = element.select(".ub-writer")[0].text.strip()
        timestamp = element.select(".gall_date")[0].text
        refresh = int(re.sub(r'[^0-9]', '', element.select(".gall_count")[0].text))
        recommend = int(re.sub(r'[^0-9]', '', element.select(".gall_recommend")[0].text))

        article.append({
            "link": link,
            "num": num,
            "subject": subject,
            "title": title,
            "reply": reply,
            "nickname": nickname,
            "timestamp": timestamp,
            "refresh": refresh,
            "recommend": recommend
        })

    return article
