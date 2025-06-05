import tkinter as tk
from datetime import datetime
import threading
import os
from Services.memo_loader import get_regular_memo, get_date_memo

class AlarmRingScreen:
    def __init__(self, root, controller):
        self.root = root
        self.controller = controller
        self.memo_cache = {"regular": "", "date": ""}

    def create_frame(self, parent):
        self.frame = tk.Frame(parent, bg='black')
        self.frame.pack(fill='both', expand=True)
        
        # 현재 시간
        self.time_label = tk.Label(
            self.frame,
            text="",
            fg="white",
            bg="black",
            font=("Helvetica", 60)
        )
        self.time_label.pack(pady=20)
        
        # 메모 영역
        memo_frame = tk.Frame(self.frame, bg='#222222', bd=1, relief=tk.SOLID)
        memo_frame.pack(fill=tk.X, padx=20, pady=10)
        
        self.memo_regular_label = tk.Label(
            memo_frame,
            text="",
            fg="white",
            bg="#222222",
            font=("Helvetica", 14),
            wraplength=600
        )
        self.memo_regular_label.pack(pady=5)
        
        self.date_memo_label = tk.Label(
            memo_frame,
            text="",
            fg="white",
            bg="#222222",
            font=("Helvetica", 14),
            wraplength=600
        )
        self.date_memo_label.pack(pady=5)
        
        # 안내 메시지
        self.instruction_label = tk.Label(
            self.frame,
            text="스페이스바 또는 엔터를 눌러 알람을 종료하세요",
            fg="white",
            bg="black",
            font=("Helvetica", 14)
        )
        self.instruction_label.pack(pady=20)
        
        # 키 이벤트 바인딩
        self.frame.focus_set()
        self.frame.bind('<space>', lambda e: self.stop_alarm())
        self.frame.bind('<Return>', lambda e: self.stop_alarm())
        
        self.update_time()
        self.fetch_memo()
        
        return self.frame

    def update_time(self):
        now = datetime.now()
        self.time_label.config(text=now.strftime("%H:%M:%S"))
        self.frame.after(1000, self.update_time)

    def fetch_memo(self):
        def run():
            try:
                regular = get_regular_memo()
                date = get_date_memo()
                self.memo_cache["regular"] = regular
                self.memo_cache["date"] = date
                self.frame.after(0, self.update_memo)
            except Exception as e:
                print(f"메모 가져오기 오류: {e}")
        
        threading.Thread(target=run).start()
        self.frame.after(30000, self.fetch_memo)

    def update_memo(self):
        self.memo_regular_label.config(text=f"✓ 정기 메모: {self.memo_cache['regular']}")
        self.date_memo_label.config(text=f"🗓 날짜 메모: {self.memo_cache['date']}")

    def stop_alarm(self):
        # TODO: 알람음 정지 기능 구현
        self.controller.show_screen('clock')
        print("알람 종료, 시계 화면으로 전환")

    def on_show(self):
        self.frame.focus_set()
        self.fetch_memo()

    def on_key_press(self, event):
        if event.keysym in ['space', 'Return']:
            self.stop_alarm()
