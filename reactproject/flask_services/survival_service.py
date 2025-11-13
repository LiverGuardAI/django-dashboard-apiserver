# flask_services/survival_service.py
import requests

FLASK_URL = "http://127.0.0.1:5000/api/predict_survival"   # Docker 환경이면 flask:5000

def predict_survival_from_flask(payload):
    """
    Django → Flask로 POST 요청 보내는 함수
    """
    try:
        response = requests.post(FLASK_URL, json=payload, timeout=10)

        if response.status_code != 200:
            return {
                "error": "Flask server error",
                "status": response.status_code,
                "detail": response.text
            }

        return response.json()

    except Exception as e:
        return {"error": str(e)}