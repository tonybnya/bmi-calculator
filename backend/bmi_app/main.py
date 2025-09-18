"""
Script Name : main.py
Description : Entrypoint for FastAPI app (creates app, includes routes)
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
