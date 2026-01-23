import requests
import os
from bs4 import BeautifulSoup

def crawl(url):
    response = requests.get(url)
    response.raise_for_status()

    soup = BeautifulSoup(response.text, "html.parser")
    title = soup.title.text.strip()
    body = soup.select_one("div.col-main-content")

    text = body.get_text("\n", strip=True)
    return title, text


def save_txt(text, folder="./data", filename="document.txt"):
    os.makedirs(folder, exist_ok=True)   # data 폴더 없으면 생성
    path = os.path.join(folder, filename)

    with open(path, "w", encoding="utf-8") as f:
        f.write(text)


# 실행부
url = "https://developer.nvidia.com/drive/documentation"
title, text = crawl(url)

print("페이지 제목:", title)
save_txt(text)