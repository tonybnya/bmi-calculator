"""
Script Name : test_categories.py
Description : Tests for BMI category endpoints
Author      : @tonybnya
"""
from fastapi.testclient import TestClient

from bmi_app.main import app

client = TestClient(app)


def test_categories_endpoint():
    """
    Test /categories/ endpoint
    """
    response = client.get(
        "/categories/",
    )
    assert response.status_code == 200
    data = response.json()
    assert "categories" in data
    assert len(data.get("categories")) == 6
    for category in data.get("categories"):
        assert "name" in category
        assert "min_value" in category
        assert "max_value" in category


def test_single_category_endpoint():
    """
    Test /categories/{id} endpoint
    """
    response = client.get("/categories/2")
    assert response.status_code == 200
    data = response.json()
    assert "name" in data
    assert "min_value" in data 
    assert "max_value" in data
    assert data["name"] == "Normal"
    assert data["min_value"] == 18.5
    assert data["max_value"] == 25.0


def test_category_not_found():
    """
    Test /categories/{id} endpoint with invalid ID
    """
    response = client.get("/categories/999")
    assert response.status_code == 404
    data = response.json()
    assert "detail" in data
    assert "not found" in data["detail"]
