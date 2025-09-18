"""
Script Name : core.py
Description : Helper functions
Author      : @tonybnya
"""


def calculate_bmi(height_m: float, weight_kg: float) -> tuple[float, float]:
    """
    Calculate the BMI.
    Formula: BMI = weight_kg / (height_m ** 2)
    """
    bmi_raw = weight_kg / (height_m ** 2)
    bmi = round(bmi_raw, 2)
    return (bmi, bmi_raw)


def categorize(bmi: float) -> str:
    """
    Define the category of a BMI measure.
    """
    if bmi < 18.5:
        return "Underweight"
    if bmi < 25:
        return "Normal"
    if bmi < 30:
        return "Overweight"
    if bmi < 35:
        return "Obesity I"
    if bmi < 40:
        return "Obesity II"
    # bmi above 40
    return "Obesity III"


def to_kg(weight: float, unit: str) -> float:
    """
    Convert a given weight to kilograms.
    """
    # kilograms -> kilograms
    if unit == "kg":
        return weight
    # lb (pounds) -> kg
    return weight * 0.45359237


def to_meters(height: float, unit: str) -> float:
    """
    Convert a given height to meters.
    """
    # meters -> meters
    if unit == "m":
        return height

    # centimeters -> meters
    if unit == "cm":
        return height / 100.0

    # in/ft(inches/feet) -> meters
    return height * 0.0254
