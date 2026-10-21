import os
from pathlib import Path

from dotenv import load_dotenv
from sqlalchemy.pool import StaticPool

# Load local development settings when running python app.py.
# Existing environment variables (including CI settings) take precedence.
load_dotenv(Path(__file__).resolve().parent / ".env")


class Config:
    SECRET_KEY = os.getenv("SECRET_KEY", "development-only-change-me")
    JWT_SECRET = os.getenv("JWT_SECRET", SECRET_KEY)
    JWT_EXPIRATION_HOURS = int(os.getenv("JWT_EXPIRATION_HOURS", "24"))
    SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URL", "sqlite:///accessevent.db")
    SQLALCHEMY_TRACK_MODIFICATIONS = False


class TestingConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = "sqlite://"
    SQLALCHEMY_ENGINE_OPTIONS = {
        "poolclass": StaticPool,
        "connect_args": {"check_same_thread": False},
    }


def get_config():
    return TestingConfig if os.getenv("TESTING") == "1" else Config
