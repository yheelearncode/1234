import requests

API_BASE_URL = "http://127.0.0.1:5000"

def get_weather():
    try:
        response = requests.get(f"{API_BASE_URL}/api/weather", timeout=5)
        response.raise_for_status()
        data = response.json()
        
        # 응답 데이터 검증 및 기본값 설정
        return {
            "weather": data.get("weather", "정보 없음"),
            "temperature": data.get("temperature", "N/A"),
            "dust": data.get("dust", "정보 없음")
        }
    except requests.exceptions.ConnectionError:
        # Flask 서버가 실행되지 않은 경우
        return {"weather": "서버 연결 실패", "temperature": "N/A", "dust": "정보 없음"}
    except requests.exceptions.Timeout:
        # 요청 시간 초과
        return {"weather": "응답 시간 초과", "temperature": "N/A", "dust": "정보 없음"}
    except requests.exceptions.RequestException:
        # 기타 네트워크 오류
        return {"weather": "네트워크 오류", "temperature": "N/A", "dust": "정보 없음"}
    except Exception:
        # 예상치 못한 오류
        return {"weather": "오류 발생", "temperature": "N/A", "dust": "오류 발생"}