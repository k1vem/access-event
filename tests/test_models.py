from models import User, Event, Registration, db
def test_password_hashing(app):
    u=User(username="tester",email="tester@example.com",password_hash=""); u.set_password("StrongPass123")
    assert u.check_password("StrongPass123") and not u.check_password("wrong") and u.password_hash!="StrongPass123"
def test_event_registration_relationship(app,user):
    event=Event(title="Доступная лекция",organizer_id=user.id,accessibility="субтитры"); db.session.add(event); db.session.commit()
    db.session.add(Registration(user_id=user.id,event_id=event.id)); db.session.commit(); assert event.registrations[0].user_id==user.id
