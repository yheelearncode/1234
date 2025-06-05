import tkinter as tk
from tkinter import ttk
import datetime
import threading
from Services.memo_loader import get_regular_memo, get_date_memos
from Services.weather_api import get_weather
from Services.alarm_manager import get_regular_alarms, get_temporary_alarm

class ClockScreen(tk.Frame):
    def __init__(self, controller):
        super().__init__(controller, bg='black')
        self.controller = controller
        
        # 캐시 구조
        self.weather_cache = {'weather': '-', 'temperature': '-', 'dust': '-'}
        self.memo_cache = {'regular': '', 'date_memos': {}}
        self.alarm_cache = {'regular': [], 'temp': None}
        
        self.setup_ui()
        self.start_timers()

    def setup_ui(self):
        """UI 구성"""
        main_frame = tk.Frame(self, bg='black')
        main_frame.pack(expand=True, fill='both', padx=20, pady=20)

        # 날짜
        self.date_label = tk.Label(main_frame, text="", fg='white', bg='black', font=('Arial', 16))
        self.date_label.pack(pady=(0, 10))

        # 시간
        self.time_label = tk.Label(main_frame, text="", fg='white', bg='black', font=('Arial', 60, 'bold'))
        self.time_label.pack(pady=(0, 15))

        # 날씨/미세먼지
        weather_frame = tk.Frame(main_frame, bg='black')
        weather_frame.pack(fill='x', pady=(0, 15))

        self.weather_label = tk.Label(weather_frame, text="", fg='white', bg='black', font=('Arial', 12))
        self.weather_label.pack(side='left', expand=True)

        self.dust_label = tk.Label(weather_frame, text="", fg='white', bg='black', font=('Arial', 12))
        self.dust_label.pack(side='right', expand=True)

        # 메모 박스
        memo_frame = tk.Frame(main_frame, bg='#222222', relief='solid', bd=1)
        memo_frame.pack(fill='x', pady=(0, 15))

        self.memo_regular_label = tk.Label(memo_frame, text="", fg='white', bg='#222222', font=('Arial', 12), wraplength=600, justify='left')
        self.memo_regular_label.pack(fill='x', padx=10, pady=(10, 5))

        separator1 = tk.Frame(memo_frame, height=1, bg='#555555')
        separator1.pack(fill='x', padx=10)

        self.date_memo_label = tk.Label(memo_frame, text="", fg='white', bg='#222222', 
                                        font=('Arial', 12), wraplength=600, justify='left')
        self.date_memo_label.pack(fill='x', padx=10, pady=(5, 10))

        # 알람 박스
        alarm_frame = tk.Frame(main_frame, bg='#222222', relief='solid', bd=1)
        alarm_frame.pack(fill='x')

        self.alarm_regular_label = tk.Label(alarm_frame, text="", fg='white', bg='#222222', font=('Arial', 12), wraplength=600, justify='left')
        self.alarm_regular_label.pack(fill='x', padx=10, pady=(10, 5))

        separator2 = tk.Frame(alarm_frame, height=1, bg='#555555')
        separator2.pack(fill='x', padx=10)

        self.alarm_temp_label = tk.Label(alarm_frame, text="", fg='white', bg='#222222', font=('Arial', 12), wraplength=600, justify='left')
        self.alarm_temp_label.pack(fill='x', padx=10, pady=(5, 10))

    def start_timers(self):
        """타이머 시작"""
        self.update_time_only()
        self.fetch_all_async()
        self.fetch_temp_alarm_only()

    def update_time_only(self):
        """시간만 업데이트"""
        now = datetime.datetime.now()
        self.date_label.config(text=now.strftime("%Y-%m-%d (%A)"))
        self.time_label.config(text=now.strftime("%H:%M:%S"))
        self.after(1000, self.update_time_only)

    def fetch_all_async(self):
        """전체 데이터 비동기 로드"""
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
                self.after(0, self.update_info)
            except Exception as e:
                print(f"데이터 로드 오류: {e}")
        
        threading.Thread(target=run, daemon=True).start()
        self.after(60000, self.fetch_all_async)  # 60초마다 갱신

    def fetch_temp_alarm_only(self):
        """임시 알람만 비동기 로드"""
        def run():
            try:
                temp_alarm = get_temporary_alarm()
                self.alarm_cache["temp"] = temp_alarm
                self.after(0, self.update_temp_alarm_only)
            except Exception as e:
                print(f"임시 알람 로드 오류: {e}")
        
        threading.Thread(target=run, daemon=True).start()
        self.after(10000, self.fetch_temp_alarm_only)  # 10초마다 갱신

    def update_temp_alarm_only(self):
        """임시 알람만 업데이트"""
        temp_alarm = self.alarm_cache["temp"]
        if temp_alarm:
            self.alarm_temp_label.config(text=f"⏰ 임시 알람: {temp_alarm}")
        else:
            self.alarm_temp_label.config(text="⏰ 임시 알람 없음")

    def update_info(self):
        """모든 정보 업데이트"""
        # 날씨
        w = self.weather_cache
        self.weather_label.config(text=f"☁ 날씨: {w['weather']} {w['temperature']}")
        self.dust_label.config(text=f"🌫 미세먼지: {w['dust']}")

        # 메모
        regular_memo = self.memo_cache["regular"]
        if regular_memo:
            self.memo_regular_label.config(text=f"✓ 정기 메모: {regular_memo}")
        else:
            self.memo_regular_label.config(text="✓ 정기 메모: 없음")

        now = datetime.datetime.now()
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

        # 알람
        alarms = self.alarm_cache["regular"]
        if alarms:
            alarm_texts = [f"{time} ({label})" for time, label in alarms]
            self.alarm_regular_label.config(text="🔔 정기 알람: " + ", ".join(alarm_texts))
        else:
            self.alarm_regular_label.config(text="🔔 정기 알람 없음")

        temp_alarm = self.alarm_cache["temp"]
        if temp_alarm:
            self.alarm_temp_label.config(text=f"⏰ 임시 알람: {temp_alarm}")
        else:
            self.alarm_temp_label.config(text="⏰ 임시 알람 없음")

    def on_show(self):
        """화면이 표시될 때 호출"""
        pass