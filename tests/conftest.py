import os

os.environ.setdefault("TESTING", "1")
os.environ.setdefault("SECRET_KEY", "test-secret-key-must-be-32-bytes-or-more-12345")
os.environ.setdefault("DATABASE_URL", "sqlite:///:memory:")

import pytest

from app import create_app
from models import db


@pytest.fixture()
def app():
    application = create_app()
    application.config.update(TESTING=True, SQLALCHEMY_DATABASE_URI="sqlite:///:memory:")
    with application.app_context():
        db.drop_all()
        db.create_all()
        yield application
        db.session.remove()
        db.drop_all()


@pytest.fixture()
def client(app):
    return app.test_client()


@pytest.fixture()
def user(app):
    from models import User

    account = User(
        username="testuser",
        email="user@example.com",
        password_hash="",
        role="user",
    )
    account.set_password("StrongPass123")
    db.session.add(account)
    db.session.commit()
    return account