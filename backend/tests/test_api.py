import pytest
from fastapi.testclient import TestClient
from main import app
from database import SessionLocal
import auth

client = TestClient(app)

def test_token_generation():
    auth.seed_users()
    response = client.post(
        "/api/token",
        data={"username": "viewer", "password": "password123"}
    )
    assert response.status_code == 200
    assert "access_token" in response.json()
    assert response.json()["role"] == "Viewer"

def test_esd_unauthorized():
    response = client.post("/api/esd", json={"equipment_id": "V-101"})
    assert response.status_code == 401

def test_esd_viewer_forbidden():
    auth.seed_users()
    token_res = client.post("/api/token", data={"username": "viewer", "password": "password123"})
    token = token_res.json()["access_token"]
    
    response = client.post(
        "/api/esd",
        headers={"Authorization": f"Bearer {token}"},
        json={"equipment_id": "V-101"}
    )
    assert response.status_code == 403

def test_esd_admin_success():
    auth.seed_users()
    token_res = client.post("/api/token", data={"username": "admin", "password": "password123"})
    token = token_res.json()["access_token"]
    
    response = client.post(
        "/api/esd",
        headers={"Authorization": f"Bearer {token}"},
        json={"equipment_id": "V-101"}
    )
    assert response.status_code == 200
    assert response.json()["status"] == "esd_triggered"
