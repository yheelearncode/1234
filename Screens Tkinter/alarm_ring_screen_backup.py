import tkinter as tk
from tkinter import ttk
import datetime
import os
import threading
import pygame
from Services.memo_loader import get_regular_memo, get_date_memo

class AlarmRingScreen(tk.Frame):
    def __init__(self, controller):
        super().__init__(controller, bg='black')
        self.controller = controller
        self.memo_cache = {"regular": "", "date": ""}
        self.sound = None
        
        self.setup_ui()
        self.setup_sound()
        self.start_timers()

    def setup_ui(self):
        # 메인 프레임
        main_frame = tk.Frame(self, bg='black')
        main_frame.pack(expand=True, fill='both', padx=20, pady=20)

        # 🔔 아이콘
        self.icon_label = tk.Label(main_frame, text="🔔", fg='white', bg='black', font=('Arial', 150))
        self.icon_label.pack(pady=(0, 30))

        # 현재 시간
        self.time_label = tk.Label(main_frame, text="", fg='white', bg='black', font=('Arial', 40, 'bold'))
        self.time_label.pack(pady=(0, 30))

        # 메모 박스
        memo_frame = tk.Frame(main_frame, bg='#222222', relief='solid', bd=1)
        memo_frame.pack(fill='x', pady=(0, 10))

        # 정기 메모
        self.memo_regular_label = tk.Label(memo_frame, text="", fg='white', bg='#222222', font=('Arial', 12), wraplength=600, justify='left')
        self.memo_regular_label.pack(fill='x', padx=10, pady=(10, 5))

        # 날짜 메모
        separator = tk.Frame(memo_frame, height=1, bg='#555555')
        separator.pack(fill='x', padx=10)
        
        self.date_memo_label = tk.Label(memo_frame, text="", fg='white', bg='#222222', 
                                        font=('Arial', 12), wraplength=600, justify='left')
        self.date_memo_label.pack(fill='x', padx=10, pady=(5, 10))

    def setup_sound(self):
        """알람음 설정"""
        try:
            pygame.mixer.init()
            sound_path = os.path.join("Assets", "alarm.wav")
            if os.path.exists(sound_path):
                self.sound = pygame.mixer.Sound(sound_path)
            else:
                print(f"알람 파일을 찾을 수 없습니다: {sound_path}")
        except Exception as e:
            print(f"알람음 설정 오류: {e}")

    def start_timers(self):
        """타이머 시작"""
        self.update_time()
        self.fetch_memo_async()

    def start_alarm(self):
        """알람 시작"""
        print("알람 시작!")
        if self.sound:
            try:
                self.sound.play(loops=-1)  # 무한 반복
            except Exception as e:
                print(f"알람 재생 오류: {e}")
        else:
            print("알람음 파일이 설정되지 않았습니다.")

    def update_time(self):
        """시간 업데이트"""
        now = datetime.datetime.now()
        self.time_label.config(text=now.strftime("%H:%M:%S"))
        self.after(1000, self.update_time)

    def fetch_memo_async(self):
        """메모 비동기 로드"""
        def run():
            try:
                regular = get_regular_memo()
                date = get_date_memo()
                self.memo_cache["regular"] = regular or "없음"
                self.memo_cache["date"] = date or "없음"
                self.after(0, self.update_memo)
            except Exception as e:
                print(f"메모 로드 오류: {e}")
                self.memo_cache["regular"] = "로드 실패"
                self.memo_cache["date"] = "로드 실패"
                self.after(0, self.update_memo)
        
        threading.Thread(target=run, daemon=True).start()
        self.after(30000, self.fetch_memo_async)  # 30초마다 갱신

    def update_memo(self):
        """메모 업데이트"""
        self.memo_regular_label.config(text=f"✓ 정기 메모: {self.memo_cache['regular']}")
        self.date_memo_label.config(text=f"🗓 날짜 메모: {self.memo_cache['date']}")

    def stop_alarm(self):
        """알람 정지"""
        print("알람 정지!")
        if self.sound:
            try:
                pygame.mixer.stop()
            except Exception as e:
                print(f"알람 정지 오류: {e}")
        
        # 시계 화면으로 전환
        self.controller.show_clock_screen()
        print("시계 화면으로 전환")

    def on_show(self):
        """화면이 표시될 때 호출"""
        self.start_alarm()
        self.focus_set()  # 키보드 포커스 설정

    def on_key_press(self, event):
        """키 입력 처리"""
        if event.keysym in ('space', 'Return', 'Escape'):
            self.stop_alarm()