import os
from dotenv import load_dotenv
import requests

load_dotenv()
API_KEY = os.getenv("DEEPSEEK_API_KEY")
if not API_KEY:
    raise ValueError("没有读取到 DEEPSEEK_API_KEY，请检查 .env 文件")
def ask_llm(prompt):
    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json",
    }
    payload = {
        "model": "deepseek-flash",
        "messages": [{"role": "user", "content": prompt}],
    }
    response = requests.post(url="https://api.deepseek.com/chat/completions",headers=headers,json=payload,timeout=30)

    response.raise_for_status()
    data = response.json()
    clean_data = data["choices"][0]["message"]["content"]
    return clean_data
if __name__ == '__main__':
    print(ask_llm("用一句话介绍 FastAPI"))