import google.generativeai as genai
import json

def load_api_key():
    with open("config.json", "r", encoding="utf-8") as f:
        return json.load(f)["gemini_api_key"]

genai.configure(api_key=load_api_key())

for m in genai.list_models():
    print(m.name, m.supported_generation_methods)