import sqlite3
import os

DB_PATH = os.path.join('instance', 'alarms.db')

def check_database():
    if not os.path.exists(DB_PATH):
        print(f"데이터베이스 파일이 없습니다: {DB_PATH}")
        return

    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    print("\n=== 알람 테이블 내용 ===")
    cursor.execute("SELECT * FROM alarm")
    alarms = cursor.fetchall()
    if not alarms:
        print("알람이 없습니다.")
    for alarm in alarms:
        print(f"ID: {alarm['id']}")
        print(f"시간: {alarm['time']}")
        print(f"레이블: {alarm['label']}")
        print(f"요일: {alarm['days']}")
        print(f"특정 날짜: {alarm['specific_date']}")
        print(f"활성화: {alarm['is_active']}")
        print(f"생성일: {alarm['created_at']}")
        print("-" * 30)

    print("\n=== 메모 테이블 내용 ===")
    cursor.execute("SELECT * FROM memo")
    memos = cursor.fetchall()
    if not memos:
        print("메모가 없습니다.")
    for memo in memos:
        print(f"ID: {memo['id']}")
        print(f"내용: {memo['content']}")
        print(f"날짜: {memo['date']}")
        print(f"생성일: {memo['created_at']}")
        print("-" * 30)

    conn.close()

if __name__ == "__main__":
    check_database() 