import tkinter as tk.QtWidgets import tk.Tk, tk.Label, # Layout placeholder (Tkinter uses pack/grid/place)
import tkinter as tk.QtCore import Qt
import requests
import datetime

API_BASE_URL = "http://127.0.0.1:5000"

def get_today_and_next_dates():
    now = datetime.datetime.now()
    today = now.date()
    next_day = today + datetime.timedelta(days=1)
    return today, next_day

class AlarmSetScreen(tk.Tk):
    def __init__(self, controller):
        super().__init__()
        self.controller = controller
        self.setStyleSheet("background-color: black; color: white;")
        self.selected_index = 0
        self.edit_mode = False

        layout = # Layout placeholder (Tkinter uses pack/grid/place)()
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(20)
        self.setLayout(layout)

        self.active_label = tk.Label("🔘 알람 활성화: OFF")
        self.active_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.active_label.setStyleSheet(self.active_box_style())
        layout.addWidget(self.active_label)

        self.empty_label = tk.Label("")
        self.empty_label.setFixedHeight(60)
        layout.addWidget(self.empty_label)

        self.hour = 7
        self.hour_label = tk.Label(f"{self.hour:02d} 시")
        self.hour_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.hour_label.setStyleSheet(self.time_box_style())
        layout.addWidget(self.hour_label)

        self.minute = 30
        self.minute_label = tk.Label(f"{self.minute:02d} 분")
        self.minute_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.minute_label.setStyleSheet(self.time_box_style())
        layout.addWidget(self.minute_label)

        self.update_highlight()

    def active_box_style(self):
        return """
            background-color: #222;
            border: 1px solid #555;
            border-radius: 10px;
            padding: 3px 15px;
            font-size: 18px;
            min-height: 25px;
        """

    def time_box_style(self):
        return """
            background-color: #222;
            border: 1px solid #555;
            border-radius: 10px;
            padding: 20px;
            font-size: 28px;
            min-height: 80px;
        """

    def update_highlight(self):
        labels = [self.active_label, self.hour_label, self.minute_label]
        for i, label in enumerate(labels):
            if i == self.selected_index:
                style = self.time_box_style() if i != 0 else self.active_box_style()
                style += "border: 2px solid #0f0;"
                label.setStyleSheet(style)
                if i == 1 and self.edit_mode:
                    label.config(text=(f"▲\n{self.hour:02d} 시\n▼")
                elif i == 2 and self.edit_mode:
                    label.config(text=(f"▲\n{self.minute:02d} 분\n▼")
                else:
                    if i == 1:
                        label.config(text=(f"{self.hour:02d} 시")
                    elif i == 2:
                        label.config(text=(f"{self.minute:02d} 분")
            else:
                if i == 1:
                    label.config(text=(f"{self.hour:02d} 시")
                elif i == 2:
                    label.config(text=(f"{self.minute:02d} 분")
                label.setStyleSheet(self.time_box_style() if i != 0 else self.active_box_style())

    def keyPressEvent(self, event):
        key = event.key()
        if key == Qt.Key.Key_Up:
            if self.edit_mode:
                if self.selected_index == 1:
                    self.hour = (self.hour + 1) % 24
                elif self.selected_index == 2:
                    self.minute = (self.minute + 1) % 60
            else:
                self.selected_index = (self.selected_index - 1) % 3
            self.update_highlight()

        elif key == Qt.Key.Key_Down:
            if self.edit_mode:
                if self.selected_index == 1:
                    self.hour = (self.hour - 1) % 24
                elif self.selected_index == 2:
                    self.minute = (self.minute - 1) % 60
            else:
                self.selected_index = (self.selected_index + 1) % 3
            self.update_highlight()

        elif key in (Qt.Key.Key_Space, Qt.Key.Key_Return):
            if self.selected_index == 0:
                self.handle_alarm_toggle()
            elif self.selected_index in [1, 2]:
                self.edit_mode = not self.edit_mode
                self.update_highlight()

    def handle_alarm_toggle(self):
        current_text = self.active_label.get()
        today, next_day = get_today_and_next_dates()
        alarm_time = f"{self.hour:02d}:{self.minute:02d}"

        if "OFF" in current_text:
            self.active_label.config(text=("🔘 알람 활성화: ON")
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
            self.active_label.config(text=("🔘 알람 활성화: OFF")
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