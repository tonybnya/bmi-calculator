"""
Script Name : main.py
Description : Pydantic schemas (request/response validation)
Author      : @tonybnya
"""
from pydantic import BaseModel, Field


class BMICalculateRequest(BaseModel):
    height: float = Field(..., gt=0, description="Numeric value of the height")
    height_unit: str = Field(..., description="Unit of the height ('cm', 'm', or 'in/ft')")
    weight: float = Field(..., gt=0, description="Numeric value of the weight")
    weight_unit: str = Field(..., description="Unit of the weight ('kg' or 'lb')")


class BMICalculateResponse(BaseModel):
    height: float
    weight: float
    bmi: float
    bmi_raw: float
    category: str
    formula: str
