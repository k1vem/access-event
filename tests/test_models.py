from models import User, Event, Registration, db
from utils.accessibility import accessibility_matches


def test_password_hashing(app):
    user = User(username="tester", email="tester@example.com", password_hash="")
    user.set_password("StrongPass123")
    assert user.check_password("StrongPass123")
    assert not user.check_password("wrong")
    assert user.password_hash != "StrongPass123"


def test_event_registration_relationship(app, user):
    event = Event(title="Доступная лекция", organizer_id=user.id, accessibility="субтитры")
    db.session.add(event)
    db.session.commit()
    registration = Registration(user_id=user.id, event_id=event.id)
    db.session.add(registration)
    db.session.commit()
    assert event.registrations[0].user_id == user.id


def test_user_serialization_does_not_expose_password(app, user):
    data = user.to_dict()
    assert data["username"] == "testuser"
    assert data["email"] == "user@example.com"
    assert "password_hash" not in data
    assert "password" not in data


def test_event_serialization_has_accessibility_fields(app, user):
    event = Event(
        title="Лекция с субтитрами",
        organizer_id=user.id,
        accessibility="субтитры, текстовый чат",
        location="Аудитория 12",
    )
    db.session.add(event)
    db.session.commit()

    data = event.to_dict()
    assert data["title"] == "Лекция с субтитрами"
    assert "субтитры" in data["accessibility"]
    assert data["registration_count"] == 0


def test_registration_serialization_contains_status(app, user):
    event = Event(title="Текстовая встреча", organizer_id=user.id)
    db.session.add(event)
    db.session.commit()
    registration = Registration(user_id=user.id, event_id=event.id, status="pending")
    db.session.add(registration)
    db.session.commit()

    data = registration.to_dict()
    assert data["user_id"] == user.id
    assert data["event_id"] == event.id
    assert data["status"] == "pending"


def test_accessibility_matching_is_case_insensitive(app):
    assert accessibility_matches("Субтитры, Текстовый чат", ["субтитры"])
    assert not accessibility_matches("Субтитры", ["сурдоперевод"])
