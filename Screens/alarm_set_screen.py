import tkinter as tk
from datetime import datetime, timedelta
import requests

API_BASE_URL = "http://127.0.0.1:5000"

def get_today_and_next_dates():
    now = datetime.now()
    today = now.date()
    next_day = today + timedelta(days=1)
    return today, next_day

class AlarmSetScreen:
    def __init__(self, root, controller):
        self.root = root
        self.controller = controller
        self.selected_index = 0
        self.edit_mode = False
        self.hour = 7
        self.minute = 30
        self.is_active = False

    def create_frame(self, parent):
        self.frame = tk.Frame(parent, bg='black')
        self.frame.pack(fill='both', expand=True)
        
        # 알람 활성화 상태
        self.active_label = tk.Label(
            self.frame, 
            text="🔘 알람 활성화: OFF",
            fg="white", 
            bg="#222222",
            font=("Helvetica", 18),
            padx=15,
            pady=3
        )
        self.active_label.pack(pady=20)
        
        # 빈 공간
        tk.Label(self.frame, text="", bg="black", height=2).pack()
        
        # 시간 설정
        self.hour_label = tk.Label(
            self.frame,
            text=f"{self.hour:02d} 시",
            fg="white",
            bg="#222222",
            font=("Helvetica", 28),
            padx=20,
            pady=20
        )
        self.hour_label.pack(pady=10)
        
        # 분 설정
        self.minute_label = tk.Label(
            self.frame,
            text=f"{self.minute:02d} 분",
            fg="white",
            bg="#222222",
            font=("Helvetica", 28),
            padx=20,
            pady=20
        )
        self.minute_label.pack(pady=10)
        
        self.update_highlight()
        
        # 키 이벤트 바인딩
        self.frame.focus_set()
        self.frame.bind('<Up>', lambda e: self.handle_key('Up'))
        self.frame.bind('<Down>', lambda e: self.handle_key('Down'))
        self.frame.bind('<space>', lambda e: self.handle_key('space'))
        self.frame.bind('<Return>', lambda e: self.handle_key('Return'))
        
        return self.frame

    def update_highlight(self):
        labels = [self.active_label, self.hour_label, self.minute_label]
        for i, label in enumerate(labels):
            if i == self.selected_index:
                label.config(bg="#444444")
                if i == 1 and self.edit_mode:
                    label.config(text=f"▲\n{self.hour:02d} 시\n▼")
                elif i == 2 and self.edit_mode:
                    label.config(text=f"▲\n{self.minute:02d} 분\n▼")
            else:
                label.config(bg="#222222")
                if i == 1:
                    label.config(text=f"{self.hour:02d} 시")
                elif i == 2:
                    label.config(text=f"{self.minute:02d} 분")

    def handle_key(self, key):
        if key == 'Up':
            if self.edit_mode:
                if self.selected_index == 1:
                    self.hour = (self.hour + 1) % 24
                elif self.selected_index == 2:
                    self.minute = (self.minute + 1) % 60
            else:
                self.selected_index = (self.selected_index - 1) % 3
            self.update_highlight()
            
        elif key == 'Down':
            if self.edit_mode:
                if self.selected_index == 1:
                    self.hour = (self.hour - 1) % 24
                elif self.selected_index == 2:
                    self.minute = (self.minute - 1) % 60
            else:
                self.selected_index = (self.selected_index + 1) % 3
            self.update_highlight()
            
        elif key in ['space', 'Return']:
            if self.selected_index == 0:
                self.handle_alarm_toggle()
            elif self.selected_index in [1, 2]:
                self.edit_mode = not self.edit_mode
                self.update_highlight()

    def handle_alarm_toggle(self):
        self.is_active = not self.is_active
        current_text = "ON" if self.is_active else "OFF"
        self.active_label.config(text=f"🔘 알람 활성화: {current_text}")
        
        today, next_day = get_today_and_next_dates()
        alarm_time = f"{self.hour:02d}:{self.minute:02d}"
        
        if self.is_active:
            try:
                requests.post(
                    f"{API_BASE_URL}/api/alarms/temp",
                    json={
                        "time": alarm_time,
                        "date": today.strftime("%Y-%m-%d")
                    }
                )
            except Exception as e:
                print(f"[알람 등록 실패] {e}")
        else:
            for target_date in [today, next_day]:
                try:
                    requests.delete(
                        f"{API_BASE_URL}/api/alarms/temp",
                        json={
                            "time": alarm_time,
                            "date": target_date.strftime("%Y-%m-%d")
                        }
                    )
                except Exception as e:
                    print(f"[알람 삭제 실패: {target_date}] {e}")
        self.update_highlight()

    def on_show(self):
        self.frame.focus_set()

    def on_key_press(self, event):
        self.handle_key(event.keysym)
