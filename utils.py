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
    filename = re.sub(r'[\/:*?"<>|]', '_', str(title))
    filename = filename[:100] + '.txt'
    return filename

def save_local_original(text, title):
    folder = "./data/local_original"
    os.makedirs(folder, exist_ok=True)
    path = os.path.join(folder, safe_filename(title))
    with open(path, "w", encoding="utf-8") as f:
        f.write(text)
    return path

def save_ai_original(text, title):
    folder = "./data/ai_original"
    os.makedirs(folder, exist_ok=True)
    path = os.path.join(folder, safe_filename(title))
    with open(path, "w", encoding="utf-8") as f:
        f.write(text)
    return path

def save_summary(text, title):
    folder = "./data/summary"
    os.makedirs(folder, exist_ok=True)
    path = os.path.join(folder, safe_filename(title))
    with open(path, "w", encoding="utf-8") as f:
        f.write(text)
    return path