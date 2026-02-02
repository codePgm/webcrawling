import google.generativeai as genai
import requests

class OllamaModel:
    def __init__(self, model="gemma3:4b"): #model 이 안들어오면 초기 값
        self.model = model
        self.url = "http://localhost:11434/api/generate"

    def generate(self, prompt):
        payload = {
            "model": self.model,
            "prompt": prompt,
            "stream": False
        }
        r = requests.post(self.url, json=payload)
        r.raise_for_status()
        return r.json()["response"]

# init
def init_gemini(api_key, model_name="gemini-3-flash-preview"):
    genai.configure(api_key=api_key)
    return genai.GenerativeModel(model_name)

def init_ollama(model_name):
    return OllamaModel(model_name)

#크롤링 내용 요약
def summarize(model, text):
    prompt = f"""
대화는 한글(한국어)로 할 거야
너는 문서 요약 최고 전문가야.
방금 내가 준 글, 문서를 보고 핵심 내용 위주로 정리해서 한국어(한글)로 대답해줘
불필요한 광고, 메뉴, 중복 문장은 제거하고 핵심 주장과 중요한 내용만 요약해줘

본문:
{text}

규칙:
- 핵심 개념 중심
- 의미 단위로 정리
- 불필요한 나열 제거
- 설명서/논문 스타일 유지
- 대답은 한국어(한글)로 작성할 것
"""
    if hasattr(model, "generate_content"): #제미나이
        response = model.generate_content(prompt)
        return response.text.strip()
    else : #올라마
        return model.generate(prompt)

#ai 크롤링 [ 사용 불가 = 환각작동 ]
def get_ai_content(model, url):
    prompt = f"""
    웹페이지: {url}
해당 웹페이지에 들어가서 너가 판단 한 본문 내용을 수정없이 그대로 가져와줘
다른 내용은 필요없어, 본문 내용만 있으면 돼

중요 규칙 :
- 절대로 없는 내용은 생성하지 말 것
- URL에 접속 할 수 없다면 답변에 [ 접속 불가 ] 라고 쓰고 이유를 적을 것
- 크롤링을 실패하면 답변에 [ 크롤링 실패 ] 라고 쓰고 이유를 적을 것
- "절대로" 임의의 내용 생성 금지

규칙 : 
- 번역이나 요약 없이 그대로 한글자도 빼먹지않고 가져올것
- 본문 내용만 가져올것, 광고나 메뉴 등 본문 내용이 아닌것은 가져오지 말것
- 내용을 가져오는 것이 목적임으로 수정 하지말 것

"""
    ai_text = model.generate(prompt)
    return ai_text, url

#로컬 vs ai 크롤링 결과 중 더 정확한거 선택
def summarize_best(model, local_text,ai_text):
    
    # 베스트 내용으로 선택
    prompt = f"""
나는 하나의 웹사이트를 각각 다른 방식으로 추출해왔어.
해당 웹사이트의 추출 결과를 가지고 더 정확한 추출결과를 선택해줘
글을 선택하면 선택한 글을 그대로 다시 나한테 보내줘

규칙:
- 두 개의 글중 어느 것 이 더 정확한 정보가 있는지
- 어떤 글이 짜임성이 더 좋고 문맥상 맞게 되어있는지
- 글의 완성도가 어느 것 이 더 높은지
- 글의 생각 할 수 있는 모든 부분에서의 완성도가 어느 것 이 더 좋은지
- 선택한 글은 나에게 변화시키지않고 그대로 다시 보낼 것

1번
{local_text}
-----------------------------
2번
{ai_text}
"""
    return model.generate(prompt)