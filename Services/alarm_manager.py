from datetime import datetime
import sqlite3
import os

DB_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'instance', 'alarms.db')

def get_db_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def get_regular_alarms():
    conn = get_db_connection()
    try:
        cursor = conn.cursor()
        # 오늘 요일에 해당하는 알람만 가져오기 (특정 날짜가 없는 알람)
        today = datetime.now()
        weekday = str(today.weekday())
        
        query = """
        SELECT time, label FROM alarm 
        WHERE days LIKE ? 
        AND specific_date IS NULL
        AND is_active = 1
        ORDER BY time
        """
        cursor.execute(query, (f'%{weekday}%',))
        alarms = cursor.fetchall()
        return [(alarm['time'], alarm['label']) for alarm in alarms]
    finally:
        conn.close()

def get_temporary_alarm():
    conn = get_db_connection()
    try:
        cursor = conn.cursor()
        # 오늘 이후의 가장 가까운 특정 날짜 알람 가져오기
        today = datetime.now().strftime('%Y-%m-%d')
        query = """
        SELECT time, specific_date, label FROM alarm 
        WHERE specific_date >= ? 
        AND is_active = 1 
        ORDER BY specific_date, time 
        LIMIT 1
        """
        cursor.execute(query, (today,))
        result = cursor.fetchone()
        if result:
            return f"{result['time']} ({result['label']} - {result['specific_date']})"
        return None
    finally:
        conn.close()