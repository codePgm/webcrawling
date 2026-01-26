import tkinter as tk
from tkinter import simpledialog, messagebox
import os
import sys
import google.generativeai as genai

def get_base_dir():
    if getattr(sys, 'frozen', False):
        return os.path.dirname(sys.executable)
    return os.path.dirname(os.path.abspath(__file__))

API_FILE = os.path.join(get_base_dir(), "api_key.txt")

def load_api_key():
    if os.path.exists(API_FILE):
        with open(API_FILE, "r", encoding="utf-8") as f:
            return f.read().strip()
    return None

#api key 입력
def get_or_create_api_key():
    key = load_api_key()
    if key:
        return key

    root = tk.Tk()
    root.withdraw()

    key = simpledialog.askstring(
        "API KEY 입력",
        "Gemini API Key를 입력하세요:",
        #show="*"
    )

    if not key:
        messagebox.showerror("오류", "API Key가 입력되지 않았습니다.")
        sys.exit(1)

    try:
        save_api_key(key)
    except PermissionError:
        messagebox.showerror(
            "권한 오류",
            "api_key.txt를 저장할 수 없습니다.\n"
            "프로그램을 쓰기 가능한 위치에서 실행하세요."
        )
        sys.exit(1)

    return key

def save_api_key(key):
    with open(API_FILE, "w", encoding="utf-8") as f:
        f.write(key)

genai.configure(api_key=get_or_create_api_key())
model = genai.GenerativeModel("gemini-2.5-flash-lite")

#베스트 크롤링 요약
def summarize(text):
    prompt = f"""
너는 기술 분석 최고 담당자다.
다음은 기술 문서 또는 설명서 본문이다.
불필요한 광고, 메뉴, 중복 문장은 제거하고 핵심 주장과 중요한 내용만 요약해줘.

요약 규칙:
- 핵심 개념 중심
- 의미 단위로 정리
- 불필요한 나열 제거
- 설명서/논문 스타일 유지

본문:
{text}
"""
    response = model.generate_content(prompt)
    return response.text.strip()

#ai 크롤링
def get_ai_content(url):
    prompt = f"""
    웹페이지: {url}
해당 웹페이지에 들어가서 본문 내용을 수정없이 그대로 가져와줘

규칙 : 
- 번역이나 요약 없이 그대로 한글자도 빼먹지않고 가져올것
- 본문 내용만 가져올것, 광고나 메뉴 등 본문 내용이 아닌것은 가져오지 말것
- 내용을 가져오는 것이 목적임으로 수정 하지말 것

"""
    response = model.generate_content(prompt)
    ai_text = response.text.strip()
    return ai_text

#로컬 vs ai 크롤링 결과 중 더 정확한거 선택
def summarize_best(url):
    # 1. 로컬 크롤링 결과
    from crawler import crawl_local  # crawler.py에서 import
    title, local_text = crawl_local(url)
    
    # 2. ai 크롤링 결과
    ai_content = get_ai_content(url)
    
    # 3. 베스트 내용으로 요약
    summary_prompt = f"""
너는 기술 분석 최고 담당자다.
나는 하나의 웹사이트를 각각 다른 방식으로 추출해왔어.
해당 웹사이트의 추출 결과를 가지고 더 정확한 추출결과를 선택해줘

요약 규칙:
- 두 개의 글중 어느 것 이 더 정확한 정보가 있는지
- 어떤 글이 짜임성이 더 좋고 문맥상 맞게 되어있는지
- 글의 완성도가 어느 것 이 더 높은지
- 글의 생각 할 수 있는 모든 부분에서의 완성도가 어느 것 이 더 좋은지
- 답변으로는 선택한 글을 나에게 다시 보내줘

1번
{local_text}
-----------------------------
2번
{ai_content}
"""
    best_crawler = model.generate_content(summary_prompt).text.strip()
    
    return best_crawler