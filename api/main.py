"""
Script Name : main.py
Description : Main application
Author      : @tonybnya
"""
from fastapi import FastAPI

app = FastAPI(root_path="/api/v1")


@app.get('/')
def root():
    """
    Root endpoint.
    """
    return {"message": "Hello, World!"}
