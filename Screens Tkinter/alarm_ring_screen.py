import tkinter as tk
from tkinter import ttk
import datetime
import os
import threading
import time
import pygame
import cv2
import mediapipe as mp

from Services.memo_loader import get_regular_memo, get_date_memo

def monitor_stretch_motion():
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

class AlarmRingScreen:
    def __init__(self, parent, controller):
        self.parent = parent
        self.controller = controller
        self.root = None
        self.sound_channel = None
        self.memo_cache = {"regular": "", "date": ""}
        
        # pygame 초기화 (사운드용)
        try:
            pygame.mixer.init()
        except pygame.error as e:
            print(f"pygame 초기화 실패: {e}")

    def create_frame(self, root):
        self.root = root
        frame = tk.Frame(root, bg='black')
        frame.pack(fill='both', expand=True)

        # 메인 컨테이너
        main_container = tk.Frame(frame, bg='black')
        main_container.pack(fill='both', expand=True, padx=20, pady=20)

        # 알람 아이콘
        self.icon_label = tk.Label(main_container, text="🔔", bg='black', fg='white', font=('Arial', 120))
        self.icon_label.pack(pady=(0, 30))

        # 시간 표시
        self.time_label = tk.Label(main_container, text="", bg='black', fg='white', font=('Arial', 40, 'bold'))
        self.time_label.pack(pady=(0, 30))

        # 메모 박스
        memo_frame = tk.Frame(main_container, bg='#222222', relief='solid', bd=1)
        memo_frame.pack(fill='x', pady=(0, 20))

        # 정기 메모
        self.memo_regular_label = tk.Label(memo_frame, text="", bg='#222222', fg='white', font=('Arial', 12),wraplength=600, justify='left')
        self.memo_regular_label.pack(anchor='w', padx=10, pady=5)

        # 구분선
        separator = tk.Frame(memo_frame, height=1, bg='#555555')
        separator.pack(fill='x', padx=10, pady=5)

        # 날짜 메모
        self.date_memo_label = tk.Label(memo_frame, text="", bg='#222222', fg='white', font=('Arial', 12), wraplength=600, justify='left')
        self.date_memo_label.pack(anchor='w', padx=10, pady=5)

        # 키보드 포커스 설정
        frame.bind('<Key>', self.on_key_press)
        frame.focus_set()

        self.update_time()
        self.fetch_memo_async()
        
        return frame

    def setup_sound(self):
        try:
            sound_path = os.path.join("Assets", "alarm.wav")
            if os.path.exists(sound_path):
                self.alarm_sound = pygame.mixer.Sound(sound_path)
                return True
            else:
                print(f"알람 파일을 찾을 수 없습니다: {sound_path}")
                return False
        except Exception as e:
            print(f"알람음 설정 오류: {e}")
            return False

    def start_alarm(self):
        print("알람 시작!")
        if self.setup_sound():
            try:
                # 무한 반복으로 재생
                self.sound_channel = pygame.mixer.Channel(0)
                self.sound_channel.play(self.alarm_sound, loops=-1)
                self.sound_channel.set_volume(0.5)
            except Exception as e:
                print(f"알람음 재생 오류: {e}")
        else:
            print("알람음 파일이 설정되지 않았습니다.")

        # 모션 인식 스레드 시작
        threading.Thread(target=self.monitor_stretch_motion_thread, daemon=True).start()

    def monitor_stretch_motion_thread(self):
        if monitor_stretch_motion():
            self.root.after(0, self.stop_alarm)  # GUI 스레드에서 실행

    def update_time(self):
        if self.root:
            now = datetime.datetime.now()
            self.time_label.config(text=now.strftime("%H:%M:%S"))
            self.root.after(1000, self.update_time)

    def fetch_memo_async(self):
        def run():
            try:
                regular = get_regular_memo()
                date = get_date_memo()
                self.memo_cache["regular"] = regular or "없음"
                self.memo_cache["date"] = date or "없음"
                if self.root:
                    self.root.after(0, self.update_memo)  # GUI 스레드에서 실행
            except Exception as e:
                print(f"메모 로드 오류: {e}")
                self.memo_cache["regular"] = "로드 실패"
                self.memo_cache["date"] = "로드 실패"
                if self.root:
                    self.root.after(0, self.update_memo)
        
        threading.Thread(target=run, daemon=True).start()
        
        # 30초마다 메모 갱신
        if self.root:
            self.root.after(30000, self.fetch_memo_async)

    def update_memo(self):
        if hasattr(self, 'memo_regular_label'):
            self.memo_regular_label.config(text=f"✓ 정기 메모: {self.memo_cache['regular']}")
        if hasattr(self, 'date_memo_label'):
            self.date_memo_label.config(text=f"🗓 날짜 메모: {self.memo_cache['date']}")

    def stop_alarm(self):
        print("알람 정지!")
        try:
            if self.sound_channel:
                self.sound_channel.stop()
                self.sound_channel = None
        except Exception as e:
            print(f"알람 정지 오류: {e}")
        
        self.controller.show_screen('clock')
        print("시계 화면으로 전환")

    def on_show(self):
        """화면이 표시될 때 호출"""
        self.start_alarm()

    def on_key_press(self, event):
        key = event.keysym
        if key in ('space', 'Return', 'Escape'):
            self.stop_alarm()