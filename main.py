import json
import time
import importlib
import os
import sys

from detector import detect_people
from screen_ocr import get_screen_text, OCR_INTERVAL_SECONDS
from window_control import cover_mode

print("✅ DeskGuard AI 启动成功！")

def has_valid_api_key():
    try:
        with open("settings.json", "r", encoding="utf-8") as f:
            key = json.load(f).get("DEEPSEEK_API_KEY", "").strip()
        return len(key) > 0 and key.startswith("sk-")
    except:
        return False

while True:
    try:
        import config
        importlib.reload(config)
        USE_NANOBOT_API = config.USE_NANOBOT_API
        OCR_INTERVAL_SECONDS = int(getattr(config, "OCR_INTERVAL", 10))

        people = detect_people()
        screen_text = get_screen_text()
        need_cover = False
        reason = ""
        activity = ""

        print("\n--------------------------")
        print(f"👀 人数：{people}")
        print(f"🤖 AI模式：{USE_NANOBOT_API}")
        print(f"⏱️ 检测间隔：{OCR_INTERVAL_SECONDS}s")

        if USE_NANOBOT_API:
            if not has_valid_api_key():
                reason = "未配置 API Key → 普通模式"
                need_cover = people >= 2
            else:
                from nanobot_agent import ai_decision
                decision = ai_decision(people, screen_text)
                need_cover = decision.get("need_cover", False)
                activity = decision.get("activity", "未知")
                reason = decision.get("reason", "")
        else:
            need_cover = people >= 2
            reason = "普通模式：人数≥2则保护"
            activity = ""

        print(f"💼 当前行为：{activity}")
        print(f"🎯 最终决策：{need_cover} | {reason}")

        if need_cover:
            print("🔒 触发保护！")
            cover_mode()

        time.sleep(1)

    except Exception as e:
        print(f"⚠️ 异常：{e}")
        time.sleep(1)