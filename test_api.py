import pytest
from fastapi.testclient import TestClient
from app import app

client = TestClient(app)

def test_root():
    response = client.get("/")
    assert response.status_code == 200
    data = response.json()
    assert data["message"] == "MLOps prediction API running"
    assert data["model_loaded"] is True

def test_health():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "healthy"

def test_predict_setosa():
    response = client.post("/predict", json={"features": [5.1, 3.5, 1.4, 0.2]})
    assert response.status_code == 200
    data = response.json()
    assert data["prediction"] == 0
    assert data["flower_class"] == "setosa"
    assert "latency_ms" in data

def test_predict_versicolor():
    response = client.post("/predict", json={"features": [6.0, 2.9, 4.5, 1.5]})
    assert response.status_code == 200
    data = response.json()
    assert data["prediction"] == 1
    assert data["flower_class"] == "versicolor"

def test_predict_invalid_features():
    response = client.post("/predict", json={"features": [5.1, 3.5]})
    assert response.status_code == 422

def test_prometheus_metrics():
    response = client.get("/metrics")
    assert response.status_code == 200
    assert b"http_requests_total" in response.content
