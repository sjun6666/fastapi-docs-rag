import os
from dotenv import load_dotenv
import requests
import time
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
    for attempt in range(3):  # attempt 依次是 0、1、2
        try:
            response = requests.post(url="https://api.deepseek.com/chat/completions",headers=headers,json=payload,timeout=30)
        except (requests.exceptions.Timeout, requests.exceptions.ConnectionError) as e:
            wait = 2 ** attempt
            print(f"第 {attempt + 1} 次失败（{type(e).__name__}），{wait} 秒后重试")
            time.sleep(wait)
            continue

        if response.status_code >= 500:
            wait = 2 ** attempt # 空 2（和空 1 一样）
            print(f"第 {attempt + 1} 次失败（{response.status_code}），{wait} 秒后重试")
            time.sleep(wait)
            continue

        response.raise_for_status()  # 4xx 在这里直接报错，不重试
        data = response.json()
        return data["choices"][0]["message"]["content"]

    raise RuntimeError("调用 DeepSeek 失败，已重试 3 次")

if __name__ == '__main__':
    print(ask_llm("用一句话介绍 FastAPI"))