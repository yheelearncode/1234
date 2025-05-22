# screens/clock_screen.py
import tkinter as tk
from datetime import datetime
import threading
import time
from Services.weather_api import get_weather_info
from Services.memo_loader import load_today_memo

class ClockScreen:
    def __init__(self, root):
        self.root = root
        self.root.title("스마트 알람 – 기본 화면")
        self.root.geometry("480x320")
        self.root.configure(bg="black")

        # 시간 표시
        self.time_label = tk.Label(root, font=("Helvetica", 40), fg="white", bg="black")
        self.time_label.pack(pady=20)

        # 날씨/미세먼지
        self.weather_label = tk.Label(root, font=("Helvetica", 16), fg="lightblue", bg="black")
        self.weather_label.pack(pady=10)

        # 메모 표시
        self.memo_label = tk.Label(root, font=("Helvetica", 16), fg="white", bg="black", wraplength=440, justify="center")
        self.memo_label.pack(pady=20)

        self.update_time()
        self.update_info()

    def update_time(self):
        now = datetime.now().strftime("%H:%M:%S")
        self.time_label.config(text=now)
        self.root.after(1000, self.update_time)

    def update_info(self):
        weather, dust = get_weather_info()
        memo = load_today_memo()

        info_text = f"{weather} / 미세먼지: {dust}"
        self.weather_label.config(text=info_text)
        self.memo_label.config(text=memo)

        # 정보는 10분마다 갱신
        threading.Timer(600, self.update_info).start()