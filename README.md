# 📡 Smart Alarm IoT 시스템

기지개 동작으로 알람을 해제하고, LCD 화면에 오늘의 메모와 준비물을 보여주는 스마트 알람 시스템입니다.  
사용자의 기상 습관을 개선하고 아침 준비를 돕는 **모션 인식 기반 IoT 시스템**을 구현합니다.

---

## 🧠 프로젝트 개요

### 🎯 목적

- 알람을 끄고 다시 자는 **재취침 문제**를 해결하고
- 아침에 챙겨야 할 물품, 일정, 날씨 정보를 **즉시 확인**할 수 있도록 지원합니다.

### 💡 주요 기능

| 기능         | 설명                                                      |
| ------------ | --------------------------------------------------------- |
| 🔔 알람 해제 | 사용자가 **기지개 동작**을 하면 알람이 해제됨             |
| 📝 메모 표시 | 전날 등록한 메모/준비물 목록을 LCD로 표시                 |
| ☁️ 날씨 표시 | API를 통해 오늘 날씨/미세먼지 정보 표시                   |
| 📡 서버 연동 | 사용자 웹을 통해 메모를 등록하고, 라즈베리파이에서 가져옴 |

---

0. venv
   - `python -m venv venv`
   - `source venv/bin/activate` (Linux/Mac)
   - `venv\Scripts\activate` (Windows)

1. Install - `pip install -r requirements.txt`
   Flask==3.0.2
   Flask-SQLAlchemy==3.1.1
   python-dateutil==2.8.2
   PyQt6==6.6.1

2. Run Flask Server

   - `FLASK_APP=run.py FLASK_ENV=development flask run`
   - http://localhost:5000 접속

3. Run Raspberry Pi Code
   - `python main.py`
   - 라즈베리파이에서 실행
