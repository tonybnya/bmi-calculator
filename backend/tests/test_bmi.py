"""
Script Name : test_categories.py
Description : Tests for /bmi endpoints
Author      : @tonybnya
"""
from fastapi.testclient import TestClient

from bmi_app.main import app

client = TestClient(app)


def test_calculate_bmi_endpoint_normal():
    """
    Test /bmi endpoint for 'Normal' BMI
    """
    response = client.post(
        "/bmi/",
        json={
            "weight": 70,
            "weight_unit": "kg",
            "height": 175,
            "height_unit": "cm"
        }
    )
    assert response.status_code == 200
    data = response.json()
    assert data.get('height') == 175
    assert data.get('weight') == 70
    assert data.get('bmi') == 22.86
    assert data.get('bmi_raw') == 22.857142857142858
    assert data.get('category') == "Normal"
    assert data.get('formula') == "70.0 kg / (1.75 m) ^ 2 = 22.857142857142858"
