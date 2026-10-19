from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash

db = SQLAlchemy()

class User(db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False, index=True)
    password_hash = db.Column(db.String(255), nullable=False)
    role = db.Column(db.String(20), nullable=False, default="user")
    is_deaf = db.Column(db.Boolean, nullable=False, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    registrations = db.relationship("Registration", back_populates="user", cascade="all, delete-orphan")
    events = db.relationship("Event", back_populates="organizer")
    def set_password(self, password): self.password_hash = generate_password_hash(password)
    def check_password(self, password): return check_password_hash(self.password_hash, password)
    def to_dict(self):
        return {"id": self.id, "username": self.username, "email": self.email, "role": self.role, "is_deaf": self.is_deaf}

class Event(db.Model):
    __tablename__ = "events"
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text, default="")
    event_date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    location = db.Column(db.String(200), default="")
    accessibility = db.Column(db.String(500), default="")
    is_inclusive = db.Column(db.Boolean, default=True)
    max_participants = db.Column(db.Integer, default=50)
    organizer_id = db.Column(db.Integer, db.ForeignKey("users.id", ondelete="SET NULL"), nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    organizer = db.relationship("User", back_populates="events")
    registrations = db.relationship("Registration", back_populates="event", cascade="all, delete-orphan")
    def to_dict(self):
        return {"id": self.id, "title": self.title, "description": self.description or "", "event_date": self.event_date.isoformat(), "location": self.location or "", "accessibility": self.accessibility or "", "is_inclusive": self.is_inclusive, "organizer_id": self.organizer_id}

class Registration(db.Model):
    __tablename__ = "registrations"
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    event_id = db.Column(db.Integer, db.ForeignKey("events.id", ondelete="CASCADE"), nullable=False)
    registered_at = db.Column(db.DateTime, default=datetime.utcnow)
    status = db.Column(db.String(20), default="confirmed")
    __table_args__ = (db.UniqueConstraint("user_id", "event_id", name="uq_user_event"),)
    user = db.relationship("User", back_populates="registrations")
    event = db.relationship("Event", back_populates="registrations")
    def to_dict(self): return {"id": self.id, "user_id": self.user_id, "event_id": self.event_id, "status": self.status}

class Message(db.Model):
    __tablename__ = "messages"
    id = db.Column(db.Integer, primary_key=True)
    sender_id = db.Column(db.Integer, db.ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    event_id = db.Column(db.Integer, db.ForeignKey("events.id", ondelete="CASCADE"), nullable=False)
    content = db.Column(db.Text, nullable=False)
    sent_at = db.Column(db.DateTime, default=datetime.utcnow)

class EventCategory(db.Model):
    __tablename__ = "event_categories"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, default="")

class EventCategoryLink(db.Model):
    __tablename__ = "event_category_link"
    id = db.Column(db.Integer, primary_key=True)
    event_id = db.Column(db.Integer, db.ForeignKey("events.id", ondelete="CASCADE"), nullable=False)
    category_id = db.Column(db.Integer, db.ForeignKey("event_categories.id", ondelete="CASCADE"), nullable=False)
    __table_args__ = (db.UniqueConstraint("event_id", "category_id"),)

class Notification(db.Model):
    __tablename__ = "notifications"
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    event_id = db.Column(db.Integer, db.ForeignKey("events.id", ondelete="CASCADE"), nullable=True)
    type = db.Column(db.String(50), nullable=False, default="visual")
    is_read = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
