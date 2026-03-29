import time
import base64
import requests

API_KEY = "sk-f1107afe9f8542bd9657f796c4936a68"
URL = "https://api.deepseek.com/v1/chat/completions"
IMAGE_PATH = "screenshots/screen.jpg"

with open(IMAGE_PATH, "rb") as f:
    b64 = base64.b64encode(f.read()).decode()

prompt = "分析屏幕内容，只返回：工作模式/娱乐摸鱼模式/普通模式"

headers = {
    "Authorization": f"Bearer {API_KEY}",
    "Content-Type": "application/json"
}

data = {
    "model": "deepseek-chat",
    "messages": [
        {"role": "user", "content": prompt}
    ],
    "temperature": 0.1
}

# 测速
start = time.time()
try:
    print("📤 发送请求...")
    resp = requests.post(URL, headers=headers, json=data, timeout=15)
    result = resp.json()
    content = result.get("choices", [{}])[0].get("message", {}).get("content", "无返回")
except Exception as e:
    content = f"错误：{str(e)}"

end = time.time()

print(f"\n✅ 耗时：{round(end-start,2)}s")
print(f"🧠 结果：{content}")
print(f"📦 完整返回：{resp.text if 'resp' in locals() else '请求失败'}")