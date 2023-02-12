from fastapi.testclient import TestClient

from src.main import app

client = TestClient(app)

def test_get_all_user():
    response = client.get("/user/get_all_user")
    assert response.status_code == 200
    

def test_get_media_by_user():
    response = client.get("/user/get_media_by_user/newjeans_official")
    assert response.status_code == 200
    assert len(response.json()) == 29