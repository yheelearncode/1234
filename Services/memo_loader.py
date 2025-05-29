from datetime import datetime
import sqlite3
import os

DB_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'instance', 'alarms.db')

def get_db_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def get_regular_memo():
    conn = get_db_connection()
    try:
        cursor = conn.cursor()
        # 날짜가 지정되지 않은 가장 최근 메모 가져오기
        query = """
        SELECT content FROM memo 
        WHERE date IS NULL 
        ORDER BY created_at DESC 
        LIMIT 1
        """
        cursor.execute(query)
        result = cursor.fetchone()
        return result['content'] if result else ""
    finally:
        conn.close()

def get_date_memo():
    conn = get_db_connection()
    try:
        cursor = conn.cursor()
        # 오늘 날짜의 메모 가져오기
        today = datetime.now().strftime('%Y-%m-%d')
        query = """
        SELECT content FROM memo 
        WHERE date = ? 
        ORDER BY created_at DESC 
        LIMIT 1
        """
        cursor.execute(query, (today,))
        result = cursor.fetchone()
        return result['content'] if result else ""
    finally:
        conn.close()

def get_date_memos():
    conn = get_db_connection()
    try:
        cursor = conn.cursor()
        # 오늘 이후의 날짜별 메모 목록 가져오기
        today = datetime.now().strftime('%Y-%m-%d')
        query = """
        SELECT date, GROUP_CONCAT(content, ' | ') as contents
        FROM memo 
        WHERE date >= ? 
        GROUP BY date
        ORDER BY date
        """
        cursor.execute(query, (today,))
        memos = cursor.fetchall()
        return {memo['date']: memo['contents'] for memo in memos}
    finally:
        conn.close()