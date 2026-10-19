from flask import Blueprint, jsonify, g
from models import db, Event, Registration
from utils.auth_helpers import token_required

registrations_bp = Blueprint("registrations", __name__, url_prefix="/api")

@registrations_bp.post("/events/<int:event_id>/register")
@token_required
def register_for_event(event_id):
    if not db.session.get(Event, event_id): return jsonify({"error":"Мероприятие не найдено"}), 404
    if Registration.query.filter_by(user_id=g.current_user_id, event_id=event_id).first():
        return jsonify({"error":"Вы уже зарегистрированы"}), 409
    item = Registration(user_id=g.current_user_id, event_id=event_id)
    db.session.add(item); db.session.commit()
    return jsonify(item.to_dict()), 201

@registrations_bp.get("/me/registrations")
@token_required
def my_registrations():
    return jsonify([item.to_dict() for item in Registration.query.filter_by(user_id=g.current_user_id).all()])
