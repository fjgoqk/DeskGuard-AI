import tkinter as tk
import subprocess
import sys
import os

# macOS 窗口修复
if sys.platform == "darwin":
    os.environ["TK_SILENCE_DEPRECATION"] = "1"

root = tk.Tk()
root.title("DeskGuard AI 控制面板")
root.geometry("360x360")
root.resizable(False, False)

root.deiconify()
root.lift()
root.focus_force()
root.attributes('-topmost', True)
root.after(100, lambda: root.attributes('-topmost', False))

root.configure(bg="#1E1E2E")

api_var = tk.BooleanVar(value=True)
cam_var = tk.BooleanVar(value=False)
interval_var = tk.StringVar(value="10")  # 🔥 这里是频率输入框

def save_config():
    try:
        interval = interval_var.get()
        with open("config.py", "w", encoding="utf-8") as f:
            f.write(f"USE_NANOBOT_API = {api_var.get()}\n")
            f.write(f"SHOW_CAMERA_WINDOW = False\n")
            f.write(f"OCR_INTERVAL = {interval}\n")  # 保存间隔
    except:
        pass

def start_main():
    save_config()
    os.system("pkill -f 'main.py'")
    subprocess.Popen([sys.executable, "main.py"])

def stop_all():
    os.system("pkill -f 'main.py'")
    root.quit()
    root.destroy()

# UI
tk.Label(root, text="DeskGuard AI 控制面板",
         font=("Arial", 16, "bold"),
         bg="#1E1E2E", fg="#FFFFFF").pack(pady=12)

tk.Checkbutton(root, text="启用 DeepSeek AI 决策", variable=api_var, command=save_config,
               bg="#1E1E2E", fg="#D0D0F0", selectcolor="#2D2B55").pack(pady=4)

tk.Checkbutton(root, text="显示摄像头画面（已关闭）", variable=cam_var, state="disabled",
               bg="#1E1E2E", fg="#8080A0", selectcolor="#2D2B55").pack(pady=4)

# 🔥 OCR 频率调节
tk.Label(root, text="⏱️ OCR/API 调用间隔（秒）(修改时间后重新启动保护程序)",
         bg="#1E1E2E", fg="#FFFFFF").pack(pady=2)
interval_entry = tk.Entry(root, textvariable=interval_var, width=10,
                         font=("Arial", 12), justify="center")
interval_entry.pack(pady=4)

tk.Button(root, text="✅ 启动保护程序", command=start_main,
          bg="#7287FD", fg="black", activebackground="#5D6BE6",
          width=18, height=2, relief="flat", bd=0,
          font=("Arial",12,"bold")).pack(pady=8)

tk.Button(root, text="❌ 关闭全部程序", command=stop_all,
          bg="#EF4444", fg="black", activebackground="#DC2626",
          width=18, height=2, relief="flat", bd=0,
          font=("Arial",12,"bold")).pack(pady=8)

save_config()
root.mainloop()