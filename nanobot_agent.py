import json
import requests
import os

def load_api_key():
    try:
        with open("settings.json", "r", encoding="utf-8") as f:
            return json.load(f).get("DEEPSEEK_API_KEY", "").strip()
    except:
        return ""

DEEPSEEK_API_KEY = load_api_key()
API_URL = "https://api.deepseek.com/v1/chat/completions"

def ai_decision(people_count, screen_text):
    if not DEEPSEEK_API_KEY:
        return {
            "need_cover": False,
            "activity": "no_key",
            "reason": "未配置 API Key"
        }

    prompt = f"""你是一个电脑屏幕行为分析助手。

根据下面的【屏幕文字】和【人数】，判断：
1. 用户正在：工作 / 学习 / 娱乐摸鱼 / 浏览网页 / 看视频
2. 人数：{people_count}
3. 如果人数≥2 且 在摸鱼/娱乐/看视频 → 需要隐藏保护
4. 如果在工作/学习 → 即使有人也不保护
5. 只返回JSON，不要多余内容，不要解释，不要换行

屏幕文字：
{screen_text}

输出格式：
{{"activity":"","need_cover":false,"reason":""}}
"""

    headers = {
        "Authorization": f"Bearer {DEEPSEEK_API_KEY}",
        "Content-Type": "application/json"
    }

    data = {
        "model": "deepseek-chat",
        "messages": [{"role": "user", "content": prompt}],
        "temperature": 0.1
    }

    try:
        resp = requests.post(API_URL, headers=headers, json=data, timeout=10)
        result = resp.json()
        content = result["choices"][0]["message"]["content"].strip()

        try:
            return json.loads(content)
        except:
            return {
                "activity": "解析失败",
                "need_cover": False,
                "reason": "AI返回格式异常"
            }

    except Exception as e:
        print(f"AI错误：{e}")
        return {
            "activity": "AI请求失败",
            "need_cover": False,
            "reason": "AI请求超时或网络异常"
        }