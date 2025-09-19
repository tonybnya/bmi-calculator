"""
Script Name : test_categories.py
Description : Tests for /bmi endpoints
Author      : @tonybnya
"""
import pytest
from fastapi.testclient import TestClient

from bmi_app.core.utils import (calculate_bmi, categorize, get_formula, to_kg,
                                to_meters)
from bmi_app.main import app

client = TestClient(app)


@pytest.mark.parametrize(
    "height_m, weight_kg, expected",
    [
        (1.80, 75, (23.15, 23.148148148148145)),
        (1.60, 50, (19.53, 19.531249999999996)),
        (1.75, 95, (31.02, 31.020408163265305)),
        (2.00, 100, (25.0, 25.0)),
        (1.50, 45, (20.0, 20.0)),
        (1.70, 70, (24.22, 24.221453287197235))
    ]
)
def test_calculate_bmi(
    height_m: float,
    weight_kg,
    expected: tuple[float, float]
) -> None:
    assert calculate_bmi(height_m, weight_kg) == expected


def test_calculate_bmi_endpoint_normal() -> None:
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


@pytest.mark.parametrize(
    "bmi, category",
    [
        (18.4, 'Underweight'),
        (18.5, 'Normal'),
        (24.9, 'Normal'),
        (26, 'Overweight'),
        (31, 'Obesity I'),
        (39, 'Obesity II'),
        (45, 'Obesity III'),
        (50, 'Obesity III')
    ]
)
def test_category_boundaries(bmi: float, category: str) -> None:
    assert categorize(bmi) == category


@pytest.mark.parametrize(
    "weight, unit, expected",
    [
        (1, "kg", 1.0),
        (0, "kg", 0.0),
        (2.5, "kg", 2.5),
        (1, "lb", 0.45359237),
        (2, "lb", 0.90718474),
        (10, "lb", 4.535923700000001),
        (150, "lb", 68.0388555),
        (0, "lb", 0.0),
        (0.5, "lb", 0.226796185),
    ]
)
def test_unit_conversion_to_kg(
    weight: float,
    unit: str,
    expected: float
) -> None:
    assert to_kg(weight, unit) == expected


@pytest.mark.parametrize(
    "height, unit, expected",
    [
        (1, "m", 1.0),
        (0, "m", 0.0),
        (2.5, "m", 2.5),
        (100, "cm", 1.0),
        (250, "cm", 2.5),
        (0, "cm", 0.0),
        (1, "in", 0.0254),
        (12, "in", 0.30479999999999996),
        (72, "in", 1.8288),
        (0, "in", 0.0)
    ]
)
def test_unit_conversion_to_meters(
    height: float,
    unit: str,
    expected: float
) -> None:
    assert to_meters(height, unit) == expected


@pytest.mark.parametrize(
    "bmi_raw, height_m, weight_kg, formula",
    [
        (
            23.148148148148145,
            1.80,
            75,
            "75 kg / (1.8 m) ^ 2 = 23.148148148148145"
        ),
        (
            19.531249999999996,
            1.60,
            50,
            "50 kg / (1.6 m) ^ 2 = 19.531249999999996"
        ),
        (
            31.020408163265305,
            1.75,
            95,
            "95 kg / (1.75 m) ^ 2 = 31.020408163265305"
        ),
        (
            25.0,
            2.00,
            100,
            "100 kg / (2.0 m) ^ 2 = 25.0"
        ),
        (
            20.0,
            1.50,
            45,
            "45 kg / (1.5 m) ^ 2 = 20.0"
        )
    ]
)
def test_get_formula(
    bmi_raw: float,
    height_m: float,
    weight_kg: float,
    formula: str
) -> None:
    assert get_formula(bmi_raw, height_m, weight_kg) == formula
