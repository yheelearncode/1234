from PyQt6.QtWidgets import QWidget, QLabel, QVBoxLayout, QScrollArea, QSizePolicy
from PyQt6.QtCore import Qt, QTimer, pyqtSignal
import threading
from Services.memo_loader import get_regular_memo, get_date_memos
from Services.alarm_manager import get_regular_alarms
from datetime import datetime

class MemoCheckScreen(QWidget):
    memo_updated = pyqtSignal()

    def __init__(self, controller):
        super().__init__()
        self.controller = controller
        self.setStyleSheet("background-color: black; color: white;")

        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(20, 20, 20, 20)
        main_layout.setSpacing(15)
        self.setLayout(main_layout)

        title = QLabel("📝 메모 확인")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title.setStyleSheet("font-size: 32px; font-weight: bold;")
        main_layout.addWidget(title)

        # 스크롤 영역 생성
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setStyleSheet("""
            QScrollArea {
                border: none;
                background-color: black;
            }
            QScrollBar:vertical {
                border: none;
                background: #222;
                width: 10px;
                margin: 0px;
            }
            QScrollBar::handle:vertical {
                background: #555;
                min-height: 20px;
                border-radius: 5px;
            }
            QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {
                border: none;
                background: none;
            }
        """)
        
        content_widget = QWidget()
        self.content_layout = QVBoxLayout(content_widget)
        self.content_layout.setSpacing(15)
        scroll.setWidget(content_widget)
        main_layout.addWidget(scroll)

        # 알람 레이블 추가
        self.regular_alarm_label = QLabel()
        self.regular_alarm_label.setStyleSheet("""
            font-size: 18px;
            color: white;
            background-color: #222;
            border: 1px solid #555;
            border-radius: 10px;
            padding: 10px;
        """)
        self.regular_alarm_label.setWordWrap(True)
        main_layout.addWidget(self.regular_alarm_label)

        # 캐시
        self.memo_cache = {
            "regular": "",
            "date_memos": {},
            "alarms": []
        }

        # 메모 갱신 타이머 (60초)
        self.memo_timer = QTimer()
        self.memo_timer.timeout.connect(self.fetch_memo_async)
        self.memo_timer.start(60000)
        self.memo_updated.connect(self.update_info)
        self.fetch_memo_async()  # 최초 1회

    def create_memo_box(self, title, content):
        box = QWidget()
        box.setStyleSheet("""
            background-color: #222;
            border: 1px solid #555;
            border-radius: 10px;
            padding: 10px;
        """)
        layout = QVBoxLayout()
        layout.setSpacing(5)
        box.setLayout(layout)

        title_label = QLabel(title)
        title_label.setStyleSheet("font-size: 18px; color: #aaa;")
        title_label.setWordWrap(True)
        layout.addWidget(title_label)

        content_label = QLabel(content)
        content_label.setStyleSheet("font-size: 20px; color: white;")
        content_label.setWordWrap(True)
        layout.addWidget(content_label)

        return box

    def fetch_memo_async(self):
        def run():
            regular_memo = get_regular_memo()
            date_memos = get_date_memos()
            alarms = get_regular_alarms()
            self.memo_cache["regular"] = regular_memo
            self.memo_cache["date_memos"] = date_memos
            self.memo_cache["alarms"] = alarms
            self.memo_updated.emit()
        threading.Thread(target=run).start()

    def update_info(self):
        # 기존 위젯들 제거
        for i in reversed(range(self.content_layout.count())): 
            widget = self.content_layout.itemAt(i).widget()
            if widget is not None:
                widget.setParent(None)

        # 정기 메모
        regular_memo = self.memo_cache["regular"]
        if regular_memo:
            self.content_layout.addWidget(
                self.create_memo_box("✓ 정기 메모", regular_memo)
            )

        # 날짜별 메모
        date_memos = self.memo_cache["date_memos"]
        today = datetime.now().strftime('%Y-%m-%d')
        
        # 오늘 메모
        if today in date_memos:
            self.content_layout.addWidget(
                self.create_memo_box("🗓 오늘의 메모", date_memos[today])
            )

        # 미래 메모
        future_memos = {date: memo for date, memo in date_memos.items() if date > today}
        if future_memos:
            for date in sorted(future_memos.keys()):
                self.content_layout.addWidget(
                    self.create_memo_box(f"📅 {date} 메모", future_memos[date])
                )

        # 빈 공간 추가
        spacer = QWidget()
        spacer.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        self.content_layout.addWidget(spacer)

        # 정기 알람 표시
        alarms = self.memo_cache["alarms"]
        if alarms:
            alarm_texts = [f"🔔 {time} ({label})" for time, label in alarms]
            self.regular_alarm_label.setText("\n".join(alarm_texts))
        else:
            self.regular_alarm_label.setText("🔔 정기 알람 없음")