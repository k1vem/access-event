import os
import pytest
os.environ.setdefault("TESTING", "1")
os.environ.setdefault("DATABASE_URL", "sqlite:///:memory:")
os.environ.setdefault("SECRET_KEY", "test-secret-key-must-be-32-bytes-or-more-12345")
from app import app, db

@pytest.fixture
def client():
    app.config["TESTING"] = True
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///:memory:"
    with app.test_client() as c:
        with app.app_context():
            db.create_all()
            yield c
            db.session.remove()
            db.drop_all()