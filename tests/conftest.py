import os
os.environ["TESTING"]="1"
os.environ["SECRET_KEY"]="test-secret-key-must-be-32-bytes-or-more-12345"
import pytest
from app import create_app
from models import db
@pytest.fixture()
def app():
    application=create_app()
    with application.app_context():
        db.drop_all(); db.create_all(); yield application; db.session.remove(); db.drop_all()
@pytest.fixture()
def client(app): return app.test_client()
@pytest.fixture()
def user(app):
    from models import User
    u=User(username="testuser",email="user@example.com",password_hash="",role="user")
    u.set_password("StrongPass123"); db.session.add(u); db.session.commit(); return u
