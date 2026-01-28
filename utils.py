import os
import re
from datetime import datetime

# 기존 save_txt 유지 (gui.py 호환)
def save_txt(text, filename, folder):
    os.makedirs(folder, exist_ok=True)
    path = os.path.join(folder, filename)
    with open(path, "w", encoding="utf-8") as f:
        f.write(text)

# 새 함수들 (제목 기반 저장)
def safe_filename(title):
    base = re.sub(r'[\/:*?"<>|]', '_', str(title))[:80]
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    return f"{base}_{timestamp}.txt"

#로컬 크롤링 결과
def save_local_original(text, title):
    folder = "./data/local_original"
    os.makedirs(folder, exist_ok=True)
    path = os.path.join(folder, safe_filename(title))
    with open(path, "w", encoding="utf-8") as f:
        f.write(text)
    return path

#ai 크롤링 결과
def save_ai_original(text, title):
    folder = "./data/ai_original"
    os.makedirs(folder, exist_ok=True)
    path = os.path.join(folder, safe_filename(title))
    with open(path, "w", encoding="utf-8") as f:
        f.write(text)
    return path

#요약된 텍스트
def save_summary(text, title):
    folder = "./data/summary"
    os.makedirs(folder, exist_ok=True)
    path = os.path.join(folder, safe_filename(title))
    with open(path, "w", encoding="utf-8") as f:
        f.write(text)
    return path

#선택된 텍스트
def save_best_crawler(text, title):
    folder = "./data/bestCrawler"
    os.makedirs(folder, exist_ok=True)
    path = os.path.join(folder, safe_filename(title))
    with open(path, "w", encoding="utf-8") as f:
        f.write(text)
    return path