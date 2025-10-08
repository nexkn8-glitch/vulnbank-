import os

BASE_DIR = os.path.abspath(os.path.dirname(__file__))

class Config:
    SECRET_KEY = os.environ.get("SECRET_KEY", "dev-secret")  # FIX: set a strong secret in production
    DATABASE = os.environ.get("DATABASE", os.path.join(BASE_DIR, "vulnbank.db"))
    DEBUG = os.environ.get("FLASK_ENV", "production") == "development"
