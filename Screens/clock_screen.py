from PyQt6.QtWidgets import QWidget, QLabel, QVBoxLayout, QHBoxLayout
from PyQt6.QtCore import QTimer, Qt
import datetime
from Services.memo_loader import get_regular_memo, get_date_memo, get_date_memos
from Services.weather_api import get_weather
from Services.alarm_manager import get_regular_alarms, get_temporary_alarm

class ClockScreen(QWidget):
    def __init__(self, controller):
        super().__init__()
        self.controller = controller
        self.setStyleSheet("background-color: black; color: white;")
        self.layout = QVBoxLayout()
        self.layout.setContentsMargins(20, 20, 20, 20)
        self.layout.setSpacing(15)
        self.setLayout(self.layout)

        # 날짜/시간
        self.date_label = QLabel("")
        self.date_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.date_label.setStyleSheet("font-size: 22px; color: white;")
        self.layout.addWidget(self.date_label)

        self.time_label = QLabel("")
        self.time_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.time_label.setStyleSheet("font-size: 100px; color: white; font-weight: bold;")
        self.layout.addWidget(self.time_label)

        # 날씨/미세먼지
        weather_dust_layout = QHBoxLayout()
        self.weather_label = QLabel("")
        self.weather_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.weather_label.setStyleSheet("font-size: 18px; color: white;")
        weather_dust_layout.addWidget(self.weather_label)

        self.dust_label = QLabel("")
        self.dust_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.dust_label.setStyleSheet("font-size: 18px; color: white;")
        weather_dust_layout.addWidget(self.dust_label)

        self.layout.addLayout(weather_dust_layout)

        # 메모 박스
        self.memo_box = QWidget()
        self.memo_box.setStyleSheet("""
            background-color: #222;
            border: 1px solid #555;
            border-radius: 10px;
            padding: 10px;
        """)
        memo_layout = QVBoxLayout()
        memo_layout.setSpacing(5)
        self.memo_box.setLayout(memo_layout)

        self.memo_regular_label = QLabel("")
        self.memo_regular_label.setStyleSheet("font-size: 18px; color: white;")
        self.memo_regular_label.setWordWrap(True)
        memo_layout.addWidget(self.memo_regular_label)

        self.date_memo_label = QLabel("")
        self.date_memo_label.setStyleSheet("font-size: 18px; color: white; border-top: 1px solid #555; padding-top: 5px;")
        self.date_memo_label.setWordWrap(True)
        memo_layout.addWidget(self.date_memo_label)

        self.layout.addWidget(self.memo_box)

        # 알람 박스
        self.alarm_box = QWidget()
        self.alarm_box.setStyleSheet("""
            background-color: #222;
            border: 1px solid #555;
            border-radius: 10px;
            padding: 10px;
        """)
        alarm_layout = QVBoxLayout()
        alarm_layout.setSpacing(5)
        self.alarm_box.setLayout(alarm_layout)

        self.alarm_regular_label = QLabel("")
        self.alarm_regular_label.setStyleSheet("font-size: 18px; color: white;")
        self.alarm_regular_label.setWordWrap(True)
        alarm_layout.addWidget(self.alarm_regular_label)

        self.alarm_temp_label = QLabel("")
        self.alarm_temp_label.setStyleSheet("font-size: 18px; color: white; border-top: 1px solid #555; padding-top: 5px;")
        self.alarm_temp_label.setWordWrap(True)
        alarm_layout.addWidget(self.alarm_temp_label)

        self.layout.addWidget(self.alarm_box)

        # 타이머
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_info)
        self.timer.start(1000)
        self.update_info()

    def update_info(self):
        now = datetime.datetime.now()
        self.date_label.setText(now.strftime("%Y-%m-%d (%A)"))
        self.time_label.setText(now.strftime("%H:%M:%S"))

        # 날씨
        weather = get_weather()
        self.weather_label.setText(f"☁ 날씨: {weather['weather']} {weather['temperature']}")
        self.dust_label.setText(f"🌫 미세먼지: {weather['dust']}")

        # 정기 메모
        regular_memo = get_regular_memo()
        if regular_memo:
            self.memo_regular_label.setText(f"✓ 정기 메모: {regular_memo}")
        else:
            self.memo_regular_label.setText("✓ 정기 메모: 없음")

        # 날짜 메모
        today = now.strftime("%Y-%m-%d")
        date_memos = get_date_memos()
        if today in date_memos:
            self.date_memo_label.setText(f"🗓 오늘의 메모: {date_memos[today]}")
        else:
            next_memo = None
            next_date = None
            for date in sorted(date_memos.keys()):
                if date > today:
                    next_memo = date_memos[date]
                    next_date = date
                    break
            if next_memo:
                self.date_memo_label.setText(f"🗓 다음 메모 ({next_date}): {next_memo}")
            else:
                self.date_memo_label.setText("🗓 예정된 메모 없음")

        # 정기 알람
        alarms = get_regular_alarms()
        if alarms:
            alarm_texts = [f"{time} ({label})" for time, label in alarms]
            self.alarm_regular_label.setText("🔔 정기 알람: " + ", ".join(alarm_texts))
        else:
            self.alarm_regular_label.setText("🔔 정기 알람 없음")

        # 임시 알람
        temp_alarm = get_temporary_alarm()
        if temp_alarm:
            self.alarm_temp_label.setText(f"⏰ 임시 알람: {temp_alarm}")
        else:
            self.alarm_temp_label.setText("⏰ 임시 알람 없음")