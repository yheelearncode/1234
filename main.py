import sys
import tkinter as tk
from tkinter import ttk
import requests

# Tkinter로 변환된 화면들을 import
from Screens.clock_screen import ClockScreen
from Screens.alarm_set_screen import AlarmSetScreen
from Screens.alarm_ring_screen import AlarmRingScreen
from Screens.memo_check_screen import MemoCheckScreen

from Services.memo_loader import get_regular_memo
import requests

class SmartAlarmApp:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Smart Alarm IoT")
        self.root.geometry("700x500")
        self.root.configure(bg='black')
        self.root.resizable(False, False)
        
        # 현재 화면과 화면 인덱스
        self.current_frame = None
        self.current_screen_name = None
        self.current_index = 0
        
        # 화면 객체들 생성
        self.clock_screen = ClockScreen(self.root, self)
        self.alarm_set_screen = AlarmSetScreen(self.root, self)
        self.memo_check_screen = MemoCheckScreen(self.root, self)
        self.alarm_ring_screen = AlarmRingScreen(self.root, self)
        
        # 화면 리스트 (순환용)
        self.screens = [
            ('clock', self.clock_screen),
            ('alarm_set', self.alarm_set_screen),
            ('memo_check', self.memo_check_screen)
        ]
        
        # 모든 화면 딕셔너리
        self.all_screens = {
            'clock': self.clock_screen,
            'alarm_set': self.alarm_set_screen,
            'memo_check': self.memo_check_screen,
            'alarm_ring': self.alarm_ring_screen
        }
        
        # 키보드 이벤트 바인딩
        self.root.bind('<Key>', self.on_key_press)
        self.root.focus_set()
        
        # 초기 화면 설정
        self.show_screen('clock')

    def show_screen(self, screen_name):
        """화면 전환"""
        if screen_name not in self.all_screens:
            print(f"화면을 찾을 수 없습니다: {screen_name}")
            return
            
        # 현재 프레임 제거
        if self.current_frame:
            self.current_frame.destroy()
        
        # 새 화면 생성 및 표시
        screen_obj = self.all_screens[screen_name]
        self.current_frame = screen_obj.create_frame(self.root)
        self.current_screen_name = screen_name
        
        # 순환 화면의 인덱스 업데이트
        for i, (name, _) in enumerate(self.screens):
            if name == screen_name:
                self.current_index = i
                break
        
        # 화면별 초기화 작업
        if hasattr(screen_obj, 'on_show'):
            screen_obj.on_show()
        
        print(f"화면 전환: {screen_name}")

    def on_key_press(self, event):
        """키보드 이벤트 처리"""
        key = event.keysym
        
        if key == 'Left':
            # 이전 화면
            self.current_index = (self.current_index - 1) % len(self.screens)
            screen_name, _ = self.screens[self.current_index]
            self.show_screen(screen_name)
            print(f"이전 화면으로 이동: {self.current_index}")
            
        elif key == 'Right':
            # 다음 화면
            self.current_index = (self.current_index + 1) % len(self.screens)
            screen_name, _ = self.screens[self.current_index]
            self.show_screen(screen_name)
            print(f"다음 화면으로 이동: {self.current_index}")
            
        elif key == 'Tab':
            # 알람 화면 토글
            if self.current_screen_name == 'clock':
                self.show_screen('alarm_ring')
                print("알람 울림 화면으로 이동")
            else:
                self.show_screen('clock')
                print("시계 화면으로 이동")
        else:
            # 현재 화면의 키 이벤트 처리
            if self.current_screen_name in self.all_screens:
                screen_obj = self.all_screens[self.current_screen_name]
                if hasattr(screen_obj, 'on_key_press'):
                    screen_obj.on_key_press(event)

    def run(self):
        """앱 실행"""
        self.root.mainloop()

    def quit(self):
        """앱 종료"""
        self.root.quit()
        self.root.destroy()

def main():
    try:
        # API 테스트
        response = requests.get("http://127.0.0.1:5000/api/weather")
        print(response.json())
    except Exception as e:
        print(f"API 연결 오류: {e}")
    
    # 앱 실행
    app = SmartAlarmApp()
    app.run()

if __name__ == "__main__":
    main()
