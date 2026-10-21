import os
<<<<<<< HEAD

class Config:
    SECRET_KEY = os.environ.get("SECRET_KEY", "dev-secret-key")
    SQLALCHEMY_DATABASE_URI = os.environ.get("DATABASE_URL", "sqlite:///accessevent.db")
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    JWT_EXPIRATION_HOURS = 24
=======
from sqlalchemy.pool import StaticPool

class Config:
    SECRET_KEY = os.getenv("SECRET_KEY", "development-only-change-me")
    JWT_SECRET = os.getenv("JWT_SECRET", SECRET_KEY)
    JWT_EXPIRATION_HOURS = int(os.getenv("JWT_EXPIRATION_HOURS", "24"))
    SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URL", "sqlite:///accessevent.db")
    SQLALCHEMY_TRACK_MODIFICATIONS = False

class TestingConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = "sqlite://"
    SQLALCHEMY_ENGINE_OPTIONS = {"poolclass": StaticPool, "connect_args": {"check_same_thread": False}}

def get_config():
    return TestingConfig if os.getenv("TESTING") == "1" else Config
>>>>>>> 93f660917251956e4d1be85cd249fe95ff9b5fe6
