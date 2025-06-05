import tkinter as tk
from tkinter import ttk, scrolledtext
import threading
from Services.memo_loader import get_regular_memo, get_date_memos
from Services.alarm_manager import get_regular_alarms
from datetime import datetime

class MemoCheckScreen:
    def __init__(self, parent, controller):
        self.parent = parent
        self.controller = controller
        self.root = None
        self.memo_cache = {
            "regular": "",
            "date_memos": {},
            "alarms": []
        }

    def create_frame(self, root):
        self.root = root
        frame = tk.Frame(root, bg='black')
        frame.pack(fill='both', expand=True)

        # 메인 컨테이너
        main_container = tk.Frame(frame, bg='black')
        main_container.pack(fill='both', expand=True, padx=20, pady=20)

        # 제목
        title = tk.Label(main_container, text="📝 메모 확인", 
                        bg='black', fg='white', 
                        font=('Arial', 24, 'bold'))
        title.pack(pady=(0, 15))

        # 스크롤 가능한 컨테이너
        canvas = tk.Canvas(main_container, bg='black', highlightthickness=0)
        scrollbar = ttk.Scrollbar(main_container, orient="vertical", command=canvas.yview)
        self.scrollable_frame = tk.Frame(canvas, bg='black')

        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )

        canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)

        # 스크롤바 스타일 설정
        style = ttk.Style()
        style.theme_use('clam')
        style.configure("Vertical.TScrollbar", background='#222222',troughcolor='#222222',borderwidth=0,arrowcolor='#555555',darkcolor='#555555',lightcolor='#555555')

        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        # 마우스 휠 스크롤 바인딩
        def _on_mousewheel(event):
            canvas.yview_scroll(int(-1*(event.delta/120)), "units")
        canvas.bind_all("<MouseWheel>", _on_mousewheel)

        # 정기 알람 레이블
        self.regular_alarm_label = tk.Label(main_container, text="", bg='#222222', fg='white', font=('Arial', 12),wraplength=600, justify='left',relief='solid', bd=1)
        self.regular_alarm_label.pack(fill='x', pady=(10, 0))

        # 메모 갱신 타이머 (60초)
        self.fetch_memo_async()
        self.start_memo_timer()
        
        return frame

    def create_memo_box(self, title, content):
        """메모 박스 생성"""
        box_frame = tk.Frame(self.scrollable_frame, bg='#222222', relief='solid', bd=1)
        box_frame.pack(fill='x', pady=7, padx=5)

        # 제목
        title_label = tk.Label(box_frame, text=title, bg='#222222', fg='#aaaaaa', font=('Arial', 12),wraplength=550, justify='left')
        title_label.pack(anchor='w', padx=10, pady=(5, 0))

        # 내용
        content_label = tk.Label(box_frame, text=content, 
                                bg='#222222', fg='white', 
                                font=('Arial', 14),
                                wraplength=550, justify='left')
        content_label.pack(anchor='w', padx=10, pady=(0, 10))

        return box_frame

    def fetch_memo_async(self):
        def run():
            try:
                regular_memo = get_regular_memo()
                date_memos = get_date_memos()
                alarms = get_regular_alarms()
                
                self.memo_cache["regular"] = regular_memo
                self.memo_cache["date_memos"] = date_memos
                self.memo_cache["alarms"] = alarms
                
                if self.root:
                    self.root.after(0, self.update_info)  # GUI 스레드에서 실행
            except Exception as e:
                print(f"메모 로드 오류: {e}")
        
        threading.Thread(target=run, daemon=True).start()

    def start_memo_timer(self):
        """60초마다 메모 갱신"""
        if self.root:
            self.root.after(60000, lambda: (self.fetch_memo_async(), self.start_memo_timer()))

    def update_info(self):
        """메모 정보 업데이트"""
        # 기존 위젯들 제거
        for widget in self.scrollable_frame.winfo_children():
            widget.destroy()

        # 정기 메모
        regular_memo = self.memo_cache["regular"]
        if regular_memo:
            self.create_memo_box("✓ 정기 메모", regular_memo)

        # 날짜별 메모
        date_memos = self.memo_cache["date_memos"]
        today = datetime.now().strftime('%Y-%m-%d')
        
        # 오늘 메모
        if today in date_memos:
            self.create_memo_box("🗓 오늘의 메모", date_memos[today])

        # 미래 메모
        future_memos = {date: memo for date, memo in date_memos.items() if date > today}
        if future_memos:
            for date in sorted(future_memos.keys()):
                self.create_memo_box(f"📅 {date} 메모", future_memos[date])

        # 빈 공간 추가
        spacer = tk.Frame(self.scrollable_frame, bg='black', height=50)
        spacer.pack(fill='x')

        # 정기 알람 표시
        alarms = self.memo_cache["alarms"]
        if alarms:
            alarm_texts = [f"🔔 {time} ({label})" for time, label in alarms]
            self.regular_alarm_label.config(text="\n".join(alarm_texts))
        else:
            self.regular_alarm_label.config(text="🔔 정기 알람 없음")

    def on_show(self):
        """화면이 표시될 때 호출"""
        pass