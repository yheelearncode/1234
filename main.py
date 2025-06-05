import tkinter as tk
import requests

from Screens.clock_screen import ClockScreen
from Screens.alarm_set_screen import AlarmSetScreen
from Screens.alarm_ring_screen import AlarmRingScreen
from Screens.memo_check_screen import MemoCheckScreen

class SmartAlarmApp(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title("Smart Alarm IoT")
        self.geometry("700x500")
        self.configure(bg="black")

        # 전체 프레임 컨테이너
        self.container = tk.Frame(self, bg="black")
        self.container.pack(fill="both", expand=True)

        # 화면 초기화
        self.clock_screen = ClockScreen(self.container, self)
        self.alarm_set_screen = AlarmSetScreen(self.container, self)
        self.memo_check_screen = MemoCheckScreen(self.container, self)
        self.alarm_ring_screen = AlarmRingScreen(self.container, self)

        self.screens = [
            self.clock_screen,
            self.alarm_set_screen,
            self.memo_check_screen
        ]
        self.current_index = 0

        for screen in self.screens + [self.alarm_ring_screen]:
            screen.grid(row=0, column=0, sticky="nsew")

        self.show_screen(self.screens[0])

        self.bind_all("<Key>", self.key_pressed)

    def show_screen(self, screen):
        screen.tkraise()

    def key_pressed(self, event):
        if event.keysym == "Left":
            self.current_index = (self.current_index - 1) % len(self.screens)
            self.show_screen(self.screens[self.current_index])
            print(f"이전 화면으로 이동: {self.current_index}")
        elif event.keysym == "Right":
            self.current_index = (self.current_index + 1) % len(self.screens)
            self.show_screen(self.screens[self.current_index])
            print(f"다음 화면으로 이동: {self.current_index}")
        elif event.keysym == "Tab":
            if self.screens[self.current_index] == self.clock_screen:
                self.show_screen(self.alarm_ring_screen)
                print("알람 울림 화면으로 이동")
            else:
                self.show_screen(self.clock_screen)
                print("시계 화면으로 이동")
        else:
            # 현재 화면에 키 이벤트 위임
            current_screen = self.screens[self.current_index]
            if hasattr(current_screen, "key_pressed"):
                current_screen.key_pressed(event)

if __name__ == "__main__":
    print(requests.get("http://127.0.0.1:5000/api/weather").json())
    app = SmartAlarmApp()
    app.mainloop()