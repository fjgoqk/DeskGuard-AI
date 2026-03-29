from PIL import ImageGrab, Image
import pytesseract
import time

OCR_INTERVAL_SECONDS = 10
last_ocr_time = 0
last_result = ""

def capture_and_ocr():
    global last_ocr_time, last_result
    current = time.time()

    if current - last_ocr_time < OCR_INTERVAL_SECONDS:
        return last_result

    try:
        img = ImageGrab.grab()
        if img.mode == "RGBA":
            img = img.convert("RGB")

        # 🔥 返回完整的屏幕文字，给AI判断
        text = pytesseract.image_to_string(img, lang="chi_sim+eng")
        text = text.strip()[:2000]  # 取前2000字符
        last_ocr_time = current
        last_result = text
        return text

    except Exception as e:
        print(f"❌ OCR异常: {e}")
        return last_result

def get_screen_text():
    return capture_and_ocr()