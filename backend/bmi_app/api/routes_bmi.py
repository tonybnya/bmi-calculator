"""
Script Name : routes_bmi.py
Description : Endpoints for BMI calculation
Author      : @tonybnya
"""
from fastapi import APIRouter

from bmi_app.core.utils import (calculate_bmi, categorize, get_formula, to_kg,
                                to_meters)
from bmi_app.schemas import BMICalculateRequest, BMICalculateResponse

router = APIRouter()


@router.post("/", response_model=BMICalculateResponse)
def calculate_bmi_endpoint(data: BMICalculateRequest):
    """
    Calculate BMI based on given height and weight.
    Return BMI values and category.
    """
    height_m: float = to_meters(data.height, data.height_unit)
    weight_kg: float = to_kg(data.weight, data.weight_unit)
    bmi, bmi_raw = calculate_bmi(height_m, weight_kg)

    category: str = categorize(bmi)
    formula: str = get_formula(bmi_raw, height_m, weight_kg)

    return BMICalculateResponse(
        height=data.height,
        weight=data.weight,
        bmi=bmi,
        bmi_raw=bmi_raw,
        category=category,
        formula=formula
    )
