from PyQt6.QtWidgets import QWidget, QLabel, QVBoxLayout
from PyQt6.QtCore import Qt
from Services.memo_loader import get_regular_memo, get_date_memos
from Services.alarm_manager import get_regular_alarms

class MemoCheckScreen(QWidget):
    def __init__(self, controller):
        super().__init__()
        self.controller = controller
        self.setStyleSheet("background-color: black; color: white;")

        layout = QVBoxLayout()
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(15)
        self.setLayout(layout)

        title = QLabel("📝 메모 확인")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title.setStyleSheet("font-size: 32px; font-weight: bold;")
        layout.addWidget(title)

        # 정기 메모 (작게)
        self.regular_memo_label = QLabel()
        self.regular_memo_label.setAlignment(Qt.AlignmentFlag.AlignLeft)
        self.regular_memo_label.setStyleSheet("""
            font-size: 16px;
            color: white;
            padding: 5px;
            max-height: 60px;
        """)
        layout.addWidget(self.regular_memo_label)

        # 날짜 메모 (크게)
        self.date_memo_label = QLabel()
        self.date_memo_label.setAlignment(Qt.AlignmentFlag.AlignLeft)
        self.date_memo_label.setStyleSheet("""
            font-size: 16px;
            color: white;
            padding: 10px;
        """)
        layout.addWidget(self.date_memo_label)

        # 정기 알람 (크게)
        self.regular_alarm_label = QLabel()
        self.regular_alarm_label.setAlignment(Qt.AlignmentFlag.AlignLeft)
        self.regular_alarm_label.setStyleSheet("""
            font-size: 16px;
            color: white;
            padding: 10px;
        """)
        layout.addWidget(self.regular_alarm_label)

        self.update_info()

    def update_info(self):
        # 정기 알람 표시 (리스트)
        alarms = get_regular_alarms()
        if alarms:
            alarm_texts = [f"🔔 {time} ({label})" for time, label in alarms]
            self.regular_alarm_label.setText("\n".join(alarm_texts))
        else:
            self.regular_alarm_label.setText("🔔 정기 알람 없음")

        # 정기 메모 표시 (단일 값)
        self.regular_memo_label.setText(f"✓ 정기 메모: {get_regular_memo()}")

        # 날짜 메모 표시 (전체)
        date_memos = get_date_memos()
        if date_memos:
            memo_texts = [f"🗓 {date}: {memo}" for date, memo in date_memos.items()]
            self.date_memo_label.setText("\n".join(memo_texts))
        else:
            self.date_memo_label.setText("🗓 날짜 메모 없음")