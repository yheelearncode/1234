import tkinter as tk
from tkinter import ttk
import requests
import datetime

API_BASE_URL = "http://127.0.0.1:5000"

def get_today_and_next_dates():
    now = datetime.datetime.now()
    today = now.date()
    next_day = today + datetime.timedelta(days=1)
    return today, next_day

class AlarmSetScreen(tk.Frame):
    def __init__(self, controller):
        super().__init__(controller, bg='black')
        self.controller = controller
        self.selected_index = 0
        self.edit_mode = False
        self.hour = 7
        self.minute = 30
        
        self.setup_ui()

    def setup_ui(self):
        """UI 구성"""
        main_frame = tk.Frame(self, bg='black')
        main_frame.pack(expand=True, fill='both', padx=20, pady=20)

        # 알람 활성화 버튼
        self.active_label = tk.Label(main_frame, text="🔘 알람 활성화: OFF", fg='white', bg='#222222', font=('Arial', 14),relief='solid', bd=1, pady=15)
        self.active_label.pack(fill='x', pady=(0, 60))

        # 시간 설정
        self.hour_label = tk.Label(main_frame, text=f"{self.hour:02d} 시", fg='white', bg='#222222', font=('Arial', 20),relief='solid', bd=1, pady=40)
        self.hour_label.pack(fill='x', pady=(0, 20))

        self.minute_label = tk.Label(main_frame, text=f"{self.minute:02d} 분", fg='white', bg='#222222', font=('Arial', 20),relief='solid', bd=1, pady=40)
        self.minute_label.pack(fill='x')

        self.update_highlight()

    def update_highlight(self):
        """하이라이트 업데이트"""
        labels = [self.active_label, self.hour_label, self.minute_label]
        
        for i, label in enumerate(labels):
            if i == self.selected_index:
                label.config(bg='#222222', fg='lime', relief='solid', bd=2)
                if i == 1 and self.edit_mode:
                    label.config(text=f"▲\n{self.hour:02d} 시\n▼")
                elif i == 2 and self.edit_mode:
                    label.config(text=f"▲\n{self.minute:02d} 분\n▼")
                else:
                    if i == 1:
                        label.config(text=f"{self.hour:02d} 시")
                    elif i == 2:
                        label.config(text=f"{self.minute:02d} 분")
            else:
                label.config(bg='#222222', fg='white', relief='solid', bd=1)
                if i == 1:
                    label.config(text=f"{self.hour:02d} 시")
                elif i == 2:
                    label.config(text=f"{self.minute:02d} 분")

    def on_key_press(self, event):
        """키 입력 처리"""
        key = event.keysym
        
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

        elif key in ('space', 'Return'):
            if self.selected_index == 0:
                self.handle_alarm_toggle()
            elif self.selected_index in [1, 2]:
                self.edit_mode = not self.edit_mode
                self.update_highlight()

    def handle_alarm_toggle(self):
        """알람 토글 처리"""
        current_text = self.active_label.cget('text')
        today, next_day = get_today_and_next_dates()
        alarm_time = f"{self.hour:02d}:{self.minute:02d}"

        if "OFF" in current_text:
            self.active_label.config(text="🔘 알람 활성화: ON")
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
            self.active_label.config(text="🔘 알람 활성화: OFF")
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
        """화면이 표시될 때 호출"""
        self.focus_set()  # 키보드 포커스 설정