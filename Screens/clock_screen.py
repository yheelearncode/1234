import tkinter as tk
from datetime import datetime
import threading
from Services.memo_loader import get_regular_memo, get_date_memos
from Services.weather_api import get_weather
from Services.alarm_manager import get_regular_alarms, get_temporary_alarm

class ClockScreen:
    def __init__(self, root, controller):
        self.root = root
        self.controller = controller
        self.weather_cache = {'weather': '-', 'temperature': '-', 'dust': '-'}
        self.memo_cache = {'regular': '', 'date_memos': {}}
        self.alarm_cache = {'regular': [], 'temp': None}

    def create_frame(self, parent):
        self.frame = tk.Frame(parent, bg='black')
        self.frame.pack(fill='both', expand=True)
        
        # 시간과 날짜
        self.date_label = tk.Label(self.frame, text="", fg="white", bg="black", font=("Helvetica", 18))
        self.date_label.pack(pady=10)
        
        self.time_label = tk.Label(self.frame, text="", fg="white", bg="black", font=("Helvetica", 36))
        self.time_label.pack(pady=10)
        
        # 날씨/미세먼지
        weather_frame = tk.Frame(self.frame, bg='black')
        weather_frame.pack(pady=10)
        
        self.weather_label = tk.Label(weather_frame, text="", fg="white", bg="black", font=("Helvetica", 14))
        self.weather_label.pack(side=tk.LEFT, padx=10)
        
        self.dust_label = tk.Label(weather_frame, text="", fg="white", bg="black", font=("Helvetica", 14))
        self.dust_label.pack(side=tk.LEFT, padx=10)
        
        # 메모 영역
        memo_frame = tk.Frame(self.frame, bg='#222222', bd=1, relief=tk.SOLID)
        memo_frame.pack(fill=tk.X, padx=20, pady=10)
        
        self.memo_regular_label = tk.Label(memo_frame, text="", fg="white", bg="#222222", font=("Helvetica", 14), wraplength=600)
        self.memo_regular_label.pack(pady=5)
        
        self.date_memo_label = tk.Label(memo_frame, text="", fg="white", bg="#222222", font=("Helvetica", 14), wraplength=600)
        self.date_memo_label.pack(pady=5)
        
        # 알람 영역
        alarm_frame = tk.Frame(self.frame, bg='#222222', bd=1, relief=tk.SOLID)
        alarm_frame.pack(fill=tk.X, padx=20, pady=10)
        
        self.alarm_regular_label = tk.Label(alarm_frame, text="", fg="white", bg="#222222", font=("Helvetica", 14), wraplength=600)
        self.alarm_regular_label.pack(pady=5)
        
        self.alarm_temp_label = tk.Label(alarm_frame, text="", fg="white", bg="#222222", font=("Helvetica", 14), wraplength=600)
        self.alarm_temp_label.pack(pady=5)
        
        self.update_time()
        self.fetch_all_data()
        
        return self.frame

    def update_time(self):
        now = datetime.now()
        self.date_label.config(text=now.strftime("%Y-%m-%d (%A)"))
        self.time_label.config(text=now.strftime("%H:%M:%S"))
        self.frame.after(1000, self.update_time)

    def fetch_all_data(self):
        def run():
            try:
                weather = get_weather()
                regular_memo = get_regular_memo()
                date_memos = get_date_memos()
                regular_alarms = get_regular_alarms()
                temp_alarm = get_temporary_alarm()
                
                self.weather_cache = weather
                self.memo_cache = {
                    "regular": regular_memo,
                    "date_memos": date_memos,
                }
                self.alarm_cache = {
                    "regular": regular_alarms,
                    "temp": temp_alarm,
                }
                
                self.frame.after(0, self.update_info)
            except Exception as e:
                print(f"데이터 가져오기 오류: {e}")
        
        threading.Thread(target=run).start()
        self.frame.after(60000, self.fetch_all_data)

    def update_info(self):
        # 날씨
        w = self.weather_cache
        self.weather_label.config(text=f"☁ 날씨: {w['weather']} {w['temperature']}")
        self.dust_label.config(text=f"🌫 미세먼지: {w['dust']}")

        # 정기 메모
        regular_memo = self.memo_cache["regular"]
        if regular_memo:
            self.memo_regular_label.config(text=f"✓ 정기 메모: {regular_memo}")
        else:
            self.memo_regular_label.config(text="✓ 정기 메모: 없음")

        # 날짜 메모
        now = datetime.now()
        today = now.strftime("%Y-%m-%d")
        date_memos = self.memo_cache["date_memos"]
        if today in date_memos:
            self.date_memo_label.config(text=f"🗓 오늘의 메모: {date_memos[today]}")
        else:
            next_memo = None
            next_date = None
            for date in sorted(date_memos.keys()):
                if date > today:
                    next_memo = date_memos[date]
                    next_date = date
                    break
            if next_memo:
                self.date_memo_label.config(text=f"🗓 다음 메모 ({next_date}): {next_memo}")
            else:
                self.date_memo_label.config(text="🗓 예정된 메모 없음")

        # 정기 알람
        alarms = self.alarm_cache["regular"]
        if alarms:
            alarm_texts = [f"{time} ({label})" for time, label in alarms]
            self.alarm_regular_label.config(text="🔔 정기 알람: " + ", ".join(alarm_texts))
        else:
            self.alarm_regular_label.config(text="🔔 정기 알람 없음")

        # 임시 알람
        temp_alarm = self.alarm_cache["temp"]
        if temp_alarm:
            self.alarm_temp_label.config(text=f"⏰ 임시 알람: {temp_alarm}")
        else:
            self.alarm_temp_label.config(text="⏰ 임시 알람 없음")

    def on_show(self):
        self.fetch_all_data()

    def on_key_press(self, event):
        pass
