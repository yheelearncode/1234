import tkinter as tk.QtWidgets import tk.Tk, tk.Label, # Layout placeholder (Tkinter uses pack/grid/place)
import tkinter as tk.QtCore import Qt, QTimer, QUrl, pyqtSignal
import tkinter as tk.QtMultimedia import QSoundEffect
import datetime
import os
import threading

from Services.memo_loader import get_regular_memo, get_date_memo

def monitor_stretch_motion():
    import cv2
    import mediapipe as mp
    import time

    mp_pose = mp.solutions.pose
    cap = cv2.VideoCapture(0)

    detected_start_time = None
    stretch_confirmed = False
    min_duration = 0.5

    with mp_pose.Pose(min_detection_confidence=0.5) as pose:
        while True:
            ret, frame = cap.read()
            if not ret:
                break

            results = pose.process(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))

            if results.pose_landmarks:
                landmarks = results.pose_landmarks.landmark
                lw = landmarks[mp_pose.PoseLandmark.LEFT_WRIST]
                rw = landmarks[mp_pose.PoseLandmark.RIGHT_WRIST]
                nose = landmarks[mp_pose.PoseLandmark.NOSE]

                stretch_condition = lw.y < nose.y and rw.y < nose.y

                if stretch_condition:
                    if detected_start_time is None:
                        detected_start_time = time.time()
                    elif time.time() - detected_start_time >= min_duration:
                        stretch_confirmed = True
                else:
                    detected_start_time = None

                if stretch_confirmed:
                    print("Stretch Detected!")
                    cap.release()
                    return True

    cap.release()
    return False

class AlarmRingScreen(tk.Tk):
    memo_updated = pyqtSignal()

    def __init__(self, controller):
        super().__init__()
        self.controller = controller
        self.setStyleSheet("background-color: black; color: white;")
        layout = # Layout placeholder (Tkinter uses pack/grid/place)()
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(30)
        self.setLayout(layout)

        self.icon_label = tk.Label("🔔")
        self.icon_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.icon_label.setStyleSheet("font-size: 200px;")
        layout.addWidget(self.icon_label)

        self.time_label = tk.Label("")
        self.time_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.time_label.setStyleSheet("font-size: 60px;")
        layout.addWidget(self.time_label)

        self.memo_box = tk.Tk()
        self.memo_box.setStyleSheet("""
            background-color: #222;
            border: 1px solid #555;
            border-radius: 10px;
            padding: 10px;
        """)
        memo_layout = # Layout placeholder (Tkinter uses pack/grid/place)()
        memo_layout.setSpacing(5)
        self.memo_box.setLayout(memo_layout)

        self.memo_regular_label = tk.Label("")
        self.memo_regular_label.setStyleSheet("font-size: 18px; color: white;")
        memo_layout.addWidget(self.memo_regular_label)

        self.date_memo_label = tk.Label("")
        self.date_memo_label.setStyleSheet("font-size: 18px; color: white; border-top: 1px solid #555; padding-top: 5px;")
        memo_layout.addWidget(self.date_memo_label)

        layout.addWidget(self.memo_box)

        self.memo_cache = {"regular": "", "date": ""}

        self.timer = QTimer()
        self.timer.timeout.connect(self.update_time)
        self.timer.start(1000)
        self.update_time()

        self.memo_timer = QTimer()
        self.memo_timer.timeout.connect(self.fetch_memo_async)
        self.memo_timer.start(30000)
        self.memo_updated.connect(self.update_memo)
        self.fetch_memo_async()

        self.sound = None
        self.setup_sound()

    def setup_sound(self):
        try:
            sound_path = os.path.join("Assets", "alarm.wav")
            if os.path.exists(sound_path):
                self.sound = QSoundEffect()
                self.sound.setSource(QUrl.fromLocalFile(os.path.abspath(sound_path)))
                self.sound.setLoopCount(999999)
                self.sound.setVolume(0.5)
            else:
                print(f"알람 파일을 찾을 수 없습니다: {sound_path}")
        except Exception as e:
            print(f"알람음 설정 오류: {e}")

    def start_alarm(self):
        print("알람 시작!")
        if self.sound:
            self.sound.play()
        else:
            print("알람음 파일이 설정되지 않았습니다.")

        # ▶ 모션 인식 스레드 시작
        threading.Thread(target=self.monitor_stretch_motion_thread, daemon=True).start()

    def monitor_stretch_motion_thread(self):
        if monitor_stretch_motion():
            self.stop_alarm()

    def update_time(self):
        now = datetime.datetime.now()
        self.time_label.config(text=(now.strftime("%H:%M:%S"))

    def fetch_memo_async(self):
        def run():
            try:
                regular = get_regular_memo()
                date = get_date_memo()
                self.memo_cache["regular"] = regular or "없음"
                self.memo_cache["date"] = date or "없음"
                self.memo_updated.emit()
            except Exception as e:
                print(f"메모 로드 오류: {e}")
                self.memo_cache["regular"] = "로드 실패"
                self.memo_cache["date"] = "로드 실패"
                self.memo_updated.emit()
        threading.Thread(target=run, daemon=True).start()

    def update_memo(self):
        self.memo_regular_label.config(text=(f"✓ 정기 메모: {self.memo_cache['regular']}")
        self.date_memo_label.config(text=(f"🗓 날짜 메모: {self.memo_cache['date']}")

    def stop_alarm(self):
        print("알람 정지!")
        if self.sound:
            self.sound.stop()
        self.setup_sound()
        self.controller.setCurrentWidget(self.controller.clock_screen)
        print("시계 화면으로 전환")

    def showEvent(self, event):
        super().showEvent(event)
        self.start_alarm()

    def keyPressEvent(self, event):
        key = event.key()
        if key in (Qt.Key.Key_Space, Qt.Key.Key_Return, Qt.Key.Key_Escape):
            self.stop_alarm()
        else:
            super().keyPressEvent(event)