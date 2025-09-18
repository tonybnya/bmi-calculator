"""
Script Name : test_categories.py
Description : Tests for BMI category endpoints
Author      : @tonybnya
"""
from fastapi.testclient import TestClient

from bmi_app.main import app

client = TestClient(app)


def test_calculate_bmi_endpoint_normal():
    """
    Test /bmi/categories endpoint
    """
    response = client.get(
        "/bmi/categories",
    )
    assert response.status_code == 200
    data = response.json()
    assert "categories" in data
    assert len(data.get("categories")) == 6
    for category in data.get("categories"):
        assert "name" in category
        assert "min_value" in category
        assert "max_value" in category
