from datetime import datetime

def load_today_memo():
    try:
        today = datetime.now().strftime("%Y-%m-%d")
        with open(f"memos/{today}.txt", "r", encoding="utf-8") as f:
            return f.read()
    except:
        return "오늘의 메모가 없습니다"