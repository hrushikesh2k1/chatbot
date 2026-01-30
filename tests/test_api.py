import requests

BASE_URL = "http://127.0.0.1:5000"


def test_health():
    r = requests.get(f"{BASE_URL}/health")
    assert r.status_code == 200


def test_generate():
    payload = {"question": "unit test"}
    r = requests.post(f"{BASE_URL}/ask", json=payload)
    assert r.status_code == 200
    data = r.json()
    assert "answer" in data
