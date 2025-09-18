"""
Script Name : main.py
Description : Entrypoint for FastAPI app (creates app, includes routes)
Author      : @tonybnya
"""
from fastapi import FastAPI

from bmi_app.api import routes_bmi

app = FastAPI(root_path="/api/v1", title="BMI Calculator API", version="1.0")

# include routes
app.include_router(routes_bmi.router, prefix="/bmi", tags=["bmi"])


@app.get('/')
def root():
    """
    Root endpoint.
    """
    return {"message": "Welcome to the BMI Calculator API"}
