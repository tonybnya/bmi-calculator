"""
Script Name : main.py
Description : Entrypoint for FastAPI app (creates app, includes routes)
Author      : @tonybnya
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from bmi_app.api import routes_bmi, routes_categories
from bmi_app.core.config import get_settings

# Get settings instance
settings = get_settings()

# Create FastAPI app with settings
app = FastAPI(
    title=settings.app_name,
    version=settings.app_version,
    debug=settings.debug,
    root_path=settings.api_v1_prefix,
    description="A comprehensive BMI (Body Mass Index) calculator API \
    that helps users track their health metrics.",
    docs_url="/docs" if settings.debug else None,
    redoc_url="/redoc" if settings.debug else None,
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.allowed_origins,
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
    allow_headers=["*"],
)

# include routes
app.include_router(routes_bmi.router, prefix="/bmi", tags=["bmi"])
app.include_router(routes_categories.router, prefix="/bmi/categories", tags=["categories"])


@app.get('/', tags=["root"])
def root():
    """
    Root endpoint with API information.
    """
    return {
        "message": f"Welcome to the {settings.app_name}",
        "version": settings.app_version,
        "status": "running",
        "debug_mode": settings.debug,
        "documentation": "/docs" if settings.debug else "Documentation disabled in production",
    }
