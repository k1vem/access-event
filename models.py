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
    is_deaf = db.Column(db.Boolean, default=False, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    registrations = db.relationship("Registration", back_populates="user", cascade="all, delete-orphan")
    events = db.relationship("Event", back_populates="organizer")
    reviews = db.relationship("Review", back_populates="user", cascade="all, delete-orphan")
    def set_password(self, password):
        self.password_hash = generate_password_hash(password, method="pbkdf2:sha256")
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
    def to_dict(self):
        return {"id": self.id, "username": self.username, "email": self.email,
                "role": self.role, "is_deaf": self.is_deaf}

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
        return {"id": self.id, "title": self.title, "description": self.description or "",
                "event_date": self.event_date.isoformat(), "location": self.location or "",
                "accessibility": self.accessibility or "", "is_inclusive": self.is_inclusive,
                "max_participants": self.max_participants, "organizer_id": self.organizer_id,
                "registration_count": len(self.registrations)}

class Registration(db.Model):
    __tablename__ = "registrations"
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    event_id = db.Column(db.Integer, db.ForeignKey("events.id", ondelete="CASCADE"), nullable=False)
    registered_at = db.Column(db.DateTime, default=datetime.utcnow)
    status = db.Column(db.String(20), default="pending", nullable=False)
    __table_args__ = (db.UniqueConstraint("user_id", "event_id", name="uq_user_event"),)
    user = db.relationship("User", back_populates="registrations")
    event = db.relationship("Event", back_populates="registrations")
    def to_dict(self):
        return {"id": self.id, "user_id": self.user_id, "event_id": self.event_id,
                "status": self.status, "registered_at": self.registered_at.isoformat()}

class Message(db.Model):
    __tablename__ = "messages"
    id = db.Column(db.Integer, primary_key=True)
    sender_id = db.Column(db.Integer, db.ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    event_id = db.Column(db.Integer, db.ForeignKey("events.id", ondelete="CASCADE"), nullable=False)
    content = db.Column(db.Text, nullable=False)
    sent_at = db.Column(db.DateTime, default=datetime.utcnow)
    sender = db.relationship("User")

class EventCategory(db.Model):
    __tablename__ = "event_categories"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True, nullable=False)
    description = db.Column(db.Text, default="")

class EventCategoryLink(db.Model):
    __tablename__ = "event_category_link"
    id = db.Column(db.Integer, primary_key=True)
    event_id = db.Column(db.Integer, db.ForeignKey("events.id", ondelete="CASCADE"), nullable=False)
    category_id = db.Column(db.Integer, db.ForeignKey("event_categories.id", ondelete="CASCADE"), nullable=False)
    __table_args__ = (db.UniqueConstraint("event_id", "category_id", name="uq_event_category"),)
    event = db.relationship("Event")
    category = db.relationship("EventCategory")

class Notification(db.Model):
    __tablename__ = "notifications"
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    event_id = db.Column(db.Integer, db.ForeignKey("events.id", ondelete="CASCADE"), nullable=True)
    type = db.Column(db.String(50), nullable=False, default="visual")
    message = db.Column(db.Text, default="")
    is_read = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    user = db.relationship("User")
    event = db.relationship("Event")

class Review(db.Model):
    __tablename__ = "reviews"
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    event_id = db.Column(db.Integer, db.ForeignKey("events.id", ondelete="CASCADE"), nullable=False)
    rating = db.Column(db.Integer, nullable=False)
    comment = db.Column(db.Text, default="")
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    __table_args__ = (db.UniqueConstraint("user_id", "event_id", name="uq_review_user_event"),
                      db.CheckConstraint("rating >= 1 AND rating <= 5", name="ck_review_rating"))
    user = db.relationship("User", back_populates="reviews")
    event = db.relationship("Event")
    def to_dict(self):
        return {"id": self.id, "user_id": self.user_id, "event_id": self.event_id,
                "rating": self.rating, "comment": self.comment or "",
                "created_at": self.created_at.isoformat()}
