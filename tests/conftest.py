import os
<<<<<<< HEAD
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
=======
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
>>>>>>> 93f660917251956e4d1be85cd249fe95ff9b5fe6
