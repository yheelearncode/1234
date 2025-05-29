from PyQt6.QtWidgets import QWidget, QLabel, QVBoxLayout
from PyQt6.QtCore import Qt

class AlarmSetScreen(QWidget):
    def __init__(self, controller):
        super().__init__()
        self.controller = controller
        self.setStyleSheet("background-color: black; color: white;")

        self.selected_index = 0
        self.edit_mode = False

        layout = QVBoxLayout()
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(20)
        self.setLayout(layout)

        # 알람 활성화 박스 (얇게)
        self.active_label = QLabel("🔘 알람 활성화: OFF")
        self.active_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.active_label.setStyleSheet(self.active_box_style())
        layout.addWidget(self.active_label)

        # 공백 추가 (얇게 보이도록)
        self.empty_label = QLabel("")
        self.empty_label.setFixedHeight(60)  # 공백 충분히 확보
        layout.addWidget(self.empty_label)

        # 시
        self.hour = 7
        self.hour_label = QLabel(f"{self.hour:02d} 시")
        self.hour_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.hour_label.setStyleSheet(self.time_box_style())
        layout.addWidget(self.hour_label)

        # 분
        self.minute = 30
        self.minute_label = QLabel(f"{self.minute:02d} 분")
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
                style += "border: 2px solid #0f0;"  # 선택 강조
                label.setStyleSheet(style)

                if i == 1 and self.edit_mode:
                    label.setText(f"▲\n{self.hour:02d} 시\n▼")
                elif i == 2 and self.edit_mode:
                    label.setText(f"▲\n{self.minute:02d} 분\n▼")
                else:
                    if i == 1:
                        label.setText(f"{self.hour:02d} 시")
                    elif i == 2:
                        label.setText(f"{self.minute:02d} 분")
            else:
                if i == 1:
                    label.setText(f"{self.hour:02d} 시")
                elif i == 2:
                    label.setText(f"{self.minute:02d} 분")
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
                current_text = self.active_label.text()
                if "OFF" in current_text:
                    self.active_label.setText("🔘 알람 활성화: ON")
                else:
                    self.active_label.setText("🔘 알람 활성화: OFF")
            elif self.selected_index in [1, 2]:
                self.edit_mode = not self.edit_mode
            self.update_highlight()