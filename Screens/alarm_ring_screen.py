from PyQt6.QtWidgets import QWidget, QLabel, QVBoxLayout
from PyQt6.QtCore import Qt, QTimer, QUrl, pyqtSignal
from PyQt6.QtMultimedia import QSoundEffect
import datetime
import os
import threading

from Services.memo_loader import get_regular_memo, get_date_memo

class AlarmRingScreen(QWidget):
    # 메모 갱신 시그널(메인스레드에서 setText 보장)
    memo_updated = pyqtSignal()

    def __init__(self, controller):
        super().__init__()
        self.controller = controller
        self.setStyleSheet("background-color: black; color: white;")

        layout = QVBoxLayout()
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(30)
        self.setLayout(layout)

        # 🔔 아이콘
        self.icon_label = QLabel("🔔")
        self.icon_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.icon_label.setStyleSheet("font-size: 200px;")
        layout.addWidget(self.icon_label)

        # 현재 시간
        self.time_label = QLabel("")
        self.time_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.time_label.setStyleSheet("font-size: 60px;")
        layout.addWidget(self.time_label)

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
        memo_layout.addWidget(self.memo_regular_label)

        self.date_memo_label = QLabel("")
        self.date_memo_label.setStyleSheet("font-size: 18px; color: white; border-top: 1px solid #555; padding-top: 5px;")
        memo_layout.addWidget(self.date_memo_label)

        layout.addWidget(self.memo_box)

        # 캐시
        self.memo_cache = {"regular": "", "date": ""}

        # 시계 타이머 (1초)
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_time)
        self.timer.start(1000)
        self.update_time()

        # 메모 타이머 (30초)
        self.memo_timer = QTimer()
        self.memo_timer.timeout.connect(self.fetch_memo_async)
        self.memo_timer.start(30000)
        self.memo_updated.connect(self.update_memo)
        self.fetch_memo_async()  # 최초 1회

        # 알람음 재생
        self.sound = QSoundEffect()
        sound_path = os.path.join("Assets", "alarm.mp3")
        self.sound.setSource(QUrl.fromLocalFile(os.path.abspath(sound_path)))
        self.sound.setLoopCount(999999)  # 사실상 무한 반복
        self.sound.setVolume(0.5)
        self.sound.play()

    def update_time(self):
        now = datetime.datetime.now()
        self.time_label.setText(now.strftime("%H:%M:%S"))

    def fetch_memo_async(self):
        # 별도 쓰레드에서 서비스 함수 실행
        def run():
            regular = get_regular_memo()
            date = get_date_memo()
            self.memo_cache["regular"] = regular
            self.memo_cache["date"] = date
            self.memo_updated.emit()
        threading.Thread(target=run).start()

    def update_memo(self):
        self.memo_regular_label.setText(f"✓ 정기 메모: {self.memo_cache['regular']}")
        self.date_memo_label.setText(f"🗓 날짜 메모: {self.memo_cache['date']}")

    def stop_alarm(self):
        self.sound.stop()
        self.controller.setCurrentWidget(self.controller.clock_screen)
        print("알람 종료, 시계 화면으로 전환")

    def keyPressEvent(self, event):
        key = event.key()
        if key in (Qt.Key.Key_Space, Qt.Key.Key_Return):
            self.stop_alarm()