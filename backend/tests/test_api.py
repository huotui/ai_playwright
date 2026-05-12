import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_root():
    response = client.get("/")
    assert response.status_code == 200
    assert "name" in response.json()

def test_health():
    response = client.get("/api/health")
    assert response.status_code == 200
    assert response.json()["status"] == "healthy"

def test_create_test_case():
    test_case_data = {
        "name": "测试登录功能",
        "description": "验证网站登录流程",
        "instruction": "打开登录页面，输入用户名和密码，点击登录按钮",
        "start_url": "https://example.com/login"
    }
    response = client.post("/api/test-cases", json=test_case_data)
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == test_case_data["name"]
    assert data["id"] > 0

def test_get_test_cases():
    response = client.get("/api/test-cases")
    assert response.status_code == 200
    assert isinstance(response.json(), list)

def test_get_test_case():
    response = client.get("/api/test-cases/1")
    assert response.status_code == 200
