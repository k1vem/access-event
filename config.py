import os
import secrets

from dotenv import load_dotenv
from sqlalchemy.pool import StaticPool

# Load local .env values when running with `python app.py`.
load_dotenv()


# A development fallback lets the app start without a manually created key.
# Set SECRET_KEY and JWT_SECRET in the environment for stable sessions/tokens.
_DEVELOPMENT_SECRET = secrets.token_hex(32)


class Config:
    SECRET_KEY = os.getenv("SECRET_KEY") or _DEVELOPMENT_SECRET
    JWT_SECRET = os.getenv("JWT_SECRET") or SECRET_KEY
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
